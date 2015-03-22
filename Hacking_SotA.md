Shroud of the Avatar should be the next generation Ultima Online.

So i thought to myself: "Does it support Customized Servers?"

The answer is: obviously yes.

The game is still in pre-alpha, so a lot will change before it will be made playable, but the core won't probably change.

I started digging by looking through the game files.
SotA Client is being developed using Unity, so C#..
How convenient ;) (RunUO anybody?).

The core file for client handling is CSharp-Assembly.dll.

Talking about making a server we need to know how packets are sent through the net.

I first looked inside the exe, finding references to a C++ Dll but that was a dead end.
Networking is being made in C# too, using the Photon3 library for Unity.
https://www.exitgames.com/en/PUN

So if the client is using Photon the server should be Photon compatible...
Exactly.

The SotA serverS are based on the Photon Server LoadBalancing example.
I wrote "serverS" because the server is splitted into multiple instances.

We have:
- Master Server: This server handles connection, authentication and lobby joining (unique)

- Game Server: The server attached to the lobby you have been assigned to. Multiple Game servers can be created (But i'm not sure if this has been mantained.)

- Scene Server: A single server that handles housing for the world. (i think this is unique)

- Group Server: This server handles social interaction. (Party, friends, chat, etc.) (unique)

- Metrics Server: This server is a feedback server for your client. It does not require authentication and will provide informations about you client state/exceptions and your hardware

I started looking into "how to avoid using Photon Server" but then i got bored, too much work to do just to test something like what i had in mind.

PhotonServer is free to be downloaded and with a free licence you can accept up to 100 connections..
it's enough to start.

So i started looking for packets, finding the PortMessage class.
This class is the backbone of the whole SotA networking.

Instead of using the Photon protocol SotA developers chose to add a layer, represented by the PortMessage envelope.

A sigle PortMessage is characterized by a UINT identifier (i haven't found a logic in the ID assignements) and a JSONPropertyBag containing all the data. (Yes, all the data is sent as string...quite against performances..)

A JSONPropertyBag is a <string,object> serializable dictionary

Packets are encrypted by Photon.
I managed to dump them writing directly CIL into the CSharp-Assembly.dll.

The following thing to do was changing IP and the RSA public key used for authenticating.

I made a little program capable of doing such thing and replaced the ip with 127.0.0.1 and the RSA key with a known one.

Once the packets started flowing through my private Photon Loadbalancing instance i had only to handle them in the proper way.

My goal was to log-in, so everything related to DB Management (items ids, items properties, character appearance) was hardcoded.

After some effort i managed to reach the game screen :)!

I will now stop developing this server waiting for further developments (right now it's almost unplayable), but the path has been shown.

Attached you can see screenshots of my first login on local server.

PS: Please notice (again): my code does not use any DB (yet?), so the code is static and just written to reach logged state.

PPS: I bought the game, but i would wait to buy it again.. there are some things that disappointed me, such as the fact that the world structure does not allow UO Gates and Recall (you would need to wait the loading of the map you are moving to). Also the multi-scened world removes the idea of an enormous area where you can wander around (as UO was). Still, let's wait for future releases!

# ScreenShots #

![http://s16.postimg.org/xtvq09p11/Start.png](http://s16.postimg.org/xtvq09p11/Start.png)

![http://s16.postimg.org/fpspfmrcl/Character.png](http://s16.postimg.org/fpspfmrcl/Character.png)

![http://s16.postimg.org/va03661h1/loading.png](http://s16.postimg.org/va03661h1/loading.png)

![http://s16.postimg.org/m7blz51px/Login.png](http://s16.postimg.org/m7blz51px/Login.png)

![http://s16.postimg.org/xky5acc8l/Login2.png](http://s16.postimg.org/xky5acc8l/Login2.png)

![http://s16.postimg.org/ke8patgj9/Login3.png](http://s16.postimg.org/ke8patgj9/Login3.png)