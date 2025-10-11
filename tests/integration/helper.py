import random
from datetime import date
from typing import Final

from httpx import ASGITransport, AsyncClient

from app.configs.db.enums import (
    MediaType, ProficiencyEnum, ReactionTypeEnum
)
from app.schemas.address_enterprise_schemas import CreateAddressEnterpriseDTO, AddressEnterpriseOUT
from app.schemas.address_user_schemas import *
from app.schemas.application_schemas import ApplicationOUT
from app.schemas.area_schemas import *
from app.schemas.category_schemas import *
from app.schemas.comment_post_enterprise_schemas import CreateCommentPostEnterpriseDTO, CommentPostEnterpriseOUT
from app.schemas.comment_post_user_schemas import CreateCommentPostUserDTO, CommentPostUserOUT
from app.schemas.curriculum_schemas import *
from app.schemas.employee_enterprise_schemas import *
from app.schemas.enterprise_schemas import *
from app.schemas.industry_schemas import *
from app.schemas.media_post_user_schemas import CreateMediaPostUserDTO, MediaPostUserOUT
from app.schemas.my_skill_schemas import *
from app.schemas.post_enterprise_schemas import CreatePostEnterpriseDTO, PostEnterpriseOUT
from app.schemas.post_user_schemas import CreatePostUserDTO, PostUserOUT
from app.schemas.reaction_comment_post_enterprise_schemas import CreateReactionCommentPostEnterpriseDTO
from app.schemas.reaction_comment_post_user_schemas import CreateReactionCommentPostUserDTO
from app.schemas.reaction_post_enterprise_schemas import CreateReactionPostEnterpriseDTO
from app.schemas.reaction_post_user_schemas import CreateReactionPostUserDTO
from app.schemas.review_enterprise_schemas import *
from app.schemas.saved_search_schemas import CreateSavedSearchDTO, SavedSearchOUT
from app.schemas.skill_schemas import *
from app.schemas.user_schemas import CreateUserDTO, LoginDTO, UserOUT
from app.schemas.vacancy_schemas import *
from app.schemas.vacancy_skill_schemas import CreateVacancySkillDTO
from app.utils.res.tokens import Tokens
from main import app

class UserTestData(BaseModel):
    dto: CreateUserDTO
    tokens: Tokens
    out: UserOUT

