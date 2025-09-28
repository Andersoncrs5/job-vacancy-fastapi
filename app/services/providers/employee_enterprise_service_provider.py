from app.services.base.employee_enterprise_service_base import EmployeeEnterpriseServiceBase
from app.repositories.providers.employee_enterprise_repository_provider import EmployeeEnterpriseRepositoryProvider

class EmployeeEnterpriseServiceProvider(EmployeeEnterpriseServiceBase):
    def __init__(self, repository: EmployeeEnterpriseRepositoryProvider):
        self.repository = repository    

    