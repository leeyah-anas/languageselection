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

class LearningReason(str, Enum):
    TRAVEL = "travel"
    CAREER = "career"
    CULTURE = "culture"
    OTHER = "other"

class DailyLearningGoal(str, Enum):
    CASUAL = "5 minutes daily"
    REGULAR = "10 minutes daily"
    SERIOUS = "20 minutes daily"
    INTENSIVE = "30 minutes daily"