async def create_react_comment_post_enterprise(user_data: UserTestData, comment_data: CommentPostEnterpriseOUT, reaction_type: ReactionTypeEnum):
    URL = "/api/v1/area/reaction-comment-enterprise"

    dto = CreateReactionCommentPostEnterpriseDTO(
        comment_enterprise_id=comment_data.id,
        reaction_type=reaction_type
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['code'] == 201

    assert body is None

async def create_react_comment_post_user(user_data_two: UserTestData, comment_data: CommentPostUserOUT, reaction_type: ReactionTypeEnum):
    URL = "/api/v1/area/reaction-comment-user"

    dto = CreateReactionCommentPostUserDTO(
        comment_user_id=comment_data.id,
        reaction_type=reaction_type
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['code'] == 201

    assert body is None

async def create_favorite_comment_user(user_data, comment_data):
    URL = "/api/v1/favorite-comment-post-user"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}/toggle-favorite/{comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )
    assert response.status_code == 201

async def create_favorite_comment(user_data: UserTestData, comment_data: CommentPostUserOUT):
    URL = "/api/v1/favorite-comment-post-enterprise"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}/toggle-favorite/{comment_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201

async def create_comment_enterprise_user(user_data: UserTestData, post_data: PostEnterpriseOUT):
    URL: Final[str] = "/api/v1/comment-post-enterprise"

    dto = CreateCommentPostEnterpriseDTO(
        content=("abc" * 50),
        post_enterprise_id=post_data.id,
        parent_comment_id=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 201
    assert data['message'] == 'Comment created with successfully'
    assert data['status'] == True

    assert body['id'] is not None
    assert isinstance(body['id'], int)
    assert body['user_id'] == user_data.out.id
    assert body['post_enterprise_id'] == post_data.id

    assert body['user']['id'] == user_data.out.id
    assert body['post']['id'] == post_data.id

    user = UserOUT(
        id=body['user']['id'],
        name=body['user']['name'],
        email=body['user']['email'],
        bio=body['user'].get('bio', None),
        avatar_url=body['user'].get('avatar_url', None),
        created_at=body['user']['created_at'],
    )

    post_dict = body['post']
    post = PostEnterpriseOUT(
        id=post_dict['id'],
        title=post_dict['title'],
        content=post_dict['content'],

        url_image=post_dict.get('url_image', None),

        enterprise_id=post_dict['enterprise_id'],
        category_id=post_dict['category_id'],
        created_at=post_dict['created_at'],
        updated_at=post_dict['updated_at'],
    )

    return CommentPostEnterpriseOUT(
        id = body['id'],
        content = body['content'],
        user_id = body['user_id'],
        post_enterprise_id = body.get('post_enterprise_id'),
        parent_comment_id= body.get('parent_comment_id', None),
        is_edited = body['is_edited'],
        created_at = body['created_at'],
        updated_at = body['updated_at'],
        user = user,
        post = post,
    )

async def create_comment_post_user(user_data: UserTestData, post_user_data: PostUserOUT):
    URL: Final[str] = "/api/v1/comment-post-user"

    dto = CreateCommentPostUserDTO(
        content=("abc" * 50),
        post_user_id=post_user_data.id,
        parent_comment_id=None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201

    data = response.json()
    body = response.json()['body']

    assert data['code'] == 201
    assert data['message'] == 'Comment created with successfully'
    assert data['status'] == True

    assert body['id'] is not None
    assert isinstance(body['id'], int)
    assert body['user_id'] == user_data.out.id
    assert body['post_user_id'] == post_user_data.id

    assert body['user']['id'] == user_data.out.id
    assert body['post']['id'] == post_user_data.id

    user = UserOUT(
        id=body['user']['id'],
        name=body['user']['name'],
        email=body['user']['email'],
        bio=body['user'].get('bio', None),
        avatar_url=body['user'].get('avatar_url', None),
        created_at=body['user']['created_at'],
    )

    post_dict = body['post']
    post = PostUserOUT(
        id=post_dict['id'],
        title=post_dict['title'],
        content=post_dict['content'],

        url_image=post_dict.get('url_image', None),

        user_id=post_dict['user_id'],
        category_id=post_dict['category_id'],
        created_at=post_dict['created_at'],
        updated_at=post_dict['updated_at'],
    )

    return CommentPostUserOUT(
        id = body['id'],
        content = body['content'],
        user_id = body['user_id'],
        post_user_id = body.get('post_user_id'),
        parent_comment_id= body.get('parent_comment_id', None),
        is_edited = body['is_edited'],
        created_at = body['created_at'],
        updated_at = body['updated_at'],
        user = user,
        post = post,
    )

async def create_reaction_post_enterprise(user_data: UserTestData, post_data: PostEnterpriseOUT, reaction: ReactionTypeEnum):
    URL = "/api/v1/area/reaction-post-enterprise"

    dto = CreateReactionPostEnterpriseDTO(
        post_enterprise_id=post_data.id,
        reaction_type=reaction
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            URL,
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Reaction added with successfully"
    assert data["code"] == 201
    assert data["status"] is True
    assert data["body"] is None

async def create_reaction_post_user(user_data: UserTestData, post_user_data: PostUserOUT, reaction: ReactionTypeEnum):
    URL = "/api/v1/area/reaction-post-user"
    dto = CreateReactionPostUserDTO(
        post_user_id=post_user_data.id,
        reaction_type=reaction
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response: Final = await ac.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['message'] == "Reaction added with successfully"
    assert data['code'] == 201

    assert body is None

async def create_follow_enterprise(user_data, enterprise_data: EnterpriseOUT):
    URL: Final[str] = "/api/v1/follow-enterprise"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{enterprise_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201

async def create_follow_user(follower_data: UserTestData, followed_data: UserTestData):
    URL = "/api/v1/follow"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{followed_data.out.id}",
            headers={"Authorization": f"Bearer {follower_data.tokens.token}"}
        )

    assert response.status_code == 201
    data = response.json()
    body = response.json()['body']

    assert data['message'] == f"You are following the {followed_data.out.name}"

    assert body is None

async def create_application(user_data: UserTestData, vacancy_data: VacancyOUT):
    URL: Final[str] = "/api/v1/application"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response: Final = await acdc.post(
            f"{URL}/{vacancy_data.id}",
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    assert response.status_code == 201

    data = response.json()
    body = response.json()['body']

    assert data['message'] == 'Application sent successfully'
    assert data['code'] == 201
    assert data['status'] == True

    assert body['id'] is not None
    assert isinstance(body['id'], int)
    assert body['vacancy_id'] == vacancy_data.id
    assert body['user_id'] == user_data.out.id

    return ApplicationOUT(
        id = body['id'],
        user_id = body['user_id'],
        vacancy_id = body['vacancy_id'],
        status = body['status'],
        is_viewed = body['is_viewed'],
        priority_level = body['priority_level'],
        rating = body['rating'],
        feedback = body['feedback'],
        source = body['source'],
        notes = body['notes'],
        applied_at = body['applied_at'],
        updated_at = body['updated_at'],
    )

async def create_address_to_enterprise(user_data: UserTestData, enterprise_data: EnterpriseOUT) -> AddressEnterpriseOUT:
    URL = "/api/v1/address-enterprise"

    dto = CreateAddressEnterpriseDTO(
        street = "Any ST",
        number = "12",
        complement = None,
        district = None,
        city = "A",
        state = "B",
        country = "C",
        zipcode = "12345",
        address_type = AddressTypeEnum.RESIDENTIAL,
        is_default = True,
        is_public = True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            f"{URL}",
            json=dict(dto),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201

    assert data['body']['enterprise_id'] == enterprise_data.id
    assert data['body']['street'] == dto.street
    assert data['body']['number'] == dto.number
    assert data['body']['address_type'] == dto.address_type
    assert data['body']['city'] == dto.city

    return AddressEnterpriseOUT(
        enterprise_id = data['body']['enterprise_id'],
        street = data['body']['street'],
        number = data['body']['number'],
        complement = data['body']['complement'],
        district = data['body']['district'],
        city = data['body']['city'],
        state = data['body']['state'],
        country = data['body']['country'],
        zipcode = data['body']['zipcode'],
        address_type = data['body']['address_type'],
        is_default = data['body']['is_default'],
        is_public = data['body']['is_public'],
        created_at = data['body']['created_at'],
        updated_at = data['body']['updated_at'],
    )

async def create_address_user(user_data: UserTestData) -> AddressUserOUT:
    URL = "/api/v1/address-user"

    dto = CreateAddressUserDTO(
        street = "Any ST",
        number = "12",
        complement = None,
        district = None,
        city = "A",
        state = "B",
        country = "C",
        zipcode = "12345",
        address_type = AddressTypeEnum.RESIDENTIAL,
        is_default = True,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            f"{URL}", 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201

    assert data['body']['id'] is not None
    assert data['body']['user_id'] == user_data.out.id
    assert data['body']['street'] == dto.street

    return AddressUserOUT(
        id = data['body']['id'],
        user_id = data['body']['user_id'],
        street = data['body']['street'],
        number = data['body']['number'],
        complement = data['body']['complement'],
        district = data['body']['district'],
        city = data['body']['city'],
        state = data['body']['state'],
        country = data['body']['country'],
        zipcode = data['body']['zipcode'],
        address_type = data['body']['address_type'],
        is_default = data['body']['is_default'],
        created_at = data['body']['created_at'],
        updated_at = data['body']['updated_at'],
    )

async def add_skill_into_vacancy(user_data, vacancy_data, skill_data) -> int:
    URL = '/api/v1/vacancy-skill'
    
    dto = CreateVacancySkillDTO(
        vacancy_id = vacancy_data.id,
        skill_id = skill_data.id,
        is_required = True,
        proficiency = ProficiencyEnum.basic,
        years_experience = 2,
        priority_level = 3,
        notes = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            f"{URL}", 
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    body = response.json()['body']
    assert response.status_code == 201

    assert body is not None
    assert isinstance(body, int) == True

    return body

async def create_vacancy(user_data: UserTestData, area_data: AreaOUT) -> VacancyOUT:
    URL = '/api/v1/vacancy'
    dto = CreateVacancyDTO(
        area_id = area_data.id,
        title = "New vacancy",
        description = "Des of vacancy",
        employment_type = EmploymentTypeEnum.full_time,
        experience_level = ExperienceLevelEnum.INTERN,
        education_level = EducationLevelEnum.MASTER,
        workplace_type = WorkplaceTypeEnum.REMOTE,
        seniority = None,
        salary_min = None,
        salary_max = None,
        currency = "USD",
        requirements = None,
        responsibilities = None,
        benefits = None,
        status = VacancyStatusEnum.OPEN,
        openings = 1,
        application_deadline = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(URL, 
            json=dict(dto), 
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()

    assert response.status_code == 201
    assert data["message"] == "Vacancy created with successfully"
    assert data["code"] == 201
    assert data['body']['id'] is not None
    assert data['body']['area_id'] == dto.area_id
    assert data['body']['title'] == dto.title

    return VacancyOUT(
        id = data['body']['id'],
        enterprise_id = data['body']['enterprise_id'],
        area_id = data['body']['area_id'],
        title = data['body']['title'],
        description = data['body']['description'],
        employment_type = data['body']['employment_type'],
        experience_level = data['body']['experience_level'],
        education_level = data['body']['education_level'],
        workplace_type = data['body']['workplace_type'],
        seniority = data['body']['seniority'],
        salary_min = data['body']['salary_min'],
        salary_max = data['body']['salary_max'],
        currency = data['body']['currency'],
        requirements = data['body']['requirements'],
        responsibilities = data['body']['requirements'],
        benefits = data['body']['benefits'],
        status = data['body']['status'],
        openings = data['body']['openings'],
        application_deadline = data['body']['application_deadline'],
        views_count = data['body']['views_count'],
        applications_count = data['body']['applications_count'],
        last_application_at = data['body']['last_application_at'],
        created_at = data['body']['created_at'],
        updated_at = data['body']['updated_at'],
    )

async def create_area(user_data: UserTestData) -> AreaOUT:
    num = random.randint(10000,100000000000000)
    URL = '/api/v1/area'
    user_data = await create_and_login_user()

    dto = CreateAreaDTO(
        name = f"name {num}",
        description = None,
        is_active = True
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    return AreaOUT(
        id = data['body']['id'],
        name = data['body']['name'],
        description = data['body']['description'],
        is_active = data['body']['is_active'],
        user_id = data['body']['user_id'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_saved_search(user_data: UserTestData) -> SavedSearchOUT:
    URL = '/api/v1/saved-search'
    num = random.randint(10000,10000000000000)

    dto = CreateSavedSearchDTO(
        name = f"any query {num}",
        query = dict({"name__ilike": "any"}),
        description = None,
        is_public = True,
        last_executed_at = None,
        notifications_enabled = False
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            f"{URL}", json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201

    assert data['body']['id'] is not None
    assert data['body']['user_id'] == user_data.out.id
    assert data['body']['name'] == dto.name

    return SavedSearchOUT(
        id = data['body']['id'],
        user_id = data['body']['user_id'],
        name = data['body']['name'],
        query = data['body']['query'],
        description = data['body']['description'],
        is_public = data['body']['is_public'],
        last_executed_at = None if data['body']['last_executed_at'] is None else str(data['body']['last_executed_at']),
        execution_count = data['body']['execution_count'],
        notifications_enabled = data['body']['notifications_enabled'],
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_review(user_data, enterprise_data, user_data_two) -> ReviewEnterpriseOUT:
    URL = "/api/v1/review-enterprise"

    dto = CreateReviewEnterpriseDTO(
        rating=5,
        title="Great place to work",
        description="Very good company culture",
        pros="Supportive environment",
        cons="Sometimes long hours",
        would_recommend=True,
        position="SOFTWARE ENGINEER",
        salary_range="5000-8000",
        employment_type=EmploymentTypeEnum.full_time,
        employment_status=EmploymentStatusEnum.current_employee,
        enterprise_id=enterprise_data.id
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(
            URL,
            json=dto.model_dump(mode="json"),
            headers={"Authorization": f"Bearer {user_data_two.tokens.token}"}
        )

    data = response.json()
    assert response.status_code == 201
    assert data["message"] == "Review created with successfully"
    assert data["code"] == 201
    assert data["status"] is True
    assert data["body"]["id"] is not None
    assert data["body"]["enterprise_id"] == enterprise_data.id
    assert data["body"]["user_id"] == user_data_two.out.id
    assert data["body"]["rating"] == dto.rating
    assert data["body"]["title"] == dto.title
    assert data["body"]["description"] == dto.description

    return ReviewEnterpriseOUT(
        id=data["body"]["id"],
        rating=data["body"]["rating"],
        title=data["body"]["title"],
        description=data["body"]["description"],
        pros=data["body"]["pros"],
        cons=data["body"]["cons"],
        would_recommend=data["body"]["would_recommend"],
        position=data["body"]["position"],
        salary_range=data["body"]["salary_range"],
        employment_type=data["body"]["employment_type"],
        employment_status=data["body"]["employment_status"],
        helpful_votes=data["body"]["helpful_votes"],
        unhelpful_votes=data["body"]["unhelpful_votes"],
        user_id=data["body"]["user_id"],
        enterprise_id=data["body"]["enterprise_id"],
        created_at=str(data["body"]["created_at"]),
        updated_at=str(data["body"]["updated_at"]),
    )

async def create_employee(user_data: UserTestData, enterprise_data, user_data_two: UserTestData) -> EmployeeEnterpriseOUT:
    URL = "/api/v1/employee-enterprise"
    dto = CreateEmployeeEnterpriseDTO(
        user_id = user_data_two.out.id,
        position = "SOFTWARE ENGINEER",
        salary_range = "5000-8000",
        employment_type = EmploymentTypeEnum.full_time,
        employment_status = EmploymentStatusEnum.current_employee,
        start_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Employee created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']["id"] is not None
    assert data['body']["user_id"] == dto.user_id
    assert data['body']["position"] == dto.position
    assert data['body']["salary_range"] == dto.salary_range

    return EmployeeEnterpriseOUT(
        id = data['body']['id'],
        user_id = data['body']['user_id'],
        enterprise_id = data['body']['enterprise_id'],
        position = data['body']['position'],
        salary_range = data['body']['salary_range'],
        employment_type = data['body']['employment_type'],
        employment_status = data['body']['employment_status'],
        start_date = str(data['body']['start_date']),
        end_date = str(data['body']['end_date']),
        created_at = str(data['body']['created_at']),
        updated_at = str(data['body']['updated_at']),
    )

async def create_favorite_post_enterprise(user_data, post_enterprise) -> int:
    URL = '/api/v1/favorite-post-enterprise'
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"{URL}/{post_enterprise.id}", headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Post favorited with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body'] is not None

    return int(data['body'])

async def create_post_enterprise(user_data, enterprise_data, category_data) -> PostEnterpriseOUT :
    URL = "/api/v1/post-enterprise"
    num = random.randint(10000,10000000000000)

    dto = CreatePostEnterpriseDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"{URL}/{category_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

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

async def create_my_skill(user_data, skill) -> MySkillOUT:
    URL = '/api/v1/my-skill'

    dto = CreateMySkillDTO(
        skill_id = skill.id,
        proficiency = ProficiencyEnum.basic,
        certificate_url = None,
        datails = None,
        years_of_experience = 2,
        last_used_date = date.today()
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}", json=dto.model_dump(mode="json"), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

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

async def create_skill(user_data) -> SkillOUT:
    URL = '/api/v1/skill'
    num = random.randint(10000,100000000000000)

    dto = CreateSkillDTO(
        name = f"name {num}" 
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

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

async def create_curriculum(user_data) -> CurriculumOUT:
    URL = '/api/v1/curriculum'

    dto = CreateCurriculumDTO(
        title = "a little about me",
        description = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

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

async def create_media_post_user(user_data: UserTestData, post_user_data: PostUserOUT) -> MediaPostUserOUT:
    URL = '/api/v1/media-post-user'
    
    dto = CreateMediaPostUserDTO(
        url = "https://picsum.photos/200/300",
        type = MediaType.IMAGE,
        order = 1,
        caption = None,
        size = None,
        mime_type = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(f"{URL}/{post_user_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()
    assert response.status_code == 201

    assert data['message'] == "Media created with successfully"
    assert data['code'] == 201
    assert data['status'] == True
    assert data['body']['id'] is not None
    assert data['body']['post_id'] == post_user_data.id

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

async def create_favorite_post_user(user_data: UserTestData, category_data: CategoryOUT, post_data: PostUserOUT) -> int:
    URL = '/api/v1/favorite-post-user'

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

async def create_enterprise(user_data: UserTestData, industry_data: IndustryOUT) -> EnterpriseOUT:
    num = random.randint(1000,1000000000000000)
    URL = '/api/v1/enterprise'

    dto = CreateEnterpriseDTO(
        name = f'name {num}',
        description = f" description {num}",
        website_url = None,
        logo_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}/{industry_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    data = response.json()

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

async def create_industry(user_data: UserTestData) -> IndustryOUT:
    URL = '/api/v1/industry'
    num = random.randint(1000,10000000000000)

    dto = CreateIndustryDTO(
        name = f"name {num}",
        description = None,
        icon_url = None,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as acdc:
        response = await acdc.post(F"{URL}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

    assert response.status_code == 201

    data = response.json()

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

async def create_post_user(user_data: UserTestData, category_data: CategoryOUT) -> PostUserOUT:
    num = random.randint(10000,100000000000)
    URL = "/api/v1/post-user"

    dto = CreatePostUserDTO(
        title = f"title {num}",
        content = f"content {num}",
        url_image = None
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"{URL}/{category_data.id}", json=dict(dto), headers={"Authorization": f"Bearer {user_data.tokens.token}"})

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

async def create_category(user_data: UserTestData) -> CategoryOUT:
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

    URL = "/api/v1/user"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(URL + f"/{dto.email}", headers={"Authorization": f"Bearer {data["token"]}"})

    assert response.status_code == 200
    data_user = response.json()

    tokens = Tokens(
        token=data["token"],
        refresh_token=data["refresh_token"],
        exp_token=data.get("exp_token"),
        exp_refresh_token=data.get("exp_refresh_token"),
    )

    out = UserOUT(
        id = data_user['body']['id'],
        name = data_user['body']['name'],
        email = data_user['body']['email'],
        avatar_url = data_user['body']['avatar_url'],
        bio = data_user['body']['bio'],
        created_at = str(data_user['body']['created_at']),
    )

    return UserTestData(dto=dto, tokens=tokens, out=out)
