class CommandContext:
    def __init__(self, protocol):
        self.chat = protocol.core_plugins["chat"]
        self.player = protocol.core_plugins["player"]
        self.protocol = protocol


class CommandManager:
    def __init__(self, factory):
        self.factory = factory
        self.commands = {}

    def register(self, command, function):
        if command in self.commands.keys():
            self.factory.logger.warn("Command already exist : " + command)
        else:
            self.commands[command] = function

    def call_command(self, protocol, message):
        command, *args = message.split(" ")
        if command in self.commands.keys():
            self.commands[command](CommandContext(protocol), *args)
        else:
            protocol.core_plugins["chat"].send_to(
                protocol,
                self.factory.config.get("messages.command_not_exist", "La commande {} n'existe pas.").format(command))
