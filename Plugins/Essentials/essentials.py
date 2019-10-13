from twisted.internet import reactor


class Essentials:
    def start(self, server):
        commands = [
            ["essentials", self.command_info, "Information sur le plugin Essentials"],
            ["help", self.command_help, "Liste des commandes"],
            ["stop", self.command_stop, "Arrête le serveur", 1],
            ["tp", self.command_tp, "Se téléporter à des coordonnées", 1],
            ["broadcast", self.command_broadcast, "Faire une annonce globale", 1],
            ["plugins", self.command_plugins, "Liste des plugins installés"]
        ]
        for command in commands:
            server.command_manager.register(*command)

    def player_joined(self, player):
        player.set_player_list_header_footer("Serveur PyMine", "Réalisé par LavaPower")

    def command_plugins(self, ctx, *args):
        ctx.chat.send_to(ctx.player, "Liste des Plugins")
        ctx.chat.send_to(ctx.player, "=========================")
        for i in ctx.player.server.plugin_manager.plugins:
            ctx.chat.send_to(ctx.player, "{} ({}) : {}".format(i.name, i.version, i.description))
        ctx.chat.send_to(ctx.player, "=========================")

    def command_info(self, ctx, *args):
        ctx.chat.send_to(ctx.player, "[PLUGIN] Essentials Plugin V 1.0 created by LavaPower")

    def command_broadcast(self, ctx, *args):
        if len(args) >= 2:
            if args[0] == "chat":
                ctx.chat.send_to_all("[SERVER] : " + " ".join(args[1:]))
            elif args[0] == "title":
                for i in ctx.players:
                    args = " ".join(args[1:]).split("|")
                    if len(args) == 1:
                        title = args[0]
                        subtitle = ""
                    else:
                        title = args[0]
                        subtitle = "|".join(args[1:])
                    i.set_title(title, subtitle)
            elif args[0] == "actionbar":
                for i in ctx.players:
                    i.set_actionbar(" ".join(args[1:]))
            else:
                ctx.chat.send_to(ctx.player, "Usage : /broadcast <chat-title-actionbar> <message>")
        else:
            ctx.chat.send_to(ctx.player, "Usage : /broadcast <chat-title-subtitle-actionbar> <message>")

    def command_tp(self, ctx, *args):
        if len(args) == 3:
            if args[0].isnumeric() and args[1].isnumeric() and args[2].isnumeric():
                ctx.set_position(int(args[0]), int(args[1]), int(args[2]))
                ctx.chat.send_to(ctx.player, "Téléportation effectuée")
            else:
                ctx.chat.send_to(ctx.player, "Usage : /tp <x> <y> <z>")
        else:
            ctx.chat.send_to(ctx.player, "Usage : /tp <x> <y> <z>")

    def command_help(self, ctx, *args):
        ctx.chat.send_to(ctx.player, "Liste des commandes")
        ctx.chat.send_to(ctx.player, "=========================")
        for i in ctx.player.server.command_manager.commands:
            if i.permission == 0 or ctx.is_op(ctx.player.display_name):
                ctx.chat.send_to(ctx.player, "{} : {}".format(i.name, i.description))
        ctx.chat.send_to(ctx.player, "=========================")

    def command_stop(self, ctx, *args):
        ctx.chat.send_to_all("[PLUGIN] Fermeture du serveur")
        ctx.player.logger.info("Close server")
        reactor.removeAll()
        reactor.iterate()
        reactor.stop()


instance = Essentials()
