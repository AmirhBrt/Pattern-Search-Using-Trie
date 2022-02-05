# Pattern Searching with Trie
The Problem here is to use a *Tree Data Structure* to search a word with one missing part in all of the documents. 
In this implementation, we used ***Trie*** to store and search words of multiple documents.
The main idea behind this implementation is explained below.

## Insert

To insert a word in Trie, First, add a *'$'* at the end to act as a sign for the end of the word.
Then insert all left rotations of this word to the Trie.
For each left rotation, Remove the first character of the string and place it at the end.

As an instance, Imagine inserting the word *'hello'* to the Trie:

At first we add *'$'* at the end, So we have *'hello$'*.now we insert all rotations of the word *'hello$'*. all of the rotations are:

+ *hello$*
+ *ello$h*
+ *llo$he*
+ *lo$hel*
+ *o$hell*
+ *$hello*

#### Note:
If the word we are inserting was already at Trie, we increase the number of that word which is saved in the last leaf node.

## Search

For searching a specific pattern with one missing substring, First, add a *'$'* at the end.
Then do the left rotation until the missing substring is at the end of the word.
Now search for the pattern in Trie.
You can find all possible words matching the pattern using backtracking (view search method code for details).
