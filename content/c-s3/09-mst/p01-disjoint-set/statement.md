# Disjoint set union (find, unite)

The structure that makes Kruskal's algorithm possible: it answers "are these two
vertices already connected?" in almost constant time.

```c
void dsuInit(DSU *d, int n);
int  find(DSU *d, int x);           /* representative of x's set */
int  unite(DSU *d, int a, int b);   /* 1 if merged, 0 if already together */
```

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `u a b` | union | `MERGED` or `ALREADY` |
| `f a b` | same set? | `SAME` or `DIFFERENT` |
| `c` | how many sets remain | a number |
| `e` | exit | nothing |

The first line of input is `n`.

## Example

```
6
f 1 2
u 1 2
f 1 2
u 2 3
f 1 3
c
e
```

```
DIFFERENT
MERGED
SAME
MERGED
SAME
4
```

After merging {1,2,3}, the remaining sets are {1,2,3}, {4}, {5}, {6} - four of them.

## The two optimisations

**Path compression** (in `find`): after finding the root, point `x` directly at it.
Trees stay almost flat.

```c
if (d->parent[x] != x) d->parent[x] = find(d, d->parent[x]);
return d->parent[x];
```

**Union by rank** (in `unite`): hang the shorter tree under the taller one, so the
result never gets deeper than necessary. `rank` is an upper bound on height; it only
increases when you join two trees of equal rank.

Together they give near-`O(1)` amortised operations. With `n <= 100` you would survive
without either, but they are three lines each and they are what the theory syllabus
means by "implementation using disjoint set data structure".

## The mistake to avoid

`unite` must work on the **roots**:

```c
int ra = find(d, a), rb = find(d, b);   /* then join ra and rb */
```

Writing `d->parent[b] = a` joins two individual vertices and orphans everything else
that was in their sets. It passes small tests and fails the moment three things merge.
