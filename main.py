from collections import defaultdict
from typing import Generator
from itertools import product


class Solution:

    ops = [ '+', '-', '*', '/' ]

    def __init__(self, n: int):

        self.digits = tuple(map(int, str(n)))
        self.ptable = defaultdict(lambda: defaultdict(set))


    def solve(self, t: int) -> Generator[str]:

        # Dynamic programming
        [ _ for _ in self.expand_recurse(available_digits = self.digits) ]
        return self.ptable[self.digits][t]


    def store(self, digits, exp):

        val = eval(exp)
        # Add reduced expression to set
        self.ptable[digits][val].add(Solution.reduce_exp(exp))
        return val, exp


    def expand_recurse(
        self,
        available_digits: tuple
    ) -> Generator[int]:

        if available_digits in self.ptable.keys():
            for val, exps in self.ptable[available_digits].items():
                for exp in exps:
                    yield val, exp

            return

        # Base case
        if len(available_digits) == 1:

            yield self.store(
                available_digits,
                str(available_digits[0])
            )

        else:

            for i in range(len(available_digits) - 1):

                lhs = tuple(available_digits[:i + 1])
                rhs = tuple(available_digits[i + 1:])

                for l_exp, r_exp in product(
                    self.expand_recurse(lhs),
                    self.expand_recurse(rhs)
                ):

                    for ex in Solution.ops:

                        try:
                            yield self.store(
                                available_digits,
                                f"({l_exp[1]}) {ex} ({r_exp[1]})"
                            )

                        except:
                            pass


    def reduce_exp(exp):

        # TODO: find a way to reduce mathematical expression to least amount of brackets

        return exp


solution = Solution(n = 5443)
print(solution.solve(10))