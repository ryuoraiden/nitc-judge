# Practice Question 1 (full)

The real thing, verbatim from the Week 4 sheet. You write the entire program this
time - parsing, traversal and output.

> Write a program that takes an unweighted directed graph `G`, in the form of an
> adjacency list, and a vertex `s` in `G` as inputs, and find (and print) the
> shortest paths between vertex `s` and every other vertex. If multiple shortest
> paths exist, choose the lexicographically smallest path.

## Input format

- first line: the number of vertices `n`
- next `n` lines: the adjacency list of `G`
- last line: the source vertex `s`

Each adjacency line begins with the vertex itself, followed by its neighbours:

```
4 1 2 3
```

means vertex `4` has edges to `1`, `2` and `3`. A vertex with no out-edges appears
alone on its line. Neighbours are **not** guaranteed to be in ascending order.

## Output format

`n` lines, one per vertex `1..n` in increasing order: the path from `s` to that
vertex, with `-` between vertices. The line for `s` itself is just `s`.

If a vertex is unreachable from `s`, print `-1`. (The sheet does not say what to do
here; this is the same choice your own Week 4 solution made, and test 6 checks it.)

## Sample

```
5
1 3 4
2 4 5
3 1 4
4 1 2 3
5 2
1
```

```
1
1-4-2
1-3
1-4
1-4-2-5
```

## The parsing is the hard part

The graph logic is exactly the previous problem. What is genuinely new is reading
an adjacency list where **each line has a different number of numbers**, so a plain
`scanf("%d")` loop has no way to know when a line ends.

Read whole lines with `fgets`, then split them with `strtok(line, " \t\r\n")`.

One trap that costs people ten minutes: after `scanf("%d", &n)`, the newline after
`n` is still in the input buffer, so your first `fgets` returns an empty line and
everything shifts by one. Consume the rest of that line first:

```c
int ch;
while ((ch = getchar()) != '\n' && ch != EOF) { }
```

Build it in three stages - parse and echo the adjacency lists, then BFS, then the
path printing - and you will find the bug in whichever stage has it, instead of
staring at a wrong final answer.
