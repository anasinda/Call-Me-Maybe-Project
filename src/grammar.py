from schema import FunctionDefenition, Parameter
from enum import Enum, auto

class State(Enum):
    START = auto()
    EXPECT_KEY = auto()
    EXPECT_COLON = auto()
    EXPECT_FUNCTION_NAME = auto()
    EXPECT_PARAMETERS_KEY = auto()
    EXPECT_PARAMETERS_NAME = auto()
    EXPECT_PARAMETERS_VALUE = auto()
    EXPECT_NEXT_PARAMETERS_OR_END = auto()


class Grammar():
    def __init__(self, functions: dict[str, FunctionDefenition]):
        self.functions = functions
        self.current_state = State.START
        self.current_function = None
        self.current_parameter = None
        self.generated_params = set()

    def get_allowed_tokens(self):
        check_basic_state = {
            State.START: "{",
            State.EXPECT_KEY: "name",
            State.EXPECT_COLON: ":"
        }

        # if self.current_state in check_state:
        #     return check_basic_state[self.current_state]
        # elif self.current_state == State.EXPECT_FUNCTION_NAME:

