WLNet Dataview Automation
=========================

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


Deciders
----

Deciders are responsible for determining the desired state of the system. While the state of the environment can always be modified manually, that cannot not be considered automation. Deciders might rely on sensors (such as those provided by the Dataview sensors application), schedule information, or any other external source in order to make decisions as to the final state of the environment.

Automators
----

Automators ensure that the physical world matches the desired state in dataview. They might communicate with a light to turn it off or adjust the volume on a speaker. Where possible, automators should rely on existing transports (such as those defined by Dataview's common transport library) to ensure secure communication to the target device.