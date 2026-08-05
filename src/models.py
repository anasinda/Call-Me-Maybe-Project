from pydantic import BaseModel


class Parameter(BaseModel):
    type: str


class FunctionDefenition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Parameter]
    returns: Parameter

class PromptGetter(BaseModel):
    prompt: str



