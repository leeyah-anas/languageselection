from enum import Enum

class NativeLanguage(str, Enum):
    ENGLISH = "English"
    HAUSA = "Hausa"
    IGBO = "Igbo"
    YORUBA = "Yoruba"
    SWAHILI = "Swahili"
    ZULU = "Zulu"

class SupportedLanguage(str, Enum):
    HAUSA = "Hausa"

class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"