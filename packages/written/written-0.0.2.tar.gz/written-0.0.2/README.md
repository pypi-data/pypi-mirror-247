This package attempts to atomically write data to a file.

**Example 1:**

```python
import written

data = "my text"
path = "/path/to/file.txt"

written.write(data, path)
```



**Example 2:**

```python
import written

data = b'my bin data'
path = "/path/to/file.bin"

written.write(data, path)
```

**Installation:**
```bash
pip install written
```