
###  1.1 What is PageRank Algorithm?

PageRank is an algorithm for ranking web pages by importance, originally developed by Larry Page and used as one of the foundations of early Google search, PageRank is introduced as an application of finite discrete-time Markov chains.


### 1.2 Markov Chain

consider a finite graph with nodes $X$={$1, 2,...,N$}

$P[X(n + 1) = j |X(n) = i, X(m), m < n]= P (i, j ), ∀i, j ∈ X ,n ≥ 0.$

The probability of moving from i to j does not depend on the previous states. This “**amnesia**” is called the Markov property.