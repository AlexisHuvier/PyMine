class Command:
    def __init__(self, plugin, name, function,  description="", permission=0):
        self.name = name
        self.function = function
        self.permission = permission
        self.description = description
        self.plugin = plugin

    def execute(self, ctx, *args):
        if self.permission == 1 and not ctx.is_op(ctx.player.display_name):
            ctx.chat.send_to(ctx.protocol, "Vous n'êtes pas op.")
        else:
            self.function(ctx, *args)


class CommandContext:
    def __init__(self, player):
        self.player = player
        self.chat = player.chat
        self.server_utils = player.server_utils
        self.world = player.world
        self.players = player.factory.players
        self.server = player.factory

    def is_op(self, username):
        if username in self.player.server.command_manager.ops:
            return True
        return False


class CommandManager:
    def __init__(self, factory):
        self.factory = factory
        self.commands = []
        self.ops = factory.config.get("ops", [])

    def register(self, plugin, command, function, description="", permission=0):
        for i in self.commands:
            if i.name == command:
                self.factory.logger.warning("Command already exist : "+command)
                return
        self.commands.append(Command(plugin, command, function, description, permission))

    def unregister(self, command):
        for k, v in enumerate(self.commands):
            if v.name == command:
                del self.commands[k]
                self.factory.logger.info("Unregister command : "+command)
                return True
        self.factory.logger.warning("Unregister unknown command : "+command)
        return False

    def unregister_plugin(self, plugin):
        for i in self.commands:
            if i.plugin == plugin:
                self.unregister(i.name)

    def call_command(self, protocol, message):
        command, *args = message.split(" ")
        for i in self.commands:
            if i.name == command:
                i.execute(CommandContext(protocol), *args)
                return
        protocol.chat.send_to(protocol, self.factory.config.get("messages.command_not_exist",
                                                                "La commande {} n'existe pas.").format(command))
