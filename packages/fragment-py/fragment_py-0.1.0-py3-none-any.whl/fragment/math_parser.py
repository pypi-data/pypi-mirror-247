import ast
import operator as op
from typing import Any, Callable, Dict, Type

# Separate dictionaries for binary and unary operators
binary_operators: Dict[Type[ast.operator], Callable[[Any, Any], Any]] = {
    ast.Add: op.add,
    ast.Sub: op.sub,
}

unary_operators: Dict[Type[ast.unaryop], Callable[[Any], Any]] = {
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def eval_expr(expr: str) -> Any:
    return eval_(ast.parse(expr.strip(), mode="eval").body)


def eval_(node: ast.BinOp | ast.Num | ast.UnaryOp | Any) -> Any:
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return binary_operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return unary_operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)
