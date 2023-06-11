"""
LRUCache

Adin Ackerman
"""

from dataclasses import dataclass, field

from Testable import Testable

from typing import TypeVar, Generic

# types
KeyT = TypeVar('KeyT')
ValueT = TypeVar('ValueT')

@dataclass(slots = True)
class LRUCache(Generic[KeyT, ValueT], Testable):
    """
    A generic, performant LRU cache for use with any hashable key and any value, of a specified size.
    
    Example:
    ```
    cache = LRUCache(size = 2) # we only need to remember two values

    def fib(n: int):
        if n<= 1:
            return n
        
        if not cache.contains(n):
            cache.put(n, fib(n - 2) + fib(n - 1)) # the order of these fib calls matters
        
        return cache.get(n)

    print(fib(100))
    ```
    """
    
    size: int
    
    itemList: list[KeyT]         = field(default_factory = list, init = False)
    itemMap:  dict[KeyT, ValueT] = field(default_factory = dict, init = False)
    
    def _evict(self) -> None:
        key = self.itemList.pop()
        self.itemMap.pop(key)
        
    def _touch(self, key: KeyT) -> None:
        self.itemList.remove(key) # O(n)
        self.itemList.insert(0, key)
        
    def _add(self, key: KeyT, value: ValueT) -> None:
        self.itemList.insert(0, key)
        self.itemMap[key] = value
    
    def contains(self, key: KeyT) -> bool:
        """Returns whether a given key is in the cache or not

        Args:
            key (KeyT): The key to search for

        Returns:
            bool: Whether the key is in the cache or not
        """
        return key in self.itemMap # O(1). nice
    
    def put(self, key: KeyT, value: ValueT) -> bool:
        """Put a new key/value pair in the cache. Or touch an already existing entry

        Args:
            key (KeyT): The key
            value (ValueT): The value

        Returns:
            bool: True if there already was an entry, False if not
        """
        if self.contains(key):
            self._touch(key)
            return True
        
        self._add(key, value)
        
        if len(self.itemList) > self.size:
            self._evict()
        
        return False
    
    def get(self, key: KeyT) -> ValueT:
        """Retrieve a value from the cache given a key

        Args:
            key (KeyT): The key of the entry to retrieve

        Returns:
            ValueT: The retrieved value
        """
        self._touch(key)
        return self.itemMap[key]
    
    
    # testing
    @Testable.test
    def keep_size() -> bool:
        cache = LRUCache(size = 5)
        
        for i in range(10):
            cache.put(i, ...)
        
        return len(cache.itemList) == 5
    
    @Testable.test
    def zero_size() -> bool:
        cache = LRUCache(size = 0)
        
        cache.put(..., ...)
        return not cache.contains(...) and len(cache.itemList) == 0
    
    @Testable.test
    def lru() -> bool:
        cache = LRUCache(size = 10)
        
        for i, j in zip(range(10), reversed(range(10))):
            cache.put(i, j)
            
        cache.put(..., ...)
        
        return not cache.contains(0) and all(cache.contains(i) for i in range(1, 9))
    
    @Testable.test
    def value_store() -> bool:
        cache = LRUCache(size = 39)
        
        for i, j in zip(range(56), reversed(range(56))):
            cache.put(i, j)
            
        for i, j in zip(range(56), reversed(range(56))):
            if not cache.contains(i): continue
            if not cache.get(i) == j:
                return False
                
        return True
        
        
    
if __name__ == '__main__':
    cache = LRUCache(size = 2) # we only need to remember two values

    def fib(n: int):
        if n<= 1:
            return n
        
        if not cache.contains(n):
            cache.put(n, fib(n - 2) + fib(n - 1)) # the order of these fib calls matters
        
        return cache.get(n)

    print(fib(100))