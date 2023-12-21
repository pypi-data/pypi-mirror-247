unique_log_filter
=================

A simple tool to filter out duplicate lines from a log file. Usage is simple:

```python
from logging import getLogger
from unique_log_filter import UniqueLogFilter

logger = getLogger("my_logger")
logger.addFilter(UniqueLogFilter())
```
