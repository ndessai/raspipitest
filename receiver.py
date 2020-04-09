import commands
import json


broker = commands.CommandBroker()
for command in broker.Receive():
    print(command.commandType)