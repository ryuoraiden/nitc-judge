# Minimum total time (the Q2 rule)

Dijkstra is provided. This rung is one short function - and one modelling decision
that is easy to get backwards.

> `n` emergency teams start from location `k` and begin delivering emergency
> supplies to all other locations **concurrently**. Find the minimum total time
> required for all `n` locations to receive supplies. If any location cannot be
> reached, return `-1`.

```c
int minTotalTime(int n, int w[MAXV][MAXV], int src);
```

## Input format

```
n
<n lines of n integers: the adjacency matrix>
k
```

`time[i][j]` is the cost of the one-way edge `i -> j`. A value of **999** means
there is no such edge. The diagonal is 0. `k` is given **1-based**; the harness
converts it before calling you, so your `src` is already 0-based.

## Output

A single integer, or `-1`.

## Example

```
5
0 5 999 999 2
999 0 1 1 999
999 999 0 2 9
999 999 999 0 10
999 2 7 999 0
1
```

```
5
```

The distances are `0 4 5 5 2`.

## The modelling decision

"Total time" sounds like a sum. It is not.

The teams travel **concurrently** - all of them set out at the same moment and none
waits for another. So the job is finished the instant the *last* location receives
its supplies, and the elapsed time is the **largest** of the shortest distances, not
their total.

In the sample, the sum would be 16 and the answer is 5.

## The order of the two checks

Take the maximum of `dist[]` and you will happily return `INF` when some location is
cut off. Test the reachability of every vertex first, return `-1` the moment one
fails, and only then take the maximum over what remains.
