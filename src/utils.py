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
    EXPECT_OBJECT_R_BRACE = auto()
    END = auto()
