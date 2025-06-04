# Problem Formulation

Given an integer *n* with *m* digits, find every possible non-redundant way to produce some total *t* through arithematic combinations (with parantheses) of the *m* digits, while preserving order. Consider the case that there may not be a possible solution.

## Example

```n = 5443, t = 0```

There are three unique possible solutions.

1) ```5 - 4 - 4 + 3 = 0```
2) ```5 * (4 - 4) * 3 = 0```
3) ```5 * (4 - 4) / 3 = 0```

The solution ```(5 - 4) - (4 - 3) = 0``` should not be considered as it is mathematically equivalent to solution 1, once the parantheses have been expanded.