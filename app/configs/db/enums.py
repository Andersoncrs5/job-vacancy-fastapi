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
