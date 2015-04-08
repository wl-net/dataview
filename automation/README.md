WLNet Dataview Automation
=========================

Dataview implements automation in three pieces. Automators are traditional "remote control" and are only concerned with performing actions. Deciders are responsible for mapping strings such as "Am I sleeping" to a machine readable value, and controllers are the glue that connect deciders and automators.
Automators
----

Automators ensure that the physical world matches the desired state in dataview. They might communicate with a light to turn it off or adjust the volume on a speaker. Where possible, automators should rely on existing transports (such as those defined by Dataview's common transport library) to ensure secure communication to the target device.

#### Working with Automators

The following examples show calling of an automator. In this case, the Automator was a Music automator leveraging JSON RPC as a transport over TLS. The entire process of changing the volume is left to the Automator. Configuration for communicating with the Automator is configured within the automator class.

```python
a = Automator.objects.get(id=1)
a.do_operations('[{"method": "set_volume", "params": ["50"]}]')
a.get_instance().set_volume(50)
a.get_instance().pause()
```

Calling an automator from the command line

```
python3 manage.py automation_callautomator "WLNet Denny Triangle Sound" play http://kandi.shoutdrive.com:80
```
##### Writing your own Automator

Create an empty file in YOUR_APPLICATION/automators/YOUR_AUTOMATOR_TYPE/YOUR_TRANSPORT.py Create a python class that extendss AbstractAutomator as shown below:

````
from dataview.transports.json_rpc import JSONRPCClient
from automation.automators import AbstractAutomator

class HumidiferJSONRPCAutomator(AbstractAutomator):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.client = JSONRPCClient()
        self.client.connect(configuration['target'], configuration['token'], configuration['certificate'])
        
    ... your automation methods
````

See the sample automators within the source tree for examples:
https://github.com/wl-net/dataview/tree/master/automation/automators

Deciders
----

Deciders are responsible for determining the desired state of the system. While the state of the environment can always be modified manually, that cannot not be considered automation. Deciders might rely on sensors (such as those provided by the Dataview sensors application), schedule information, or any other external source in order to make decisions as to the final state of the environment. Deciders must always return "True" or "False", and can be implemented to answer decisions that rely on specific user preferences, for example "is it warm outside"

Core deciders:

* time
* day
* holiday
* json-rpc (abstract)

#### Performance Considerations

Steps should be taken to prevent dataview from having to spend excessive time querying other services about their status. External systems that influence the decision of dataview should consider the implementation of the "sensors" application where sensors can report back with information directly to dataview.

Controllers
----

Controllers contain a list of deciders, specific directions for automators to perform, and metadata tying automators and deciders together. The current implementation defines special "through" classes that contain the configuration and actions for Deciders and Automators. The goal here is to reduce the amount of logic placed in the controller and defer it to the implementation of specific deciders. Deciders are evalulated in a priority based order.

Examples of specific rules that can be implemented in dataview:

* If it is after 9am and before 5pm, set status to away, otherwise set status to online (Decider: Time. Automator: Status)
* If it is after 10pm and before 6am, turn the lights off (Decider: Time. Automator: Light)
* When there is no motion after 10pm, reduce the music volume (Decider: Time, Sensor. Automator: Music)

Implementing this in a way that is easy for a user to program may require the addition of a models to handle the creation of rules where slight variances to the rules results in a automator being called.  However, in general we want to avoid making Controllers complicated and defer as much of the decision process to Deciders.
