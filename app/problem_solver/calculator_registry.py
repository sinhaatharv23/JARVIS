import ast
import math
import operator

from types import MappingProxyType

# ==========================================================
# Immutable Binary Operators
# ==========================================================

BINARY_OPERATORS = MappingProxyType({
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
})

# ==========================================================
# Immutable Unary Operators
# ==========================================================

UNARY_OPERATORS = MappingProxyType({
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
})

# ==========================================================
# Immutable Supported Functions
# ==========================================================

FUNCTIONS = MappingProxyType({

    "sqrt": math.sqrt,

    # Future Expansion
    # "sin": math.sin,
    # "cos": math.cos,
    # "tan": math.tan,
    # "asin": math.asin,
    # "acos": math.acos,
    # "atan": math.atan,
    # "log": math.log,
    # "log10": math.log10,
    # "factorial": math.factorial,
    # "ceil": math.ceil,
    # "floor": math.floor,
    # "abs": abs,
})

# ==========================================================
# Immutable Constants
# ==========================================================

CONSTANTS = MappingProxyType({

    # Future Expansion
    # "pi": math.pi,
    # "e": math.e,

})