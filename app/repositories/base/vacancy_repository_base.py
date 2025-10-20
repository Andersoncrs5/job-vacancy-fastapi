from abc import ABC, abstractmethod
from app.configs.db.database import VacancyEntity
from app.utils.filter.vacancy_filter import VacancyFilter
from typing import List

class VacancyRepositoryBase(ABC):
    pass