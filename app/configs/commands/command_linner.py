import os
import random
from typing import cast

import structlog
from dotenv import load_dotenv

from app.configs.db.database import UserEntity, RolesEntity, UserRolesEntity
from app.repositories.providers.my_roles_repository_provider import MyRolesRepositoryProvider
from app.repositories.providers.roles_repository_provider import RolesRepositoryProvider
from app.repositories.providers.user_repository_provider import UserRepositoryProvider
from app.services.providers.crypto_service import hash_password

load_dotenv()

NAME_APP = os.getenv("NAME_APP")

ROLE_SUPER_ADM = os.getenv("ROLE_SUPER_ADM")
ROLE_ADM = os.getenv("ROLE_ADM")
ROLE_MASTER = os.getenv("ROLE_MASTER")
ROLE_USER = os.getenv("ROLE_USER")
ROLE_ENTERPRISE = os.getenv("ROLE_ENTERPRISE")

logger = structlog.get_logger()

class CommandLinner:
    def __init__(self,
                 user_repository: UserRepositoryProvider,
                 role_repository: RolesRepositoryProvider,
                 my_role_repository: MyRolesRepositoryProvider,
                 ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.my_role_repository = my_role_repository
        logger.debug("CommandLinner initialized with repository providers.")

    async def init_commands(self):
        logger.info("⭐ Starting essential system initialization commands.")

        if ROLE_ADM is None or ROLE_SUPER_ADM is None:
            raise ValueError("ROLE_ADM and ROLE_SUPER_ADM are nulls")

        role_super_adm = await self._get_or_create_role(title=ROLE_SUPER_ADM, is_immutable=True)
        role_adm = await self._get_or_create_role(title=ROLE_ADM, is_immutable=True)
        role_master = await self._get_or_create_role(title=ROLE_MASTER, is_immutable=True)
        role_user = await self._get_or_create_role(title=ROLE_USER, is_immutable=True)
        role_enterprise = await self._get_or_create_role(title=ROLE_ENTERPRISE, is_immutable=True)
        await self.create_master_adm(role_master)

        logger.info("✅ System initialization commands completed successfully.")

    async def _get_or_create_role(self, title: str, is_immutable: bool) -> RolesEntity | None:
        logger.debug(f"Checking for role: {title}.")

        slug = title.lower().replace("_", "")

        role_entity = await self.role_repository.get_by_slug(slug)

        if role_entity:
            logger.info(f"Role '{title}' already exists (ID: {cast(int, role_entity.id)}). Skipping creation.")
            return role_entity

        logger.warning(f"Role '{title}' not found. Creating new immutable role...")
        new_role = RolesEntity(
            title=title,
            slug=slug,
            is_active=True,
            is_immutable=is_immutable
        )

        created_role = await self.role_repository.add(new_role)
        logger.info(f"✨ New Role '{title}' created with ID: {cast(int, created_role.id)}.")
        return created_role

    async def create_master_adm(self, role: RolesEntity | None):
        logger.info("Starting check and creation of SUPER_ADM system user.")

        if NAME_APP is None:
            logger.critical("NAME_APP environment variable is missing. Cannot create system user.")
            raise ValueError("NAME_APP is None")

        if role.title != "MASTER":
            logger.error(f"Expected MASTER role, but received '{role.title}'. Aborting user creation.")
            raise ValueError("role title is different of MASTER")

        email = f"{NAME_APP.lower()}.system@gmail.com"

        check_user_exists = await self.user_repository.exists_by_email(email)

        if check_user_exists:
            logger.info(f"System user ({email}) already exists. Skipping creation.")
            return None

        #password = str(random.randrange(10, 30))
        password = str(12345678)
        logger.warning(f"Creating new system user: {email}. Temporary password generated (NOT LOGGED).")

        user = UserEntity()
        user.name = NAME_APP.lower()
        user.email = email
        user.password = hash_password(password)

        user_created = await self.user_repository.add(user)
        user_id = cast(int, user_created.id)
        logger.info(f"👤 System user created (ID: {user_id}). Proceeding to assign role.")
        logger.info(f"👤 System user email: {user_created.email} and password: {user_created.password}")

        role_id = cast(int, cast(object, role.id))
        check_exists_my_role = await self.my_role_repository.exists_by_user_id_and_role_id(
            user_id=user_id,
            role_id=role_id
        )

        if check_exists_my_role:
            logger.warning(f"Role {role_id} already assigned to user {user_id}. Skipping role assignment.")
            return None

        my_role = UserRolesEntity()
        my_role.role_id = role.id
        my_role.user_id = user_created.id

        await self.my_role_repository.add(my_role)
        logger.info(f"🔑 SUPER_ADM role successfully assigned to system user {user_id}.")

        return None