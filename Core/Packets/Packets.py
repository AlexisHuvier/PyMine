from core.packets.Packet import Packet
from quarry.types.nbt import RegionFile, TagRoot
from quarry.types.chunk import BlockArray
import os


class ExperiencePacket(Packet):
    def __init__(self, buff, exp_bar, level, exp_total):
        super(ExperiencePacket, self).__init__(
            buff, "set_experience",
            (
                ("pack", "f", float(exp_bar)),
                ("int", int(level)),
                ("int", int(exp_total))
            )
        )


class ChangeGameStatePacket(Packet):
    def __init__(self, buff, reason, value=0):
        super(ChangeGameStatePacket, self).__init__(buff, "change_game_state", (
            ("pack", "Bf", int(reason), float(value)),
        ))


class BlockChangePacket(Packet):
    def __init__(self, buff, x, y, z, idblock):
        super(BlockChangePacket, self).__init__(
            buff, "block_change",
            (
                ("position", x, y, z),
                ("int", idblock)
            )
        )


class HealthFoodPacket(Packet):
    def __init__(self, buff, health=20, food=20, saturation=0.5):
        super(HealthFoodPacket, self).__init__(
            buff, "update_health",
            (
                ("pack", "ff", health, saturation),
                ("int", food)
            )
        )


class DisconnectPacket(Packet):
    def __init__(self, buff, message=""):
        super(DisconnectPacket, self).__init__(
            buff, "disconnect",
            (
                ("chat", message),
            )
        )


class PlayerListPacket(Packet):
    def __init__(self, buff, header="", footer=""):
        super(PlayerListPacket, self).__init__(
            buff, "player_list_header_footer",
            (
                ("chat", header),
                ("chat", footer)
            )
        )


class TitlePacket(Packet):
    def __init__(self, buff, text="", position=0):
        super(TitlePacket, self).__init__(
            buff, "title",
            (
                ("int", position),
                ("chat", text)
            )
        )


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
    def __init__(self, buff, eid=0, gamemode=0, dimension=0, level_type = "flat", view = 1):
        super(JoinGamePacket, self).__init__(
            buff, "join_game",
            (
                ("pack", "iBiqB", eid, gamemode, dimension, 0, 0), # Entity ID, GameMode, Dimension, Hashed Seed, MaxPlayers
                ("str", level_type), # Level Type
                ("int", view), # View Distance
                ("pack", "??", False, True) # Reduced DebugInfo, RespawnScreen
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
    def __init__(self, buff, x, z, full, heightmap, sections, biomes, block_entities):
        super(ChunkDataPacket, self).__init__(buff, "chunk_data", (
            ("pack", "ii?", x, z, full),
            ("chunk_bitmask", sections),
            ("nbt", heightmap),
            ("array", "I", biomes),
            ("int", len(buff.pack_chunk(sections))),
            ("chunk", sections),
            ("int", len(block_entities)),
            ("list_nbt", block_entities)
        ))
