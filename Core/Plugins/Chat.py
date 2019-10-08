from Core.Packets import ChatMessagePacket


class Chat:
    def __init__(self, protocol):
        self.protocol = protocol

    def packet_chat_message(self, buff):
        message = buff.unpack_string()
        self.send_to_all("<{}> {}".format(self.protocol.display_name, message))

    def send_to_all(self, message):
        cpacket = ChatMessagePacket(self.protocol.buff_type, message)
        for player in self.protocol.factory.players:
            player.send_packet(cpacket.type_, *cpacket.datas)
