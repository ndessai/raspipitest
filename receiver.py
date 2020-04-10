import cmdbroker
import json
import cmdmoves
from robomover import RoboMover
import threading
import socket
import time
import picamera

stoprecording = False

def CameraRecording(name):
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('wb')
    try:
        while not stoprecording:
            camera.start_recording(connection, format='h264')
            camera.wait_recording(60)
            
        camera.stop_recording()
    finally:
        connection.close()
        server_socket.close()


# start camera thread
cameraThread = threading.Thread(target=CameraRecording, args=(1,))
cameraThread.start()

def WaitCameraThread():
    stoprecording = True
    cameraThread.join()

mover = RoboMover()

try:

    broker = cmdbroker.CommandBroker()
    print("Waiting for commands")

    for command in broker.Receive():
        print(command.commandType)
        mover.Move(command)

    mover.Done()
    WaitCameraThread()

except KeyboardInterrupt:
    mover.Done()
    WaitCameraThread()
    


'''
try:
    while True:
        print("Enter Command")
        x = int(input())
        if x == 0:
            mover.Done()
            break
        if x == 1:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveForward, 90, 1))
        elif x == 2:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveBackward, 90, 1))
        elif x == 3:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveRight, .4, .1))
        elif x == 4:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveLeft, .4, .1))
        elif x == 5:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.MoveCenter, 1, 1))
        elif x == 6:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookHCenter, 1, 1))
        elif x == 7:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookLeft, 10, 1))
        elif x == 8:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookRight, 10, 1))
        elif x == 9:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookUp, 10, 1))
        elif x == 10:
            mover.Move(cmdmoves.MotionCommand(cmdmoves.MotionType.LookDown, 10, 1))


except KeyboardInterrupt:
    mover.Done()

'''




