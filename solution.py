from collections import defaultdict
from typing import Generator, Optional
from itertools import product
from sympy import Symbol, UnevaluatedExpr, oo, zoo, nan
import operator
import matplotlib.pyplot as plt


class SymbolMap:

    def __init__(self, data: list[int] | dict):

        # List of digits to map to symbols
        if isinstance(data, list):
            self.symbol_map = {
                Symbol(f'd{i}'): UnevaluatedExpr(digit)
                for i, digit in enumerate(data)
            }

        else:
            # Provided symbol map directly
            self.symbol_map = data


    @property
    def symbols(self) -> tuple:
        return tuple(self.symbol_map.keys())


    @property
    def digits(self) -> tuple:
        return tuple(self.symbol_map.values())

    def items(self) -> list:
        return self.symbol_map.items()


    def __len__(self) -> int:
        return len(self.symbol_map)


    def __getitem__(self, key) -> int:

        # When sliced, must return iterated map
        return SymbolMap(
            data = {
                symbol: self.symbol_map[symbol]
                for symbol in self.symbols[key]
            }
        )


    def __str__(self) -> str:
        return str(self.symbol_map)


class Solution:

    ops = [
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv
    ]


    def __init__(self, n: int):

        self.symbol_map = SymbolMap(data = list(map(int, str(n))))
        self.ptable = defaultdict(lambda: defaultdict(set))


    def solve(self, t: Optional[int] = None) -> Generator[str] | defaultdict:

        def replacement(expr, symbol_map):
            for key, val in symbol_map.items():
                expr = expr.replace(str(key), str(val))

            return expr


        # Dynamic programming
        [ _ for _ in self.expand_recurse(symbol_map = self.symbol_map) ]
        if t is not None:
            for solution in self.ptable[self.symbol_map.symbols][t]:
                yield replacement(str(solution), self.symbol_map)

        else:
            # Return distribution
            yield {
                key: len(val)
                for key, val in self.ptable[self.symbol_map.symbols].items()
            }


    def store(self, symbols, expr):

        # Substitute expression for unevaluated integers
        # Evaluate it once storing in ptable
        val = expr.subs(self.symbol_map.items()).doit()
        if val.has(oo, -oo, zoo, nan):
            raise ZeroDivisionError
        self.ptable[symbols][val.doit()].add(expr)
        return val, expr


    def expand_recurse(
        self,
        symbol_map: SymbolMap
    ) -> Generator[int]:

        if symbol_map.symbols in self.ptable.keys():
            for val, exprs in self.ptable[symbol_map.symbols].items():
                for expr in exprs:
                    yield val, expr

            return

        # Base case
        if len(symbol_map) == 1:

            yield self.store(
                symbol_map.symbols,
                symbol_map.symbols[0]
            )

        else:

            for i in range(len(symbol_map) - 1):

                lhs = symbol_map[:i + 1]
                rhs = symbol_map[i + 1:]

                for l_expr, r_expr in product(
                    self.expand_recurse(lhs),
                    self.expand_recurse(rhs)
                ):

                    for ex in Solution.ops:

                        try:
                            yield self.store(
                                symbol_map.symbols,
                                ex(l_expr[1], r_expr[1])
                            )

                        except ZeroDivisionError:
                            pass


# Parse arguments
if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("n", help="number for digit-based arithematic combination", type=int)
    parser.add_argument("t", nargs="?", help="target result for computation; if empty, plot distribution of solutions", type=int)
    args = parser.parse_args()

    solution = Solution(n = args.n)
    solutions = list(solution.solve(args.t))

    if solutions == []:
        print(f"No solutions found for n = {args.n}, t = {args.t}.")

    else:
        # Distribution found
        if isinstance(solutions[0], dict):
            formatted = [ int(k) for k, v in solutions[0].items() for _ in range(v) ]
            plt.hist(formatted)
            plt.savefig("dist.pdf")

        else:
            for i, expression in enumerate(solutions):
                print(f"Solution {i + 1}: {expression}")