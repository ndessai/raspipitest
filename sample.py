import commands
import json



broker = commands.CommandBroker()

while True:
    print("Enter Command")
    x = int(input())
    if x < 1 or x > 3:
        break
    if x == 1:
        broker.Send(commands.StartCommand())
    elif x == 2:
        broker.Send(commands.StopCommand())
    else:
        broker.Send(commands.MotionCommand(commands.MotionType.MoveForward, 1, 1))
    