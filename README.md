# RecursiveDescentParser
Implementation of Generic Recursive Descent Parser for Syntax Analysis Phase

# Input Grammar
A->iB
B->+iB/null

# Test String for above GRAMMAR
i+i$ - **PASS**
i+ i+ i +$ - **PASS**
i+$ - **FAIL**
+ $ - **FAIL**
