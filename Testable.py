from __future__ import annotations
from typing import Callable
    
class Testable:
    tests: list = []
    
    # unfortunate the decoration sugar is
    # not so sweet on the definition side
    @classmethod
    def test(cls, f: Callable[[], bool]):
        cls.tests.append(f)
        return f
    
    @classmethod
    def run_tests(cls) -> None:
        for i, test in enumerate(cls.tests):
            result = test()
            
            status = 'PASS' if result else 'FAIL'
            print(f'[{i}] {test.__name__} test: {status}')
            
            if not result: break
        else:
            print('All tests passed!')