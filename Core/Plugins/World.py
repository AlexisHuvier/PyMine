from Core.Packets import ChunkDataPacket


class World:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        self.send_region(0, 0)

    def send_region(self, x, z):
        for i in range(0, 6):
            for j in range(0, 6):
                try:
                    cdpacket = ChunkDataPacket(self.protocol, "r."+str(x)+"."+str(z)+".mca", i, j)
                    self.protocol.send_packet(cdpacket.type_, *cdpacket.datas)
                except ValueError:
                    pass
