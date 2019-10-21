from quarry.net.server import ServerProtocol
from Core.Plugins import ServerUtils, Chat, World
from Core.Packets import *
from Core.Objects import PlayerInfo

import logging


class Player(ServerProtocol):
    def __init__(self, factory, remote_addr):
        super(Player, self).__init__(factory, remote_addr)
        self.logger.setLevel(logging.ERROR)
        self.chat = Chat(self)
        self.server_utils = ServerUtils(self)
        self.world = World(self)
        self.infos = PlayerInfo()
        self.server = factory

    def player_joined(self):
        super(Player, self).player_joined()
        self.infos.gamemode = 1
        jpacket = JoinGamePacket(self.buff_type, gamemode=self.infos.gamemode)
        self.send_packet(jpacket.type_, *jpacket.datas)
        self.set_spawn_position(8, 8, 8)
        self.set_position(8, 8, 8)
        self.world.player_joined()
        self.chat.send_to_all(
            self.factory.config.get("messages.player_joined", "{} a rejoint le serveur").format(self.display_name))
        self.factory.logger.info(
            self.factory.config.get("messages.player_joined", "{} a rejoint le serveur").format(self.display_name))
        self.factory.plugin_manager.call("player_joined", self)

        self.ticker.add_loop(20, self.update_keep_alive)

    def player_left(self):
        super(Player, self).player_left()
        self.chat.send_to_all(
            self.factory.config.get("messages.player_left", "{} a quitté le serveur").format(self.display_name))
        self.factory.logger.info(
            self.factory.config.get("messages.player_left", "{} a quitté le serveur").format(self.display_name))
        self.factory.plugin_manager.call("player_left", self)

    def update_keep_alive(self):
        kpacket = KeepAlivePacket(self.buff_type)
        self.send_packet(kpacket.type_, *kpacket.datas)

    def packet_received(self, buff, name):
        buff.save()
        method_name = "packet_%s" % name
        for plugin in [self.chat, self.world, self.server_utils]:
            handler = getattr(plugin, method_name, None)
            if handler:
                try:
                    handler(buff)
                except Exception as e:
                    self.logger.exception(e)
                buff.restore()
        super(Player, self).packet_received(buff, name)

    def packet_use_item(self, buff):
        main_hand = buff.unpack_varint() == 0
        self.server.plugin_manager.call("use_item", self, main_hand)

    def set_spawn_position(self, x, y, z):
        spacket = SpawnPositionPacket(self.buff_type, x, y, z)
        self.send_packet(spacket.type_, *spacket.datas)

    def set_position(self, x, y, z):
        self.infos.set_position(x, y, z)
        plpacket = PlayerPositionLookPacket(self.buff_type, x=x, y=y, z=z)
        self.send_packet(plpacket.type_, *plpacket.datas)

    def set_title(self, title, subtitle=""):
        tpacket = TitlePacket(self.buff_type, title, 0)
        stpacket = TitlePacket(self.buff_type, subtitle, 1)
        self.send_packet(tpacket.type_, *tpacket.datas)
        self.send_packet(stpacket.type_, *stpacket.datas)

    def set_actionbar(self, text):
        tpacket = TitlePacket(self.buff_type, text, 2)
        self.send_packet(tpacket.type_, *tpacket.datas)

    def set_player_list_header_footer(self, header="", footer=""):
        plpacket = PlayerListPacket(self.buff_type, header, footer)
        self.send_packet(plpacket.type_, *plpacket.datas)

    def disconnect(self, message=""):
        dpacket = DisconnectPacket(self.buff_type, message)
        self.send_packet(dpacket.type_, *dpacket.datas)

    def set_health_food(self, health=20, food=20, saturation=0.5):
        hfpacket = HealthFoodPacket(self.buff_type, health, food, saturation)
        self.send_packet(hfpacket.type_, *hfpacket.datas)

    def set_gamemode(self, gamemode):
        cgspacket = ChangeGameStatePacket(self.buff_type, 3, gamemode)
        self.send_packet(cgspacket.type_, *cgspacket.datas)
