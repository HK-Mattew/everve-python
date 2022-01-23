# Example of use
```python
from everve import Everve

ever = Everve(
    api_key='<api_key>'
)

result = ever.balance()

print(result)
# -> {'user_id': '...', 'user_balance': '...'}

```