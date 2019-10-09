class Packet:
    def __init__(self, buff, type_, infos):
        self.type_ = type_
        self.infos = infos
        self.buff = buff
        self.datas = self.get_datas()

    def get_datas(self):
        liste = []
        for i in self.infos:
            if i[0] == "chat":
                liste.append(self.buff.pack_chat(i[1]))
            elif i[0] == "pack":
                liste.append(self.buff.pack(*i[1:]))
            elif i[0] == "int":
                liste.append(self.buff.pack_varint(i[1]))
            elif i[0] == "str":
                liste.append(self.buff.pack_string(i[1]))
            elif i[0] == "position":
                liste.append(self.buff.pack_position(i[1], i[2], i[3]))
            elif i[0] == "json":
                liste.append(self.buff.pack_json(i[1]))
            elif i[0] == "chunk_bitmask":
                liste.append(self.buff.pack_chunk_bitmask(i[1]))
            elif i[0] == "nbt":
                liste.append(self.buff.pack_nbt(i[1]))
            elif i[0] == "chunk":
                liste.append(self.buff.pack_chunk(i[1], i[2]))
            elif i[0] == "list_nbt":
                liste.append(b"".join(self.buff.pack_nbt(entity) for entity in i[1]))
            else:
                raise TypeError("Unknown data type : "+i[0])
        return liste

