class Demo:
    def __init__(self):
        self.factory = None
        print("Demo : INIT.")

    def start(self, factory):
        self.factory = factory
        print("Demo : START. (Factory :", factory, ")")

    def player_joined(self, protocol):
        print("Demo : PLAYER_JOINED. (Protocol :", protocol, ")")

    def player_left(self, protocol):
        print("Demo : PLAYER_LEFT. (Protocol :", protocol, ")")

    def chat_message(self, message):
        print("Demo : CHAT_MESSAGE. (Message :", message, ")")



instance = Demo()
