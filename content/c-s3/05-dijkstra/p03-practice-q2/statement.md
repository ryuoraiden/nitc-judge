# Practice Question 2 (full)

Verbatim from the Week 4 sheet.

> There is a network of `n` locations, labeled from 1 to `n`. You are given an
> adjacency matrix `time[n][n]`, where `time[i][j]` represents the time in minutes
> it takes for an emergency rescue team to travel directly from location `i` to
> location `j` along a **one-way** road (`0 <= time[i][j] < 999`). If there is **no
> direct road** from `i` to `j`, `time[i][j]` is equal to 999.
>
> `n` emergency teams start from location `k` and begin delivering emergency
> supplies to all other locations concurrently. Write a program to find the
> **minimum total time** required for all `n` locations to receive supplies from
> location `k`. If any location cannot be reached from `k`, return `-1`.

## Input format

- first line: the number of vertices `n`
- next `n` lines: the adjacency matrix `time[n][n]`
- last line: `k`

## Output format

A single integer: the minimum total time, or `-1`.

## Sample

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

## What is actually new here

Very little - and that is the point of having climbed the ladder. You wrote the
Dijkstra in problem 1 and the max-vs-sum rule in problem 2. What remains is reading
the input and remembering that `k` is 1-based while your arrays are not.

Decrement `k` exactly once, immediately after reading it. Doing it later, or twice,
is the classic way to get an answer that is right for a different source vertex.
