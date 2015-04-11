Dataview Sensors Application
============================

Getting data into Dataview

The API should handle most scenarios where you need to get data into dataview. 

POST http://dataview.restricted.wl-net.net/api/1/sensor-value/

{
    "sensor": "http://dataview.restricted.wl-net.net/api/1/sensor/14bae5f3-f6de-4234-b2a8-b6cfa8bc44ed/", 
    "value": "35.0"
}

If you are working from a Raspberry Pi, you may find this project helpful:
https://github.com/wl-net/dataview-rpi-sensor-client

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