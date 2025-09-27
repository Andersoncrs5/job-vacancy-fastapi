import random
from httpx import ASGITransport, AsyncClient
from app.configs.db.enums import MediaType
from app.schemas.media_post_user_schemas import CreateMediaPostUserDTO
from app.schemas.user_schemas import CreateUserDTO, LoginDTO
from app.schemas.enterprise_schemas import *
from app.schemas.post_user_schemas import CreatePostUserDTO, UpdatePostUserDTO, PostUserOUT
from main import app
from typing import Final
from app.schemas.curriculum_schemas import *
from pydantic import BaseModel
from app.utils.res.tokens import Tokens
from app.schemas.category_schemas import *
from app.schemas.industry_schemas import *
from app.schemas.skill_schemas import *
from app.schemas.my_skill_schemas import *
from app.schemas.post_enterprise_schemas import CreatePostEnterpriseDTO, UpdatePostEnterpriseDTO, PostEnterpriseOUT
from app.configs.db.enums import ProficiencyEnum
from datetime import date

class UserTestData(BaseModel):
    dto: CreateUserDTO
    tokens: Tokens

async def create_post_enterprise(user_data, enterprise_data, category_data):
    URL: Final[str] = "/api/v1/post-enterprise"
    num = random.randint(10000,10000000000000)

    dto = CreatePostEnterpriseDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{category_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Post created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['title'] == dto.title
    assert data['body']['content'] == dto.content
    assert data['body']['url_image'] == dto.url_image
    assert data['body']['category_id'] == category_data.id
    assert data['body']['enterprise_id'] == enterprise_data.id

    return PostEnterpriseOUT(
        id = data['body']['id'],
        title = data['body']['title'],
        content = data['body']['content'],
        url_image = data['body']['url_image'],
        enterprise_id = data['body']['enterprise_id'],
        category_id = data['body']['category_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_my_skill(user_data, skill):
    URL: Final[str] = '/api/v1/my-skill'

    dto = CreateMySkillDTO(
        skill_id = skill.id,
        proficiency = ProficiencyEnum.basic,
        certificate_url = None,
        datails = None,
        years_of_experience = 2,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201    

    assert data['body']['skill_id'] == dto.skill_id
    assert data['body']['proficiency'] == dto.proficiency
    assert data['body']['certificate_url'] == dto.certificate_url
    assert data['body']['datails'] == dto.datails
    assert data['body']['years_of_experience'] == dto.years_of_experience

    return MySkillOUT(
        user_id = data['body']['user_id'],
        skill_id = data['body']['skill_id'],
        proficiency = data['body']['proficiency'],
        certificate_url = data['body']['certificate_url'],
        datails = data['body']['datails'],
        years_of_experience = data['body']['years_of_experience'],
        last_used_date = date.today(),
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_skill(user_data):
    URL: Final[str] = '/api/v1/skill'
    num = random.randint(10000,100000000000000)

    dto = CreateSkillDTO(
        name = f"name {num}" 
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})


    data = response.json()
    assert response.status_code == 201

    assert data['body']['id'] is not None
    assert data['body']['name'] == dto.name

    return SkillOUT(
        id = data['body']['id'],
        name = data['body']['name'],
        is_active = data['body']['is_active'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_curriculum(user_data):
    URL: Final[str] = '/api/v1/curriculum'

    dto = CreateCurriculumDTO(
        title = "a little about me",
        description = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Curriculum created with successfully"
    assert data['code'] == 201
    assert data['body']['id'] is not None
    assert data['body']['user_id'] is not None
    assert data['body']['title'] == dto.title

    return CurriculumOUT(
        id = data['body']['id'],
        user_id = data['body']['user_id'],
        title = data['body']['title'],
        is_updated = data['body']['is_updated'],
        description = data['body']['description'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_media_post_user(user_data: UserTestData, post_user_data: PostUserOUT):
    URL: Final[str] = '/api/v1/media-post-user'
    
    dto = CreateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = MediaType.IMAGE,
        order = 1,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(f"{URL}/{post_user_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Media created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['post_id'] == post_user_data.id

    from app.schemas.media_post_user_schemas import MediaPostUserOUT
    return MediaPostUserOUT(
        id = data['body']['id'],
        url = data['body']['url'],
        type = data['body']['type'],
        order = data['body']['order'],
        caption = data['body']['caption'],
        size = data['body']['size'],
        mime_type = data['body']['mime_type'],
        post_id = data['body']['post_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_favorite_post_user(user_data: UserTestData, category_data: CategoryOUT, post_data: PostUserOUT):
    URL: Final[str] = '/api/v1/favorite-post-user'

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}/{post_data.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

    assert response.status_code == 201

    assert data['message'] =="Post favorited with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body'] is not None
    assert data['path'] is None
    assert data['version'] == 1

    return int(data['body'])

async def create_enterprise(user_data: UserTestData, industry_data: IndustryOUT):
    num: Final = random.randint(1000,1000000000000000)
    URL: Final[str] = '/api/v1/enterprise'

    dto = CreateEnterpriseDTO(
        name = f'name {num}',
        description = f" description {num}",
        website_url = None,
        logo_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}/{industry_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data: Final = response.json()

    assert response.status_code == 201

    assert data['message'] == 'Enterprise created with successfully'
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['user_id'] is not None
    assert data['version'] == 1
    assert data['path'] is None

    return EnterpriseOUT(
        id = data['body']['id'],
        name = data['body']['name'],
        description = data['body']['description'],
        website_url = data['body']['website_url'],
        logo_url = data['body']['logo_url'],
        user_id = data['body']['user_id'],
        industry_id = data['body']['industry_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_industry(user_data: UserTestData):
    URL: Final[str] = '/api/v1/industry'
    num: Final = random.randint(1000,10000000000000)

    dto: Final = CreateIndustryDTO(
        name = f"name {num}",
        description = None,
        icon_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 201

    data: Final = response.json()        

    assert data['message'] == "Industry created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert isinstance(data['body']['id'], int)
    assert data['body']['name'] == dto.name
    assert data['body']['description'] == dto.description
    assert data['body']['icon_url'] == dto.icon_url
    assert data['body']['user_id'] is not None
    assert isinstance(data['body']['user_id'], int)
    assert data['body']['is_active'] == True

    return IndustryOUT(
        id = data['body']['id'],
        name = data['body']['name'],
        description = data['body']['description'],
        icon_url = data['body']['icon_url'],
        is_active = data['body']['is_active'],
        usage_count = data['body']['usage_count'],
        user_id = data['body']['user_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_post_user(user_data: UserTestData, category_data: CategoryOUT):
    num = random.randint(10000,100000000000)
    URL: Final[str] = "/api/v1/post-user"

    dto = CreatePostUserDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(f"{URL}/{category_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Post created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['title'] == dto.title
    assert data['body']['content'] == dto.content
    assert data['body']['url_image'] == dto.url_image
    assert data['body']['category_id'] == category_data.id

    return PostUserOUT(
        id = data['body']['id'],
        title = data['body']['title'],
        content = data['body']['content'],
        url_image = data['body']['url_image'],
        user_id = data['body']['user_id'],
        category_id = data['body']['category_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_category(user_data: UserTestData):
    num = random.randint(100000,10000000000000)

    dto = CreateCategoryDTO(
        name = f"name {num}",
        slug = f"slug {num}",
        description = None,
        order = 5,
        icon_url = None
    )

    token = user_data.tokens.token

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/category", json=dict(dto), headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201

    data = response.json()

    assert data['code'] == 201
    assert data['message'] == 'Category created with successfully'
    assert data['status'] == True
    assert data['version'] == 1
    assert data['path'] is None

    assert data['body']['id'] is not None
    assert data['body']['name'] == dto.name
    assert data['body']['slug'] == dto.slug
    assert data['body']['description'] == dto.description
    assert data['body']['order'] == dto.order
    assert data['body']['icon_url'] == dto.icon_url
    assert data['body']['is_active'] == True
    assert data['body']['user_id'] is not None
    assert data['body']['created_at'] is not None

    return CategoryOUT(
        id = data['body']['id'],
        name = data['body']['name'],
        slug = data['body']['slug'],
        description = data['body']['description'],
        is_active = data['body']['is_active'],
        order = data['body']['order'],
        post_count = data['body']['post_count'],
        job_count = data['body']['job_count'],
        icon_url = data['body']['icon_url'],
        user_id = data['body']['user_id'],
        parent_id = data['body']['parent_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_and_login_user() -> UserTestData:
    num = random.randint(100000, 100000000000000)
    dto = CreateUserDTO(
        name=f"user {num}",
        email=f"user{num}@example.com",
        password=str(num),
        bio=None,
        avatar_url=None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json=dto.model_dump())
    assert response.status_code == 201

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_dto = LoginDTO(email=dto.email, password=dto.password)
        response = await ac.post("/api/v1/auth/login", json=login_dto.model_dump())
    assert response.status_code == 200

    data = response.json()["body"]

    assert data["token"] is not None
    assert data["refresh_token"] is not None

    tokens = Tokens(
        token=data["token"],
        refresh_token=data["refresh_token"],
        exp_token=data.get("exp_token"),
        exp_refresh_token=data.get("exp_refresh_token"),
    )

    return UserTestData(dto=dto, tokens=tokens)
