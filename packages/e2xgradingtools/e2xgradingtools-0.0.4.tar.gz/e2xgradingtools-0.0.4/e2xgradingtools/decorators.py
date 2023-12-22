import ast
import functools
import inspect
from textwrap import dedent


class CatchAllAssertErrors(ast.NodeTransformer):
    def __init__(self, source):
        self.source = source.split("\n")
        self.n_asserts = 0

    def visit_Assert(self, node):
        """Wrap assert statements in try except blocks that print the error message"""
        self.n_asserts += 1
        self.generic_visit(node)

        try_except_block = ast.Try(
            body=[
                ast.With(
                    items=[
                        ast.withitem(
                            context_expr=ast.Call(
                                func=ast.Name(id="HiddenPrints", ctx=ast.Load()),
                                args=[],
                                keywords=[],
                            )
                        )
                    ],
                    body=[
                        node,
                        ast.AugAssign(
                            target=ast.Name(id="e2x_n_passed", ctx=ast.Store()),
                            op=ast.Add(),
                            value=ast.Constant(value=1),
                        ),
                    ],
                )
            ],
            handlers=[
                ast.ExceptHandler(
                    type=ast.Name(id="Exception", ctx=ast.Load()),
                    name="e",
                    body=[
                        ast.AugAssign(
                            target=ast.Name(id="e2x_n_failed", ctx=ast.Store()),
                            op=ast.Add(),
                            value=ast.Constant(value=1),
                        ),
                        *ast.parse(
                            dedent(
                                f"""
                    print("!--> " + e.__class__.__name__ + ": " + str(e))
                    print("     Line {node.lineno}: " + '''{self.source[node.lineno-1].strip()}''')
                    print("<--!")
                    print()
                    """
                            )
                        ).body,
                    ],
                )
            ],
            orelse=[],
            finalbody=[],
            lineno=node.lineno,
            col_offset=node.col_offset,
        )

        return try_except_block


def test_asserts(points):
    """Decorator for test functions with asserts

    Args:
        points (int): The number of points for the test
    """

    def catch_all_asserts(method):
        """Function decorator that wraps all asserts in try except statements"""
        source_code = inspect.getsource(method)
        tree = ast.parse(source_code)
        transformer = CatchAllAssertErrors(source_code)
        updated = transformer.visit(tree)

        n_passed = "e2x_n_passed"
        n_failed = "e2x_n_failed"

        updated.body[0].body.insert(
            0,
            ast.ImportFrom(
                module="e2xgradingtools.utils",
                names=[ast.alias(name="HiddenPrints", asname=None)],
                level=0,
            ),
        )
        updated.body[0].body.insert(0, ast.parse(f"{n_passed} = 0").body[0])
        updated.body[0].body.insert(0, ast.parse(f"{n_failed} = 0").body[0])
        updated.body[0].body.insert(
            0, ast.parse("from e2xgradingtools import grade_report").body[0]
        )

        updated.body[0].body.append(
            ast.parse(
                f"print(str({n_passed}) + ' / ' + str({n_passed} + {n_failed}) + ' tests passed' )"
            ).body[0]
        )
        updated.body[0].body.append(ast.parse("print()").body[0])

        if transformer.n_asserts > 0:
            updated.body[0].body.append(
                ast.parse(
                    f"grade_report({n_passed}/({n_passed} + {n_failed}), {points})"
                ).body[0]
            )
        else:
            updated.body[0].body.append(ast.parse(f"grade_report(0, {points})").body[0])

        updated = ast.increment_lineno(
            ast.fix_missing_locations(updated), method.__code__.co_firstlineno
        )

        ast.copy_location(updated.body[0], tree)
        code = compile(tree, inspect.getfile(method), "exec")
        namespace = method.__globals__
        exec(code, namespace)
        new_function = namespace[method.__name__]

        method = functools.update_wrapper(new_function, method)

        def inner(*args, **kwargs):
            return method(*args, **kwargs)

        return inner

    return catch_all_asserts
