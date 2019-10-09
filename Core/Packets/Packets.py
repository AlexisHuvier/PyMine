from Core.Packets.Packet import Packet
from quarry.types.nbt import RegionFile, TagRoot
from quarry.types.chunk import BlockArray
import os


class ChatMessagePacket(Packet):
    def __init__(self, buff, message):
        super(ChatMessagePacket, self).__init__(
            buff, "chat_message",
            (
                ("chat", message),
                ("pack", "B", 0)
            )
        )


class JoinGamePacket(Packet):
    def __init__(self, buff, eid=0, gamemode=0, dimension=0, maxplayers=0, level_type="DEFAULT", view=1,
                 reduced_debug=False):
        super(JoinGamePacket, self).__init__(
            buff, "join_game",
            (
                ("pack", "iBiB", eid, gamemode, dimension, maxplayers),
                ("str", level_type),
                ("int", view),
                ("pack", "?", reduced_debug)
            )
        )


class SpawnPositionPacket(Packet):
    def __init__(self, buff, x=0, y=0, z=0):
        super(SpawnPositionPacket, self).__init__(
            buff, "spawn_position",
            (("position", x, y, z),)
        )


class PlayerPositionLookPacket(Packet):
    def __init__(self, buff, x=0, y=255, z=0, yaw=0, pitch=0):
        super(PlayerPositionLookPacket, self).__init__(
            buff, "player_position_and_look",
            (
                ("pack", "dddff?", x, y, z, yaw, pitch, 0b00000),
                ("int", 0)
            )
        )


class KeepAlivePacket(Packet):
    def __init__(self, buff):
        super(KeepAlivePacket, self).__init__(
            buff, "keep_alive", (("pack", "Q", 0),)
        )


class StatusResponsePacket(Packet):
    def __init__(self, buff, data):
        super(StatusResponsePacket, self).__init__(
            buff, "status_response", (("json", data), )
        )


class ChunkDataPacket(Packet):
    def __init__(self, protocol, file, x, z):
        file = RegionFile(os.path.join(os.path.dirname(__file__), "..", "World", "regions", file))
        self.infos = file.load_chunk(x, z).body.value["Level"].value
        full = self.infos["Status"].value == 'full'
        sections = [None] * 16
        for section in self.infos["Sections"].value:
            if 'Palette' in section.value:
                y = section.value["Y"].value
                blocks = BlockArray.from_nbt(section, protocol.factory.registry)
                block_light = None
                sky_light = None
                sections[y] = (blocks, block_light, sky_light)
        heightmap = TagRoot.from_body(self.infos["Heightmaps"])
        biomes = self.infos["Biomes"].value
        blocks_entities = self.infos["TileEntities"].value
        super(ChunkDataPacket, self).__init__(protocol.buff_type, "chunk_data", (
            ("pack", "ii?", x, z, full),
            ("chunk_bitmask", sections),
            ("nbt", heightmap),
            ("chunk", sections, biomes),
            ("int", len(blocks_entities)),
            ("list_nbt", blocks_entities)
        ))
