# Documentation

**Dicomp** - this is a self-written Python library that serves to speed up python code somewhat by distributing basic calculations to one or more servers.

>from dicomp import Dicomp


To connect to the server, use the decorator from the Xsay module -> *@send_file*

1. User`s example:
    ```python
    from dicomp import Dicomp

    # initializing the Xsay object
    server = Dicomp()

    # this decorator takes in the values of the IP address and port to connect to the server on which the calculations will be performed.
    @server.send_file(ip="0.0.0.0", port=0)
    def function_one(a, b):
        # your code
        return a + b

    # Be sure to call the function
    function_one(10, 50)
    ```

2. Server`s example:

    ```Bash
    SERVER IS RUN... 
    IP: 0.0.0.0
    PORT: 0

    192.168.0.0 523462
    OUT: b'60'

    ```
