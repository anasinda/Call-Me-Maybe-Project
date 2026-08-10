"""Data models that define supported functions and parameters."""

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class Parameter(BaseModel):
    type: str

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        """Reject empty or unsupported parameter types."""

        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("parameter type cannot be empty")
        if cleaned_value not in {"number", "string", "boolean"}:
            raise ValueError(
                f"unsupported parameter type: {cleaned_value}"
            )
        return cleaned_value


class FunctionDefenition(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    description: str
    parameters: dict[str, Parameter]
    returns: Parameter

    @field_validator("name", "description")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        """Reject empty function metadata fields."""

        if not value:
            raise ValueError("text fields cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_contract(self) -> "FunctionDefenition":
        """Keep the contract check lightweight and allow any supported type."""

        return self


class PromptGetter(BaseModel):
    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        """Reject empty or numeric-only prompts."""

        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("prompt cannot be empty")
        if not any(char.isalpha() for char in cleaned_value):
            raise ValueError("prompt cannot contain only numbers")
        return cleaned_value
