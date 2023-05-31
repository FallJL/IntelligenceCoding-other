def fib(self, n: int) -> int:  #fc:startStop "FUNC [fib]: enable or disable layer ."
        if n < 2:  #fc:ifBranch "IF" 
            return n  #fc:end "IF END"
        
        p, q, r = 0, 0, 1
        for i in range(2, n + 1): #fc:forLoop "LOOP" 
            p, q = q, r
            r = p + q  #fc:end "LOOP END" 
        
        return r  #fc:startStop FUNC [fib]: END
