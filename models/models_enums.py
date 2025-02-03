import enum


class RatingEnum(int, enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


class LanguageEnum(str, enum.Enum):
    RUS = 'Русский'
    ENG = 'Английский'


class MediaTypeEnum(str, enum.Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
