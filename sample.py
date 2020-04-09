import cmdbroker
import cmdmoves
import json



broker = cmdbroker.CommandBroker()

while True:
    print("Enter Command")
    x = int(input())
    if x == 0:
        break
    if x == 1:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveForward, 1, 1))
    elif x == 2:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveBackward, 1, 1))
    elif x == 3:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveRight, 1, 1))
    elif x == 4:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveLeft, 1, 1))
    elif x == 5:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveCenter, 1, 1))
    elif x == 6:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.LookHCenter, 1, 1))
    elif x == 7:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.LookLeft, 1, 1))
    elif x == 8:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.LookRight, 1, 1))
    elif x == 9:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.LookUp, 1, 1))
    elif x == 10:
        broker.Send(cmdmoves.MotionCommand(cmdmoves.MotionType.LookDown, 1, 1))
    