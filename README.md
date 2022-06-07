# Welcome to Minestomp!

Minestomp is a Minecraft server written in Python, based on the incredible [Minestom](https://minestom.net/) library.  Since Minestom is written in Java, Minestom**p** aims to leverage Java compatible Python tech such as [GraalPython](https://www.graalvm.org/python/) and [Jython](https://www.jython.org/).

Minestomp aims to provide a simple, easy to understand, easy to customize option for those wanting to quickly develop custom Minecraft experiences.  

One primary motivation I had to with this is to tweak the Minecraft experience for my own children, and possibly even use it to teach them Python, with features like in-game scripting!  With that in mind, a primary motivation of this project is really to keep things as simple as possible for everyone.

## Install

```
# Do the following from a linux/unix type shell.

# Gets all the code to your local machine / server
git clone https://github.com/stucotso/minestomp.git

# Be sure to make your cwd (current work dir) buildutils
cd minestomp/buildutils

# Initializes all the Gradle stuff needed to build the server
./setup.sh

# Move to the main server folder
cd ../launcher

# Invokes all the gradle magic needed to compile
./gradlew build

# get back to the repo root
cd ..

# Runs the Minestomp server on a demo script!
./rundemo.sh
```
After the above, the server will listen on 0.0.0.0 / port 25565 by default. 
Ensure the port is open on your router or server if you
want to connect from another machine.  

Otherwise just run Minecraft (Java edition for now) and connect!

## Usage

Feel free to copy the [rundemo.sh](https://github.com/stucotso/minestomp/blob/main/rundemo.sh) script and modify for your own server!  

Currently the first line is needed, as the working directory needs to be the 'python' folder of Minestomp for now, so that python libraries in the source tree are accessible for import by other scripts.

Feel free to copy the 'demo.py' script and modify to build your own Minecraft experience completely in Python!

The rundemo.sh script, for reference contains the following:

```
cd ./launcher/src/main/python
java -jar ../../../build/libs/minestomp-0.1-all.jar ./examples/demo.py
```

## Contributing

PRs accepted. Send em!

## License

Public Domain

## Features

Minestomp is purely experimental stage right now. That being said there is a lot planned!

```
Key: [X] = Feature implemented  [ ] = Planned

[X] Just get it 'to work' (tm) under Jython for now.
[X] Expose the entire Minestom API via Python
[X] Provide a basic working demo sample
[ ] GraalPython support (speed/performance boost)
[ ] Bedrock client support via Geyser (https://geysermc.org/) so any Minecraft client can connect, right out of the box

Many more example scripts for common features, such as:

[ ] Mobs / AI / Pathfinding
[ ] Combat
[ ] Recipes
 
[ ] Leverage Python eval() to let players attach scripts to their worlds in-game!

[ ] more to come....
```

## FAQ

* What's with the name?

    > Minestom = Minecraft + Custom
    > 
    > Minestom**p** = Minestom + **P**ython!

* Why Python?

    > Many reasons! It's fun, easy to learn, easy to read, and needs less typing to write.  But mainly, I'm looking to use Minestomp to help teach programming to children, possibly even allow them to write Python in-game, to customize their worlds!  Because of its simplicity, Python
    is a great fit here.
    > 
    > Note also Python consistently ranks as the #1 language in the world in popularity on many indexes, such as [TIOBE](https://www.tiobe.com/tiobe-index/) - it seems many adults also enjoy the language!


* Are you really using Jython?! Isn't that library slow/outdated/etc. ?

    > We'd also like to add GraalPython support very soon!  But due to it's experimental status it's probably better to support both for now.

* But seriously, isn't Python too slow for something like a Minecraft server? Won't my world run slowly?

    > A lot of the 'performance sensitive' stuff that needs to happen is  already handled by the Minestom/Java code under the hood.  Minestom is a very well designed, high performance Minecraft system. That being said, we're also aiming to keep the Python and Java API code very similair so if you ever need to optimize a particular piece of logic, it would be very easy to do.
    >
    > Another thing to note is that Python performance on the JVM is advancing fairly nicely - it's likely that Python will gain considerable speed improvements in time.  For example it's been found that Javascript (a language as dynamic as Python) performance on GraalVM is [at times faster than Java](https://www.youtube.com/watch?v=GmxXgUkOOdw), with GraalPython being built on the same technology!
    >
    > On this topic, a great read is: [premature optimization is the root of all evil !](https://stackify.com/premature-optimization-evil/)
