WLNet Dataview Automation
=========================

Automators
----

Automators ensure that the physical world matches the desired state in dataview. They might communicate with a light to turn it off or adjust the volume on a speaker. Where possible, automators should rely on existing transports (such as those defined by Dataview's common transport library) to ensure secure communication to the target device.

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

Speaker Control
----

#### Speakers

Each speaker should be placed in one room within a residence. Dataview allows you to adjust the volume and mute (preserving the original volume on unmute) speakers individually. The sound playing on the speakers is controlled by Speaker Sources, described below.

#### Speaker Sources

If speakers are only intended to be operated standalone, each speaker can be its own source.

WLNet Dataview also supports operating speakers in time-synced audio receivers over TCP/IP. Dataview does not currently provide an implementation of the actual transport, though pulseaudio and RTP have proven to work in testing.

#### Radio Stations

Dataview allows the creation of radio stations as target media to play on speaker sources.


Mood Control
----

A mood is defined as a name and a collection of properties that are associated with that name. For example, the "sleep" mood might turn off lighting and play ambient background music.

The current mood is defined on a per-residence or per-room basis and can be changed either manually or based on the output of deciders.
