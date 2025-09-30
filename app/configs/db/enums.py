import enum
from sqlalchemy import Enum

class MediaType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    GIF = "gif"
    PDF = "pdf"
    TEXT = "text"
    ARCHIVE = "archive"

class ProficiencyEnum(str, enum.Enum):
    basic = "Basic"
    intermediary = "Intermediary"
    proficient = "Proficient"
    specialist = "Specialist"

class EmploymentTypeEnum(str, enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    internship = "internship"
    contract = "contract"
    temporary = "temporary"
    freelance = "freelance"
    apprentice = "apprentice"
    seasonal = "seasonal" 

class EmploymentStatusEnum(str, enum.Enum):
    current_employee = "current_employee"
    former_employee = "former_employee"
    on_leave = "on_leave"   
    vacation = "vacation"   
    probation = "probation" 

class ExperienceLevelEnum(str, enum.Enum):
    INTERN = "Internship"
    JUNIOR = "Junior"
    PLENO = "Pleno"
    SENIOR = "Senior"
    LEAD = "Lead"

class EducationLevelEnum(str, enum.Enum):
    NONE = "None"
    HIGH_SCHOOL = "HighSchool"
    TECHNICAL = "Technical"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"

class VacancyStatusEnum(str, enum.Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    PAUSED = "Paused"

class CurrencyEnum(str, enum.Enum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
    BTC = "BTC"
