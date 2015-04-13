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

##### Ensuring State

Your automator should be designed such that sending the same command multiple times should have no impact as long as the system is already in that state.

For example, if you automate a light switch you should not implement change_state() but rather turn_on() and turn_off(). Some use cases will fit outside of this model, such as a coffee maker. In these cases, care must be taken to ensure that the action is performed only once by returning accurate status information to automator requests.

Tasks
----

Tasks are a way of telling automators what to do. For example, you might have a humidifier that you want to turn on and set the fan speed to low. A task can incorporate both of these actions for simplicity.

##### Task Groups

Tasks only relate to one automator, so if you need to trigger multiple automators you should place your tasks in a task group. 

Tasks and task groups can be run from the command line:

```
python3 manage.py automation_runtask 913c7e48-6260-4374-b182-55a849a69671
```

Deciders
----

Deciders are responsible for determining the desired state of the system. While the state of the environment can always be modified manually, that cannot not be considered automation. Deciders might rely on sensors (such as those provided by the Dataview sensors application), schedule information, or any other external source in order to make decisions as to the final state of the environment. Deciders must always return "True" or "False", and can be implemented to answer decisions that rely on specific user preferences, for example "is it warm outside"

Core deciders:

* time
* day
* holiday
* json-rpc (abstract)

Deciders can be queried from the web interface:

http://dataview.restricted.wl-net.net:8000/portal/automation/query-decider/824a884d-0732-4f48-91af-0e69f58486f3

```
{"name": "Should humidifier run?", "decision": {"boolean": true, "string_descriptive": [{"message": "comparison of 35.0 was less than 50.0"}], "numeric": 1}}
```

or via the command line:

```
$ python3 manage.py  automation_calldecider 824a884d-0732-4f48-91af-0e69f58486f3
{'string_descriptive': [{'message': 'comparison of 34.0 was less than 50.0'}], 'numeric': 1, 'boolean': True}
```

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
