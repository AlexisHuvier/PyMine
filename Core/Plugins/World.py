from Core.Packets import ChunkDataPacket


class World:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        self.send_chunk(0, 0)

    def send_chunk(self, x, z):
        try:
            cdpacket = ChunkDataPacket(self.protocol, "r.0.0.mca", 0, 0, x, z)
            self.protocol.send_packet(cdpacket.type_, *cdpacket.datas)
        except ValueError:
            pass
