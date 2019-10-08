from Core.Packets import StatusResponsePacket


class ServerUtils:
    def __init__(self, protocol):
        self.protocol = protocol

    def packet_status_request(self, buff):
        protocol_version = self.protocol.factory.force_protocol_version
        if protocol_version is None:
            protocol_version = self.protocol.protocol_version

        d = {
            "description": {
                "text": self.protocol.factory.motd
            },
            "players": {
                "online": len(self.protocol.factory.players),
                "max": self.protocol.factory.max_players
            },
            "version": {
                "name": "PyMine 1.14.4",
                "protocol": protocol_version
            }
        }
        if self.protocol.factory.icon_path is not None:
            print("Not Support favicon")

        spacket = StatusResponsePacket(self.protocol.buff_type, d)
        self.protocol.send_packet(spacket.type_, *spacket.datas)

