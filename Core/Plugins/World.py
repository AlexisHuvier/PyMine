from Core.Packets import ChunkDataPacket


class World:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        for x in range(0, 2):
            for z in range(0, 2):
                self.send_chunk(x, z)

    def send_chunk(self, x, z):
        try:
            cdpacket = ChunkDataPacket(self.protocol, "r.0.0.mca", 0, 0, x, z)
            self.protocol.send_packet(cdpacket.type_, *cdpacket.datas)
        except ValueError:
            pass
