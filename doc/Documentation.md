# Documentation

**Xsay** - this is a self-written Python library that serves to speed up python code somewhat by distributing basic calculations to one or more servers.

>from cient import Xsay


To connect to the server, use the decorator from the Xsay module -> *@send_file*

>> @Xsay.send_file(ip=..., port=...)
