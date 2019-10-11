from Core.Packets import ChatMessagePacket


class Chat:
    def __init__(self, protocol):
        self.protocol = protocol

    def packet_chat_message(self, buff):
        message = buff.unpack_string()
            self.send_to_all(self.protocol.factory.config.get("messages.chat_format", "<{}> {}")
                             .format(self.protocol.display_name, message))

    def send_to_all(self, message):
        for player in self.protocol.factory.players:
            self.send_to(player, message)

    def send_to(self, player, message):
        cpacket = ChatMessagePacket(self.protocol.buff_type, message)
        player.send_packet(cpacket.type_, *cpacket.datas)
