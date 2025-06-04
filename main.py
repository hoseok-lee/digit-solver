from collections import defaultdict
from typing import Generator
from itertools import product
from sympy import Symbol, UnevaluatedExpr
import operator


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


    def solve(self, t: int) -> Generator[str]:

        # Dynamic programming
        [ _ for _ in self.expand_recurse(symbol_map = self.symbol_map) ]
        for solution in self.ptable[self.symbol_map.symbols][t]:
            yield solution


    def store(self, symbols, exp):

        # Substitute expression for unevaluated integers
        # Evaluate it once storing in ptable
        val = exp.subs(self.symbol_map.items())
        self.ptable[symbols][val.doit()].add(exp)
        return val, exp


    def expand_recurse(
        self,
        symbol_map: SymbolMap
    ) -> Generator[int]:

        if symbol_map.symbols in self.ptable.keys():
            for val, exps in self.ptable[symbol_map.symbols].items():
                for exp in exps:
                    yield val, exp

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

                for l_exp, r_exp in product(
                    self.expand_recurse(lhs),
                    self.expand_recurse(rhs)
                ):

                    for ex in Solution.ops:

                        try:
                            yield self.store(
                                symbol_map.symbols,
                                ex(l_exp[1], r_exp[1])
                            )

                        except ZeroDivisionError:
                            pass


solution = Solution(n = 5443)
print(list(solution.solve(0)))

# A = ['5 * ((4 - 4) * 3 / 4)', '5 * (4 - 4) * 3 / 4']
# A = ['5 - (4 - 6 * (3 - 5))']

# for exp in A:

#     print(Simplifier(exp).simplify())