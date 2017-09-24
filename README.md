# RecursiveDescentParser
Implementation of Generic Recursive Descent Parser for Syntax Analysis Phase <br />

# Input Grammar
A->iB <br/>
B->+iB/null <br />

# Test String for above GRAMMAR
i+i$ - **PASS** <br />
i+ i+ i +$ - **PASS** <br />
i+$ - **FAIL** <br />
\+ $ - **FAIL** <br />
