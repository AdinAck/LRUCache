"""
Cached

an abstraction of the LRUCache to apply it to any Callable type (function, or functor, etc.).

Adin Ackerman
"""

from __future__ import annotations
from dataclasses import dataclass

from cache.LRUCache import LRUCache

from typing import TypeVar, Callable

ValueT = TypeVar('ValueT')
Cachable = Callable[..., ValueT]

@dataclass(slots = True)
class _Signature:
    args: tuple
    kwargs: dict
    
    def __init__(self, args: tuple, kwargs: dict):
        self.args = args
        self.kwargs = kwargs
    
    def __hash__(self) -> int:
        return hash((self.args, frozenset(self.kwargs)))
    
    def __eq__(self, other: _Signature) -> bool:
        arg_check = all(left == right for left, right in zip(self.args, other.args))
        
        if not arg_check: return False
        
        key_check = (
            all(key in other.kwargs for key in self.kwargs)
            and
            all(key in self.kwargs for key in other.kwargs)
        )
        
        if not key_check: return False
        
        pair_check = all(self.kwargs[key] == other.kwargs[key] for key in self.kwargs)
        
        return pair_check

class Cached(LRUCache[_Signature, ValueT]):
    """
    Decorator for `LRUCache` for any Callable.
    
    Example:
    ```
    @Cached(size = 2)
    def fib(n: int):
        if n <= 1:
            return n
        
        return fib(n = n - 2) + fib(n = n - 1) # the order of these calls matters. "least recently used"
    
    print(fib(100)) # would run forever if not cached
    ```
    """
    
    def __call__(self, f: Cachable) -> Cachable:
        def dispatch(*args: ..., **kwargs: ...) -> ValueT:
            s = _Signature(args, kwargs)
            if not self.contains(s):
                self.put(s, f(*args, **kwargs))
            
            return self.get(s)
        return dispatch
            
        
if __name__ == '__main__':
    @Cached(size = 2)
    def fib(n: int):
        if n <= 1:
            return n
        
        return fib(n = n - 2) + fib(n = n - 1) # the order of these calls matters. "least recently used"
    
    print(fib(100)) # would run forever if not cached