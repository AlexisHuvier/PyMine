from quarry.net.server import ServerProtocol
from Core.Plugins import Player, ServerUtils, Chat, World
from Core.Packets import KeepAlivePacket


class Protocol(ServerProtocol):
    def __init__(self, factory, remote_addr):
        super(Protocol, self).__init__(factory, remote_addr)
        self.core_plugins = {
            "chat": Chat(self),
            "player": Player(self),
            "server": ServerUtils(self),
            "world": World(self)
        }
        
    def player_joined(self):
        super(Protocol, self).player_joined()
        self.core_plugins["player"].player_joined()
        self.core_plugins["world"].player_joined()
        self.core_plugins["chat"].send_to_all(self.display_name+" a rejoin.")

        self.ticker.add_loop(20, self.update_keep_alive)

    def player_left(self):
        super(Protocol, self).player_left()
        self.core_plugins["chat"].send_to_all(self.display_name+" a quitté.")

    def update_keep_alive(self):
        kpacket = KeepAlivePacket(self.buff_type)
        self.send_packet(kpacket.type_, *kpacket.datas)

    def packet_received(self, buff, name):
        buff.save()
        method_name = "packet_%s" % name
        for plugin in self.core_plugins.values():
            handler = getattr(plugin, method_name, None)
            if handler:
                try:
                    handler(buff)
                    assert len(buff) == 0, "Packet too long: %s" % method_name
                except Exception as e:
                    self.logger.exception(e)
                buff.restore()
        super(Protocol, self).packet_received(buff, name)
