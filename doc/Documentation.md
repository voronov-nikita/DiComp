# Documentation

**Xsay** - this is a self-written Python library that serves to speed up python code somewhat by distributing basic calculations to one or more servers.

>from cient import Xsay


To connect to the server, use the decorator from the Xsay module -> *@send_file*

Examples:
```python
from Xsay import Xsay

# initializing the Xsay object
server = Xsay()

# this decorator takes in the values of the IP address and port to connect to the server on which the calculations will be performed.
@server.send_file(ip="0.0.0.0", port=0000)
def function_one(a, b):
    return a + b

# Be sure to call the function
function_one(10, 50)
```
