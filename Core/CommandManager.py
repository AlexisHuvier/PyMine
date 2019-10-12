class Command:
    def __init__(self, name, function,  description="", permission=0):
        self.name = name
        self.function = function
        self.permission = permission
        self.description = description

    def execute(self, ctx, *args):
        if self.permission == 1 and not ctx.is_op(ctx.protocol.display_name):
            ctx.chat.send_to(ctx.protocol, "Vous n'êtes pas op.")
        else:
            self.function(ctx, *args)


class CommandContext:
    def __init__(self, protocol):
        self.chat = protocol.core_plugins["chat"]
        self.player = protocol.core_plugins["player"]
        self.protocol = protocol


class CommandManager:
    def __init__(self, factory):
        self.factory = factory
        self.commands = []
        self.ops = factory.config.get("ops", [])

    def register(self, command, function, description="", permission=0):
        for i in self.commands:
            if i.name == command:
                self.factory.logger.warn("Command already exist : "+command)
                return
        self.commands.append(Command(command, function, description, permission))

    def call_command(self, protocol, message):
        command, *args = message.split(" ")
        for i in self.commands:
            if i.name == command:
                i.execute(CommandContext(protocol), *args)
                return
        protocol.core_plugins["chat"].send_to(protocol,
                                              self.factory.config.get("messages.command_not_exist",
                                                                      "La commande {} n'existe pas.").format(command))
