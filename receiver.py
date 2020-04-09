import cmdbroker
import json
from robomover import RoboMover

mover = RoboMover()
broker = cmdbroker.CommandBroker()
for command in broker.Receive():
    print(command.commandType)
    mover.Move(command)

mover.Done()