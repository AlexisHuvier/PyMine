class Demo:
    def __init__(self):
        print("Demo : INIT.")

    def start(self, server):
        server.command_manager.register("demo", self.command_info, "Info du plugin Demo")
        print("Demo : START. (Server :", server, ")")

    def player_joined(self, player):
        print("Demo : PLAYER_JOINED. (Player :", player, ")")

    def player_left(self, player):
        print("Demo : PLAYER_LEFT. (Player :", player, ")")

    def chat_message(self, message):
        print("Demo : CHAT_MESSAGE. (Message :", message, ")")

    def block_placement(self, player, block_info):
        print("Demo : BLOCK_PLACEMENT. (Player :", player, ". Info :", block_info, ")")

    def use_item(self, player, hand):
        print("Demo : USE_ITEM. (Player :", player, ". Hand :", hand, ")")

    def command_info(self, ctx, *args):
        print("Demo : COMMAND_INFO.")
        ctx.chat.send_to(ctx.player, "[PLUGIN] Demo Plugin created by LavaPower")


instance = Demo()
