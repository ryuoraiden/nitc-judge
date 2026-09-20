# Week 5 Q1: Emergency Communication Network (Prim)

Verbatim from the Week 5 sheet.

> A disaster-management authority needs to establish a temporary communication network
> among `n` emergency response centers... The authority wants to connect all response
> centers with the minimum possible total cost, without creating unnecessary cycles. A
> fixed starting center `s` is given. **The network must be built starting from this
> center.** All link costs are positive and distinct.
>
> After constructing the complete minimum-cost spanning tree, display the final tree and
> its total cost. If all vertices cannot be reached from the given source, print `-1`.

## Input format

```
n
m
s
u1 v1 w1
...
```

Constraints: `1 <= n <= 100`, `1 <= w <= 1000`, `u != v`.

## Output format

The MST as an `n x n` adjacency matrix - `0` on the diagonal, the weight for a chosen
edge, `-1` where there is none - then the total cost. If the graph is not connected,
print `-1` and nothing else.

## Sample

```
5
7
1
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 10
4 5 7
```

```
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
15
```

## Which algorithm, and does it matter?

"Must be built starting from this center" is Prim's wording, and Q2 is the Kruskal
one - the pair is deliberate, so use the one each question describes.

A useful thing to notice: **all weights are positive and distinct, so the MST is
unique.** That means Prim-from-`s` and Kruskal produce the *same* tree here, and since
this question prints no intermediate states, `s` only really affects the reachability
test. If you run out of time, a Kruskal you remember beats a Prim you half-remember.

Also, because the graph is undirected, "reachable from `s`" is the same as "the graph
is connected", so both questions' `-1` cases reduce to the same check: did you manage
to add exactly `n-1` edges?

## The output matrix is separate

Do not overwrite the input weights. Keep `tree[][]` initialised to `0` on the diagonal
and `-1` elsewhere, and fill in only the `n-1` chosen edges, in **both** directions.
