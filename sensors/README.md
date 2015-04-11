Dataview Sensors Application
============================

Working with reported sensor values
---

From your python code:

```python
from sensor.models import SensorValue

print(SensorValue.objects.filter(sensor="14bae5f3-f6de-4234-b2a8-b6cfa8bc44ed").order_by('-updated')[0].value)
```

From the command line:

```
$ python3 manage.py sensors_getsensorvalue 14bae5f3-f6de-4234-b2a8-b6cfa8bc44ed
'23.0' was reported at 2015-04-11 23:16:07.674237+00:00
```