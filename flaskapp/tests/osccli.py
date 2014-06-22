from OSC import OSCClient, OSCMessage
from time import sleep

client = OSCClient()
client.connect( ("localhost", 8000) )

# client.send( OSCMessage("/skeletons/0/joints/fingertips/position", [1.0, 2.0, 3.0 ] ) )
for i in range(1, 1000):
    client.send( OSCMessage("/skeletons/0/joints/fingertips/position", [1.0, 2.0, 3.0 ] ) )
    sleep(.5)


# client.send( OSCMessage("/user/1", [1.0, 2.0, 3.0 ] ) )
# client.send( OSCMessage("/user/2", [2.0, 3.0, 4.0 ] ) )
# client.send( OSCMessage("/user/3", [2.0, 3.0, 3.1 ] ) )
# client.send( OSCMessage("/user/4", [3.2, 3.4, 6.0 ] ) )
# 
# client.send( OSCMessage("/test/1", [3.2, 3.4, 6.0, 'Testing' ] ) )
# 
# client.send( OSCMessage("/quit") )
