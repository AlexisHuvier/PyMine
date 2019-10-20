class Demo:
    def __init__(self):
        self.logger = None

    def start(self, server):
        server.command_manager.register("demo", self.command_info, "Info du plugin Demo")
        self.logger = server.logger
        self.logger.info("Demo : START. (Server : %s )", server)

    def player_joined(self, player):
        self.logger.info("Demo : PLAYER_JOINED. (Player : %s )", player)

    def player_left(self, player):
        self.logger.info("Demo : PLAYER_LEFT. (Player : %s )", player)

    def chat_message(self, message):
        self.logger.info("Demo : CHAT_MESSAGE. (Message : %s )", message)

    def block_placement(self, player, block_info):
        self.logger.info("Demo : BLOCK_PLACEMENT. (Player : %s. Info : %s )", player, block_info)

    def use_item(self, player, hand):
        self.logger.info("Demo : USE_ITEM. (Player : %s. Hand : %s )", player, hand)

    def start_digging(self, player, x, y, z, face):
        self.logger.info("Demo : START_DIGGING. (Player : %s. Pos : %s. Face : %s )", player, [x, y, z], face)

    def cancel_digging(self, player, x, y, z, face):
        self.logger.info("Demo : CANCEL_DIGGING. (Player : %s. Pos : %s. Face : %s )", player, [x, y, z], face)

    def finish_digging(self, player, x, y, z, face):
        self.logger.info("Demo : FINISH_DIGGING. (Player : %s. Pos : %s. Face : %s )", player, [x, y, z], face)

    def drop_item(self, player):
        self.logger.info("Demo : DROP_ITEM. (Player : %s )", player)

    def shoot_arrow(self, player):
        self.logger.info("Demo : SHOOT_ARROW. (Player : %s )", player)

    def finish_eating(self, player):
        self.logger.info("Demo : FINISH_EATING. (Player : %s )", player)

    def swap_hand(self, player):
        self.logger.info("Demo : SWAP_HAND. (Player : %s )", player)

    def command_info(self, ctx, *args):
        self.logger.info("Demo : COMMAND_INFO.")
        ctx.chat.send_to(ctx.player, "[PLUGIN] Demo Plugin created by LavaPower")


instance = Demo()
