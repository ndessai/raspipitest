class CommandType:
    Start = 'Start'
    Stop = 'Stop'
    Motion = 'Motion'

class MotionType:
    MoveForward = 'MoveForward'
    MoveBackward = 'MoveBackward'
    MoveLeft = 'MoveLeft'
    MoveRight = 'MoveRight'
    MoveCenter = 'MoveCenter'

    LookVCenter = 'LookVCenter'
    LookUp = 'LookUp'
    LookDown = 'LookDown'

    LookHCenter = 'LookHCenter'
    LookRight = 'LookRight'
    LookLeft = 'LookLeft'

    NoMotion = 'NoMotion'

class MotionCommand:
    def __init__(self, motionType = MotionType.NoMotion, speed = 1 , duration = 1):
        self.motionType = motionType
        self.speed = speed
        self.duration = duration
        self.commandType = CommandType.Motion

    def toJson(self):
        return { 
            'commandType': self.commandType, 
            'motionType' : self.motionType,
            'duration' : self.duration,
            'speed' : self.speed
         }
    
    def FromDict(self, dict):
        self.commandType = CommandType.Motion
        self.motionType = dict['motionType']
        self.duration = dict['duration']
        self.speed = dict ['speed']

class StartCommand:
    def __init__(self):
        self.commandType = CommandType.Start

    def toJson(self):
        return { 
            'commandType': CommandType.Start
         }

class StopCommand:
    def __init__(self):
        self.commandType = CommandType.Stop

    def toJson(self):
        return { 
            'commandType': CommandType.Stop
         }