# Information Retrieval System with Spelling Correction and Wildcard Queries

This repository contains the implementation of an Information Retrieval System developed as part of a university project. The system is capable of processing textual data, handling spelling corrections, and supporting wildcard queries using a trie data structure. This README file provides an overview of the project's goals, challenges, and improvements, along with a technical description of the implementation.

## Project Overview

This project involves the development of an Information Retrieval System designed to efficiently search and retrieve documents. The system supports:

- **Spelling Correction**: Uses dynamic programming to find the closest matching words in the posting list.
- **Wildcard Queries**: Implements wildcard search using a trie data structure that supports rotation of strings and appends `$` at the end to facilitate searching.
- **Tokenization**: Processes input text by tokenizing and removing stop words and punctuation.

## Key Challenges and Improvements

### Trie Tree Implementation

The primary challenge of this project was the construction of an efficient trie tree. This was accomplished by designing two classes:

- **Node Class**: Implements each node of the trie tree.
- **Trie Tree Class**: Manages the entire trie structure and supports operations like word insertion, BFS traversal, and wildcard search.

### Wildcard Search

To perform wildcard searches, the project leverages circular permutations of strings by appending `$` at the end of each string. The implementation supports both single and double wildcards, optimizing for speed and accuracy.

## Libraries Used

- **NLTK (Natural Language Toolkit)**: Used for text tokenization and stop word removal.
  - `word_tokenize`: Tokenizes the input text.
  - `stopwords`: Provides a list of common stop words in the English language.
- **String**: Utilized for handling punctuation in text data.
- **NumPy**: Employed for efficient numerical operations, such as calculating distances.
- **Copy**: Used for deep copying data structures where necessary.

## Code Structure

### Node Class

The `Node` class represents each node in the trie tree, maintaining information about child nodes, the character it represents, and whether it forms a valid word.

### Trie Tree Class

The `TrieTree` class manages the trie structure, supporting word insertion, BFS traversal, and wildcard search operations. Key functions include:

- `insertWord`: Inserts a word into the trie.
- `insertWordPermutation`: Inserts all circular permutations of a word.
- `find`: Searches for wildcard patterns in the trie.

### Search Engine Class

The `SearchEngine` class orchestrates the input processing, posting list management, and query execution. Key functions include:

- `addToPostingList`: Adds tokenized words to the posting list.
- `spellCheckingSingleWord`: Performs spelling correction for individual words.
- `spellCheckingExpression`: Corrects spelling for each word in an expression.
- `findQuery`: Executes queries, supporting spelling correction and wildcard searches.

## How to Use

1. **Input Documents**: Add paths to your documents using the `input()` method.
2. **Execute Queries**: Use the `findQuery()` method to perform searches with or without wildcards.
3. **Spell Checking**: Utilize the `spellCheckingExpression()` method for correcting spelling errors in input queries.

This project demonstrates a comprehensive approach to building an Information Retrieval System, focusing on trie data structures for efficient search and retrieval operations.
