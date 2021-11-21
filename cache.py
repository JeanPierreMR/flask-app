from functools import lru_cache

@lru_cache(maxsize=16)
def fib(n):
    if n==0 or n==1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

import time 

tl = time.time()
print([fib(x) for x in range(70)])
t2 = time.time()

t2-tl

print(fib.cache_info())