from schema import FunctionDefenition, Parameter
from enum import Enum, auto

class State(Enum):
    START = auto()
    EXPECT_KEY = auto()
    EXPECT_COLON = auto()
    EXPECT_FUNCTION_NAME = auto()
    EXPECT_KEY_COMMA = auto()
    EXPECT_PARAMETERS_KEY = auto()
    EXPECT_PARAMETERS_COLON = auto()
    EXPECT_PARAMETERS_L_BRACE = auto()
    EXPECT_PARAMETERS_NAME = auto()
    EXPECT_PARAMETERS_NAME_COLON = auto()
    EXPECT_PARAMETERS_VALUE = auto()
    EXPECT_PARAMETERS_COMMA = auto()
    EXPECT_PARAMETERS_R_BRACE = auto()
    EXPECT_NEXT_PARAMETERS_OR_END = auto()
    EXPECT_OBJECT_R_BRACE = auto()
    END = auto()


class Grammar():
    def __init__(self, functions: dict[str, FunctionDefenition]):
        self.functions: dict[str, FunctionDefenition] = functions
        self.current_state: State = State.START
        self.current_function: str | None = None
        self.current_parameter: str | None = None
        self.generated_params: set[str] = set()

    def get_allowed_tokens(self) -> str | set[str] | None:
        check_basic_state: dict[State, str] = {
            State.START: "{",
            State.EXPECT_KEY: "name",
            State.EXPECT_COLON: ":",
            State.EXPECT_KEY_COMMA: ",",
            State.EXPECT_PARAMETERS_KEY: "parameters",
            State.EXPECT_PARAMETERS_COLON: ":",
            State.EXPECT_PARAMETERS_L_BRACE: "{",
            State.EXPECT_PARAMETERS_COMMA: ",",
            State.EXPECT_PARAMETERS_NAME_COLON: ":",
            State.EXPECT_PARAMETERS_R_BRACE: "}",
            State.EXPECT_OBJECT_R_BRACE: "}"
        }


        if self.current_state in check_basic_state:
            return check_basic_state[self.current_state]

        if self.current_state == State.EXPECT_FUNCTION_NAME:
            return set(self.functions)

        if self.current_state == State.EXPECT_PARAMETERS_NAME:
            assert self.current_function is not None

            param_name: set[str] = set(self.functions[self.current_function].parameters)
            return param_name - self.generated_params

        if self.current_state == State.EXPECT_PARAMETERS_VALUE:
            assert self.current_parameter is not None
            assert self.current_function is not None

            param_value = self.functions[self.current_function].parameters[self.current_parameter]
            return param_value.type

        if self.current_state == State.EXPECT_NEXT_PARAMETERS_OR_END:
            assert self.current_function is not None

            func_obj: FunctionDefenition = self.functions[self.current_function]
            remaining = set(func_obj.parameters) - self.generated_params

            if remaining:
                return check_basic_state[State.EXPECT_PARAMETERS_COMMA]
            else:
                return check_basic_state[State.EXPECT_PARAMETERS_R_BRACE]

        if self.current_state == State.EXPECT_OBJECT_R_BRACE:
            return check_basic_state[State.EXPECT_OBJECT_R_BRACE]

        if self.current_state == State.END:
            return None
        raise RuntimeError(f"Unhandled state: {self.current_state}")




