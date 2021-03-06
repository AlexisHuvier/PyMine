from core.packets import ChunkDataPacket, BlockChangePacket, ChangeGameStatePacket
from quarry.types.nbt import RegionFile, TagRoot, TagCompound, TagLongArray
from quarry.types.chunk import PackedArray
from quarry.types.registry import LookupRegistry


class World:
    def __init__(self, protocol):
        self.protocol = protocol

    def player_joined(self):
        self.send_chunk(0, 0)

    def set_block(self, x, y, z, idblock):
        bspacket = BlockChangePacket(self.protocol.buff_type, int(x), int(y), int(z), int(idblock))
        for i in self.protocol.server.players:
            i.send_packet(bspacket.type_, *bspacket.datas)

    def set_weather(self, is_rainning=False):
        cgspacket = ChangeGameStatePacket(self.protocol.buff_type, int(is_rainning)+1)
        for i in self.protocol.server.players:
            i.send_packet(cgspacket.type_, *cgspacket.datas)

    def packet_player_block_placement(self, buff):
        main_hand = buff.unpack_varint() == 0
        x, y, z = buff.unpack_position()
        face = buff.unpack_varint()
        crx, cry, crz = buff.unpack("fff")
        self.protocol.server.plugin_manager.call("block_placement", self.protocol, {
            "x": x, "y": y, "z": z, "main_hand": main_hand, "face": face, "crx": crx, "cry": cry, "crz": crz
        })

    def packet_player_digging(self, buff):
        status = buff.unpack_varint()
        x, y, z = buff.unpack_position()
        face = buff.unpack_varint()
        functions = ["start_digging", "cancel_digging", "finish_digging", "drop_item_stack", "drop_item",
                     "shoot_arrow|finish_eating", "swap_hand"]
        args = []

        if status in (0, 1, 2):
            for i in [x, y, z, face]:
                args.append(i)
            if status == 2 and self.protocol.infos.gamemode != 1:
                print("DROP")
        elif status in (3, 4):
            if status == 3:
                print("STACK DROP")
                status = 4
            else:
                print("DROP")
        elif status == 5:
            functions[5] = functions[5].split("|")[0]

        self.protocol.server.plugin_manager.call(functions[status], self.protocol, *args)

    def send_chunk(self, x, z):
        emptyHeight = TagRoot({"": TagCompound({
            "MOTION_BLOCKING": TagLongArray(PackedArray.empty_height())
        })})
        try:
            cdpacket = ChunkDataPacket(self.protocol.buff_type, x, z, False, emptyHeight, [None]*16, [1]*256, [])
            self.protocol.send_packet(cdpacket.type_, *cdpacket.datas)
        except ValueError:
            pass
