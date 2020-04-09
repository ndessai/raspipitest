import cmdbroker
import json
from robomover import RoboMover

mover = RoboMover()
broker = cmdbroker.CommandBroker()
print("Waiting for commands")
for command in broker.Receive():
    print(command.commandType)
    mover.Move(command)

mover.Done()
