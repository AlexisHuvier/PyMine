class Demo:
    def __init__(self):
        self.factory = None
        print("Demo : INIT.")

    def start(self, factory):
        self.factory = factory
        factory.command_manager.register("demo", self.command_info)
        print("Demo : START. (Factory :", factory, ")")

    def player_joined(self, protocol):
        print("Demo : PLAYER_JOINED. (Protocol :", protocol, ")")

    def player_left(self, protocol):
        print("Demo : PLAYER_LEFT. (Protocol :", protocol, ")")

    def chat_message(self, message):
        print("Demo : CHAT_MESSAGE. (Message :", message, ")")

    def command_info(self, protocol, *args):
        print("Demo : COMMAND_INFO.")
        protocol.core_plugins["chat"].send_to(protocol, "[PLUGIN] Demo Plugin created by LavaPower")


instance = Demo()
