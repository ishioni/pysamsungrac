# pysamsungrac

A python library for Samsung ACs

Currently supported devices:

* Samsung RAC (port 8888)

## Install

```bash
pip install pysamsungrac
```

## Example usage
```python
rac = SamsungRac(SamsungRacConnection(address, token))
rac.set_target_temperature("21")
```

You can also look at the included samsungrac.py script in bin

## TBD

* Support getting the token automatically
* Support power usage statistics
* Support Samsung2888 devices
