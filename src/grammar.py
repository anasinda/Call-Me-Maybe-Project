from dataclasses import dataclass
from models import FunctionDefenition
from utils import State

@dataclass
class Allowed():
    literal: str | None = None
    choices: set[str] | None = None
    usable_funcs: set[str] | None = None
    value_type: str | None = None

    def check_value_type(self):
        if self.literal is not None:
            return [self.literal]

        if self.value_type is not None:
            return [self.value_type]

        if self.choices is not None:
            return self.choices

        if self.usable_funcs is not None:
            return self.usable_funcs

        raise RuntimeError("Allowed is empty...")



class Grammar:
    def __init__(self, functions: dict[str, FunctionDefenition]):
        self.functions = functions
        self.current_state = State.START
        self.current_function: str | None = None
        self.current_parameter: str | None = None
        self.available_params: set[str] = set()
        self.generated_params: set[str] = set()

    def get_allowed_tokens(self) -> Allowed:
        basic = {
            State.START: "{",
            State.EXPECT_KEY: "name",
            State.EXPECT_COLON: ":",
            State.EXPECT_KEY_COMMA: ",",
            State.EXPECT_PARAMETERS_KEY: "parameters",
            State.EXPECT_PARAMETERS_COLON: ":",
            State.EXPECT_PARAMETERS_L_BRACE: "{",
            State.EXPECT_PARAMETERS_NAME_COLON: ":",
            State.EXPECT_PARAMETERS_COMMA: ",",
            State.EXPECT_PARAMETERS_R_BRACE: "}",
            State.EXPECT_OBJECT_R_BRACE: "}",
            State.END: None,
        }

        if self.current_state in basic:
            allowed_literal = Allowed(literal=basic[self.current_state])
            return allowed_literal

        if self.current_state == State.EXPECT_FUNCTION_NAME:
            allowed_funcs = Allowed(usable_funcs=set(self.functions))
            return allowed_funcs

        if self.current_state == State.EXPECT_PARAMETERS_NAME:
            allowed_choices = Allowed(choices=(self.available_params - self.generated_params))
            return allowed_choices

        if self.current_state == State.EXPECT_PARAMETERS_VALUE:
            assert self.current_function is not None
            assert self.current_parameter is not None

            allowed_type = Allowed(value_type=self.functions[self.current_function].parameters[self.current_parameter].type)
            return allowed_type

        raise RuntimeError(f"Unhandled state {self.current_state}")

    def consume(self, token: str):
        allowed = self.get_allowed_tokens()

        if allowed.literal is not None:
            assert token == allowed.literal

        elif allowed.choices is not None:
            assert token in allowed.choices

        elif allowed.usable_funcs is not None:
            assert token in allowed.usable_funcs

        elif allowed.value_type is not None:
            if allowed.value_type == "number":
                # TODO: validate number
                pass
            elif allowed.value_type == "string":
                # TODO: validate string
                pass
            else:
                raise AssertionError(f"Unknown type {allowed.value_type}")

        if self.current_state == State.EXPECT_FUNCTION_NAME:
            self.current_function = token
            self.available_params = set(
                self.functions[token].parameters.keys()
            )

        elif self.current_state == State.EXPECT_PARAMETERS_NAME:
            self.current_parameter = token
            self.generated_params.add(token)

        if self.current_state == State.EXPECT_PARAMETERS_VALUE:
            remaining = self.available_params - self.generated_params

            if remaining:
                self.current_state = State.EXPECT_PARAMETERS_COMMA
            else:
                self.current_state = State.EXPECT_PARAMETERS_R_BRACE
            return

        transitions = {
            State.START: State.EXPECT_KEY,
            State.EXPECT_KEY: State.EXPECT_COLON,
            State.EXPECT_COLON: State.EXPECT_FUNCTION_NAME,
            State.EXPECT_FUNCTION_NAME: State.EXPECT_KEY_COMMA,
            State.EXPECT_KEY_COMMA: State.EXPECT_PARAMETERS_KEY,
            State.EXPECT_PARAMETERS_KEY: State.EXPECT_PARAMETERS_COLON,
            State.EXPECT_PARAMETERS_COLON: State.EXPECT_PARAMETERS_L_BRACE,
            State.EXPECT_PARAMETERS_L_BRACE: State.EXPECT_PARAMETERS_NAME,
            State.EXPECT_PARAMETERS_NAME: State.EXPECT_PARAMETERS_NAME_COLON,
            State.EXPECT_PARAMETERS_NAME_COLON: State.EXPECT_PARAMETERS_VALUE,
            State.EXPECT_PARAMETERS_COMMA: State.EXPECT_PARAMETERS_NAME,
            State.EXPECT_PARAMETERS_R_BRACE: State.EXPECT_OBJECT_R_BRACE,
            State.EXPECT_OBJECT_R_BRACE: State.END,
        }

        self.current_state = transitions[self.current_state]

    def reset(self):
        self.current_state = State.START
        self.current_function = None
        self.current_parameter = None
        self.available_params.clear()
        self.generated_params.clear()
