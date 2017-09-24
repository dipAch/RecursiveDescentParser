# RecursiveDescentParser
Implementation of Generic Recursive Descent Parser for **Syntax Analysis Phase**. It can take any valid grammar <br />
accepted by the RDP, and transform the production rules to recursive functions or procedures at runtime. <br />

# Test Input Grammar
A->iB <br/>
B->+iB/null <br />

# Test String for above GRAMMAR
i+i$ - **PASS** <br />
i+ i+ i +$ - **PASS** <br />
i+$ - **FAIL** <br />
\+ $ - **FAIL** <br />
