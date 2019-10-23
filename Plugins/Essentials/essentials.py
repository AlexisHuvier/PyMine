from twisted.internet import reactor


class Essentials:
    def start(self, server):
        commands = [
            ["essentials", self.command_info, "Information sur le plugin Essentials"],
            ["help", self.command_help, "Liste des commandes"],
            ["stop", self.command_stop, "Arrête le serveur", 1],
            ["tp", self.command_tp, "Se téléporter à des coordonnées", 1],
            ["broadcast", self.command_broadcast, "Faire une annonce globale", 1],
            ["plugins", self.command_plugins, "Liste des plugins installés"],
            ["kick", self.command_kick, "Ejecte quelqu'un du server", 1],
            ["heal", self.command_heal, "Donne toute sa vie et sa bouffe à un joueur", 1],
            ["setblock", self.command_setblock, "Définis un bloc", 1],
            ["weather", self.command_weather, "Définis la météo", 1],
            ["gamemode", self.command_gamemode, "Change son mode de jeu", 1],
            ["exp", self.command_exp, "Définis son nombre d'expérience", 1]
        ]
        for command in commands:
            server.command_manager.register(*command)

    def player_joined(self, player):
        player.set_player_list_header_footer("Serveur PyMine", "Réalisé par LavaPower")

    def command_exp(self, ctx, *args):
        if len(args) == 2:
            if args[0].isnumeric() and args[1].isnumeric():
                ctx.player.set_experience(int(args[0]), int(args[1]))
                ctx.chat.send_to(ctx.player, "Expérience modifiée")
            else:
                ctx.chat.send_to(ctx.player, "Usage : /exp <level> <exp>")
        elif len(args) == 3:
            for player in ctx.players:
                if player.display_name == args[0]:
                    if args[1].isnumeric() and args[2].isnumeric():
                        ctx.chat.send_to(ctx.player, "Changement de l'expérience de "+player.display_name)
                        ctx.player = player
                        self.command_exp(ctx, *args[1:])
                    else:
                        ctx.chat.send_to(ctx.player, "Usage : /exp "+args[0]+" <level> <exp>")
                    return
            ctx.chat.send_to(ctx.player, "Joueur introuvable")
        else:
            ctx.chat.send_to(ctx.player, "Usage : /exp <level> <exp>")

    def command_weather(self, ctx, *args):
        if len(args):
            if args[0] == "clear":
                ctx.world.set_weather(False)
                ctx.chat.send_to(ctx.player, "La pluie s'arrête.")
            elif args[0] == "rain":
                ctx.world.set_weather(True)
                ctx.chat.send_to(ctx.player, "La pluie commence.")
        else:
            ctx.chat.send_to(ctx.player, "Usage : /weather <clear|rain>")

    def command_gamemode(self, ctx, *args):
        if len(args) == 1:
            if args[0].isnumeric():
                gm = int(args[0])
                if 0 <= gm <= 3:
                    ctx.player.set_gamemode(gm)
                    ctx.chat.send_to(ctx.player, "Mode de jeu changé pour : " + args[0] + ".")
                else:
                    ctx.chat.send_to(ctx.player, "Mode de jeu inconnu.")
            else:
                ctx.chat.send_to(ctx.player, "Mode de jeu inconnu.")
        elif len(args) == 2:
            for player in ctx.players:
                if player.display_name == args[0]:
                    if args[1].isnumeric():
                        ctx.chat.send_to(ctx.player, "Changement du mode de jeu de "+player.display_name)
                        ctx.player = player
                        self.command_gamemode(ctx, args[1])
                    else:
                        ctx.chat.send_to(ctx.player, "Mode de jeu inconnu.")
                    return
            ctx.chat.send_to(ctx.player, "Joueur introuvable")
        else:
            ctx.chat.send_to(ctx.player, "Usage : /gamemode <0|1|2|3>")

    def command_setblock(self, ctx, *args):
        if len(args) == 4:
            ctx.world.set_block(*args)
            ctx.chat.send_to(ctx.player, "Bloc changé.")
        else:
            ctx.chat.send_to(ctx.player, "Usage : /setblock <x> <y> <z> <id>")

    def command_heal(self, ctx, *args):
        if len(args):
            name = args[0]
            for i in ctx.players:
                if i.display_name == name:
                    i.set_health_food()
                    ctx.chat.send_to(ctx.player, "Joueur soigné : "+name)
                    ctx.chat.send_to(i, ctx.player.display_name + " t'a soigné")
                    return
            ctx.chat.send_to(ctx.player, "Joueur introuvable : "+name)
        else:
            ctx.player.set_heath_food()
            ctx.chat.send_to(ctx.player, "Tu t'es soigné")

    def command_kick(self, ctx, *args):
        if len(args):
            name = args[0]
            reason = " ".join(args[1:])
            if reason == "":
                reason = "Tu as été kick sans raison."
            else:
                reason = "Tu as été kick pour : "+reason
            for i in ctx.players:
                if i.display_name == name:
                    i.disconnect(reason)
                    return
            ctx.chat.send_to(ctx.player, "Joueur introuvable : "+name)
        else:
            ctx.chat.send_to(ctx.player, "Usage : /kick <name> [reason]")

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
        numperpage = 6

        if len(args) == 0:
            page = 1
        else:
            page = int(args[0])

        maxpage = len(ctx.player.server.command_manager.commands) // numperpage
        if len(ctx.player.server.command_manager.commands) % numperpage:
            maxpage += 1

        if page > maxpage:
            ctx.chat.send_to(ctx.player, "Page introuvable. Page maximum : "+str(maxpage))
            return

        ctx.chat.send_to(ctx.player, "==============================")
        ctx.chat.send_to(ctx.player, "Liste des commandes : "+str(page)+"/"+str(maxpage))
        ctx.chat.send_to(ctx.player, "==============================")

        for i in range(numperpage):
            try:
                command = ctx.player.server.command_manager.commands[numperpage * (page-1) + i]
                if command.permission:
                    ctx.chat.send_to(ctx.player, "{} : {} (STAFF)".format(command.name, command.description))
                else:
                    ctx.chat.send_to(ctx.player, "{} : {}".format(command.name, command.description))
            except IndexError:
                ctx.chat.send_to(ctx.player, "")
        ctx.chat.send_to(ctx.player, "==============================")

    def command_stop(self, ctx, *args):
        ctx.chat.send_to_all("[PLUGIN] Fermeture du serveur")
        ctx.player.logger.info("Close server")
        reactor.removeAll()
        reactor.iterate()
        reactor.stop()


instance = Essentials()
