from Core.Packets import ChunkDataPacket


class World:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.send_empty_chunk(i, j)

    def send_empty_chunk(self, x, z):
        cdpacket = ChunkDataPacket(self.protocol.buff_type, x=x, z=z)
        self.protocol.send_packet(cdpacket.type_, *cdpacket.datas)