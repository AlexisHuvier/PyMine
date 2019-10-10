from Core.Packets import JoinGamePacket, SpawnPositionPacket, PlayerPositionLookPacket


class Player:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        jpacket = JoinGamePacket(self.protocol.buff_type, gamemode=1)
        self.protocol.send_packet(jpacket.type_, *jpacket.datas)
        spacket = SpawnPositionPacket(self.protocol.buff_type)
        self.protocol.send_packet(spacket.type_, *spacket.datas)
        plpacket = PlayerPositionLookPacket(self.protocol.buff_type, x=8, y=8, z=8)
        self.protocol.send_packet(plpacket.type_, *plpacket.datas)
