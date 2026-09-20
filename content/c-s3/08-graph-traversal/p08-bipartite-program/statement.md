# Week 3 evaluation: bipartite from adjacency lines

> Read a graph given as adjacency-list lines, where each line begins with a vertex
> followed by its neighbours. Determine whether the graph is bipartite using DFS
> implemented with a stack. If it is, print the two colour sets; otherwise print `-1`.

**This is a reconstruction**, not the official sheet - the wording is from memory of
the Week 3 evaluation. The algorithm and the parsing are what matter, and both are
exactly what that question tested.

## Input format

- first line: the number of vertices `n`
- next `n` lines: `u v1 v2 v3 ...` - vertex `u` followed by its neighbours, in any order

The graph is undirected; each edge appears in both endpoints' lines. A vertex with no
neighbours appears alone on its line.

## Output format

Two lines: the vertices of colour 0 then the vertices of colour 1, each ascending and
space separated. In every component the smallest-numbered vertex takes colour 0. Print
`-1` if the graph is not bipartite.

## Example

```
4
1 2 4
2 1 3
3 2 4
4 1 3
```

```
1 3
2 4
```

## The parsing is the marks

You lost a test case on this question to `%c` parsing tripping over a **trailing
space**. Several tests here have trailing spaces, and one has a blank line, precisely
so that a fragile parser fails locally instead of in the exam.

The robust recipe:

```c
int ch; while ((ch = getchar()) != '\n' && ch != EOF) { }   /* after scanf("%d", &n) */
...
fgets(line, sizeof line, stdin);
char *tok = strtok(line, " \t\r\n");        /* all four delimiters */
if (tok == NULL) continue;                  /* blank line - do not count it */
```

`strtok` with that delimiter set collapses any run of spaces, tabs and carriage
returns, so trailing whitespace produces no phantom token at all. Reading character by
character and deciding what a space means yourself is how a single stray byte costs
two marks.

## The algorithm

Stack-based DFS, colouring each neighbour `1 - colour[u]`, with the
for-every-uncoloured-vertex loop around it so disconnected graphs work.
