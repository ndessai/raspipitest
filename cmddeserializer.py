from cmdmoves import CommandType, MotionType, MotionCommand, StartCommand, StopCommand 

class CommandDeserializer:

    def Deserialize(self, dict):
        if dict['commandType'] == CommandType.Start:
            return StartCommand()
        elif dict['commandType'] == CommandType.Stop:
            return StopCommand()
        elif dict['commandType'] == CommandType.Motion:
            cmd = MotionCommand()
            cmd.FromDict(dict)
            return cmd