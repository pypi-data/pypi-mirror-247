This package generates unique string identifiers.

```python
from ustrid import ustrid

unique_string_id = ustrid()
```

Under the hood:

```python
import uuid
import threading


def ustrid():
    """Generate a unique string identifier (thread-safe)"""
    return Ustrid.run()


class Ustrid:

    """Private class to generate unique string identifiers (thread-safe)"""
    _lock = threading.Lock()
    _count = 0

    @classmethod
    def run(cls):
        """Generate a unique string identifier (thread-safe)"""
        with cls._lock:
            cls._count += 1
            return "{}-{}".format(cls._count, uuid.uuid4())
```


**Installation:**
```bash
pip install ustrid
```
