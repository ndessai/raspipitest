import json
from json import JSONEncoder
from azure.servicebus import QueueClient, Message
from cmdmoves import CommandType, MotionType, MotionCommand
from cmddeserializer import CommandDeserializer

connstr = 'Endpoint=sb://picarbus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=xep/GfmBwhJeXbxY6ppddqjCi7D/K9z/SOOmQHOg8U0='
queue = 'commands'

class CommandEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

class CommandBroker:

    def Send(self, command):
        # Create the QueueClient
        queue_client = QueueClient.from_connection_string(connstr, queue)

        # Send a test message to the queue
        msg = Message(json.dumps(command, indent=4, cls=CommandEncoder))
        queue_client.send(msg)

    def Receive(self):
        # Create the QueueClient
        queue_client = QueueClient.from_connection_string(connstr, queue)

        # Receive the message from the queue
        cmd = MotionCommand(MotionType.NoMotion)
        with queue_client.get_receiver() as queue_receiver:
            while cmd.commandType != CommandType.Stop :
                messages = queue_receiver.fetch_next(timeout=3)
                for message in messages:
                    message.complete()
                    cmd = CommandDeserializer().DeserializeCommand(json.loads(str(message)))
                    yield cmd