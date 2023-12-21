# structlib-py
similar function to the builtin struct-library but more efficient

```python
import structlib as sl

@dataclasses.dataclass
class MyStruct(sl.Structure):
    name: Annotated[str, sl.String(10))]
    value: int

sl.dumps(MyStruct("Hello World", 10))
MyStruct.struct_dumps(binary/stream)
b'\x12Hello World\x10'
sl.loads(binary/stream, type=MyStruct)
MyStruct.struct_load(binary/stream)
```
