Dataview Sensors Application
============================

Getting data into Dataview
---

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

Dealing with old data
---

Dataview provides a utility to delete sensor data older than n days.

```
$ python3 manage.py sensors_deleteoldsensorvalues 31feb385-259f-43fe-b929-a070db09a1cd 2
Delete 1148 recorded senor values before 2015-04-09 16:55:55.379834? Yes
Deleting...
```