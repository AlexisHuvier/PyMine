from twisted.internet import reactor


class Essentials:
    def start(self, factory):
        commands = {
            "essentials": self.command_info,
            "help": self.command_help,
            "stop": self.command_stop,
            "tp": self.command_tp,
            "broadcast": self.command_broadcast
        }
        for k, v in commands.items():
            factory.command_manager.register(k, v)

    def command_info(self, ctx, *args):
        ctx.chat.send_to(ctx.protocol, "[PLUGIN] Essentials Plugin created by LavaPower")

    def command_broadcast(self, ctx, *args):
        if len(args):
            ctx.chat.send_to_all("[SERVER] : " + " ".join(args))
        else:
            ctx.chat.send_to(ctx.protocol, "Usage : /broadcast <message>")

    def command_tp(self, ctx, *args):
        if len(args) == 3:
            if args[0].isnumeric() and args[1].isnumeric() and args[2].isnumeric():
                ctx.player.set_position(int(args[0]), int(args[1]), int(args[2]))
                ctx.chat.send_to(ctx.protocol, "Téléportation effectuée")
            else:
                ctx.chat.send_to(ctx.protocol, "Usage : /tp <x> <y> <z>")
        else:
            ctx.chat.send_to(ctx.protocol, "Usage : /tp <x> <y> <z>")

    def command_help(self, ctx, *args):
        for i in ctx.protocol.factory.command_manager.commands.keys():
            ctx.chat.send_to(ctx.protocol, i)

    def command_stop(self, ctx, *args):
        ctx.chat.send_to_all("[PLUGIN] Fermeture du serveur")
        ctx.protocol.logger.info("Close server")
        reactor.removeAll()
        reactor.iterate()
        reactor.stop()


instance = Essentials()
