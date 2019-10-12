from Core.Packets import JoinGamePacket, SpawnPositionPacket, PlayerPositionLookPacket, TitlePacket, PlayerListPacket


class Player:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        jpacket = JoinGamePacket(self.protocol.buff_type, gamemode=1)
        self.protocol.send_packet(jpacket.type_, *jpacket.datas)
        self.set_spawn_position(8, 8, 8)
        self.set_position(8, 8, 8)

    def set_spawn_position(self, x, y, z):
        spacket = SpawnPositionPacket(self.protocol.buff_type, x, y, z)
        self.protocol.send_packet(spacket.type_, *spacket.datas)

    def set_position(self, x, y, z):
        plpacket = PlayerPositionLookPacket(self.protocol.buff_type, x=x, y=y, z=z)
        self.protocol.send_packet(plpacket.type_, *plpacket.datas)

    def set_title(self, title, subtitle=""):
        tpacket = TitlePacket(self.protocol.buff_type, title, 0)
        stpacket = TitlePacket(self.protocol.buff_type, subtitle, 1)
        self.protocol.send_packet(tpacket.type_, *tpacket.datas)
        self.protocol.send_packet(stpacket.type_, *stpacket.datas)

    def set_actionbar(self, text):
        tpacket = TitlePacket(self.protocol.buff_type, text, 2)
        self.protocol.send_packet(tpacket.type_, *tpacket.datas)

    def set_player_list_header_footer(self, header="", footer=""):
        plpacket = PlayerListPacket(self.protocol.buff_type, header, footer)
        self.protocol.send_packet(plpacket.type_, *plpacket.datas)


