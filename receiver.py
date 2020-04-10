import cmdbroker
import json
import cmdmoves
from robomover import RoboMover

mover = RoboMover()

try:
    while True:
        print("Enter Command")
        x = int(input())
        if x == 0:
            mover.Done()
            break
        if x == 1:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveForward, 50, 1))
        elif x == 2:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveBackward, 50, 1))
        elif x == 3:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveRight, 5, 1))
        elif x == 4:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveLeft, 5, 1))
        elif x == 5:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveCenter, 1, 1))
        elif x == 6:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookHCenter, 1, 1))
        elif x == 7:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookLeft, 1, 1))
        elif x == 8:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookRight, 1, 1))
        elif x == 9:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookUp, 1, 1))
        elif x == 10:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookDown, 1, 1))


except KeyboardInterrupt:
    mover.Done()

'''
try:

    broker = cmdbroker.CommandBroker()
    print("Waiting for commands")

    for command in broker.Receive():
        print(command.commandType)
        mover.Move(command)

    mover.Done()

except KeyboardInterrupt:
    mover.Done()


'''
