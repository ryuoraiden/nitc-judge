# PD Lab 10 Q4: vehicle parking tree

Verbatim from PD Lab 10: a menu-driven program over a binary tree of vehicle records,
where vehicles are placed in **level order** as they arrive - not by vehicle number.

## Menu

| Option | Meaning | Output |
|---|---|---|
| `1 <Vno> <Vmodel> <Price>` | insert in level order | none |
| `2` | inorder | one record per line |
| `3` | preorder | one record per line |
| `4` | postorder | one record per line |
| `5` | level order | one record per line |
| `6 <Vno>` | search | the record, or `-1` |
| `7` | exit | none |

A record prints as `Vno Vmodel Price`, space separated. `100 <= Vno <= 250`, the model
is a single word of at most 30 characters, `1 <= Price <= 100`.

## Sample

```
1 105 RoyalEnfield 4
1 102 Dizire 8
1 108 Venue 14
2
3
4
5
6 108
6 103
7
```

```
102 Dizire 8
105 RoyalEnfield 4
108 Venue 14
105 RoyalEnfield 4
102 Dizire 8
108 Venue 14
102 Dizire 8
108 Venue 14
105 RoyalEnfield 4
105 RoyalEnfield 4
102 Dizire 8
108 Venue 14
108 Venue 14
-1
```

(The sheet prints the seven menu lines before the sample input; those are the menu,
not input.)

## Level order is not BST order

105 arrives first and becomes the root. 102 goes to the first free slot in level order -
root's left - and 108 to root's right. With a fourth vehicle it would go under 102's
left, **whatever its number**. The inorder output happens to look sorted in the sample
only because of the arrival order; test 3 onward will show you it is not.
