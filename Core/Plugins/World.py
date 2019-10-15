from Core.Packets import ChunkDataPacket


class World:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        for x in range(0, 2):
            for z in range(0, 2):
                self.send_chunk(x, z)

    def packet_player_block_placement(self, buff):
        main_hand = buff.unpack_varint() == 0
        x, y, z = buff.unpack_position()
        face = buff.unpack_varint()
        crx, cry, crz = buff.unpack("fff")
        self.protocol.server.plugin_manager.call("block_placement", self.protocol, {
            "x": x, "y": y, "z": z, "main_hand": main_hand, "face": face, "crx": crx, "cry": cry, "crz": crz
        })

    def send_chunk(self, x, z):
        try:
            cdpacket = ChunkDataPacket(self.protocol, "r.0.0.mca", 0, 0, x, z)
            self.protocol.send_packet(cdpacket.type_, *cdpacket.datas)
        except ValueError:
            pass
