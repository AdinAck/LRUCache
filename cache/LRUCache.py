"""
LRUCache

A generic, performant LRU cache for use with any hashable key and any value, of a specified size.

Adin Ackerman
"""

from dataclasses import dataclass, field

from typing import TypeVar, Generic

# types
KeyT = TypeVar('KeyT')
ValueT = TypeVar('ValueT')

@dataclass(slots = True)
class LRUCache(Generic[KeyT, ValueT]):
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
        
        if len(self.itemList) == self.size:
            self._evict()
        
        self._add(key, value)
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