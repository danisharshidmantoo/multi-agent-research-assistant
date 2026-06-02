class AppError(Exception):
    """Base application exception."""


class ConfigurationError(AppError):
    """Raised when required configuration is invalid or missing."""


class GeminiServiceError(AppError):
    """Raised when Gemini API calls fail."""


class AgentExecutionError(AppError):
    """Raised when any agent fails during workflow execution."""

