import math


class BitGenerator:
    def __init__(self, input):
        self.input = [word for word in input.strip()]
        self.bit_buffer = []
        return

    def next_bit(self, n=1):
        bits = []
        while len(bits) < n:
            if len(self.bit_buffer) == 0 and len(self.input) > 0:
                next_hex = self.input.pop(0)
                next_bits = [x for x in bin(int(next_hex, 16))[2:].zfill(4)]
                self.bit_buffer.extend(next_bits)
            bits.append(self.bit_buffer.pop(0))
        return ''.join(bits)

    def has_next_bit(self):
        return len(self.bit_buffer) > 0 or len(self.input) > 0

    def flush_bit_buffer(self):
        self.bit_buffer = []


class PacketReader:
    def __init__(self, bit_generator):
        self.bit_generator = bit_generator

    def next_packet(self):
        bit_generator = self.bit_generator
        length = 6
        subpackets = []
        version_sum = int(bit_generator.next_bit(3), 2)
        type_id = int(bit_generator.next_bit(3), 2)
        value = 0
        if type_id == 4:
            bytes_buffer = []
            while True:
                group_bit = bit_generator.next_bit()
                bytes_buffer.extend(bit_generator.next_bit(4))
                length += 5
                if group_bit == '0':
                    break
            value = int(''.join(bytes_buffer), 2)
        else:
            length_type_id = bit_generator.next_bit()
            length += 1
            if length_type_id == '0':
                subpackets_length = int(bit_generator.next_bit(15), 2)
                length += 15
                length += subpackets_length
                while subpackets_length > 0:
                    subpacket = self.next_packet()
                    version_sum += subpacket[0]
                    subpackets_length -= subpacket[1]
                    subpackets.append(subpacket)
            else:
                total_subpackets = int(bit_generator.next_bit(11), 2)
                length += 11
                for i in range(0, total_subpackets):
                    subpacket = self.next_packet()
                    version_sum += subpacket[0]
                    length += subpacket[1]
                    subpackets.append(subpacket)

            values = [x[2] for x in subpackets]
            if type_id == 0:
                value = sum(values)
            elif type_id == 1:
                value = math.prod(values)
            elif type_id == 2:
                value = min(values)
            elif type_id == 3:
                value = max(values)
            elif type_id == 5:
                value = 1 if values[0] > values[1] else 0
            elif type_id == 6:
                value = 1 if values[0] < values[1] else 0
            elif type_id == 7:
                value = 1 if values[0] == values[1] else 0

        return (version_sum, length, value)


def solve(puzzle_input):
    packet_reader = PacketReader(BitGenerator(puzzle_input))
    packet = packet_reader.next_packet()

    # part 1
    print(packet[0])

    # part 2
    print(packet[2])

    return


solve("""
420D74C3088043390499ED709E6EB49A5CC4A3A3898B7E0F44011C4CC48AC0119D049B0C500265EB8F615900180910C88129B2F0007C61C4B7F74ED7396B20020A44A4C014D005E5A72E274B4E5C4B96CC3793410078C01D82F1DA08180351661AC1920042A3CC578BA6008F802138D93352B9CFCEF61D3009A7D2268D254925569C02A92D62BF108D52C1B3E4B257B57FAE5C54400A84840267880311D23245F1007A35C79848200C4288FF0E8C01194A4E625E00A4EFEF5F5996486C400C5002800BFA402D3D00A9C4027B98093D602231C00F001D38C009500258057E601324C00D3003D400C7003DC00A20053A6F1DBDE2D4600A6802B37C4B9E872B0E44CA5FF0BFB116C3004740119895E6F7312BCDE25EF077700725B9F2B8F131F333005740169A7F92EFEB3BC8A21998027400D2CDF30F927880B4C62D6CDFFD88EB0068D2BF019A8DAAF3245B39C9CFA1D2DF9C3DB9D3E50A0164BE2A3339436993894EC41A0D10020B329334C62016C8E7A5F27C97D0663982D8EB23C5282529CDD271E8F100AE1401AA80021119E3A4511006E1E47689323585F3AEBF900AEB2B6942BD91EE8028000874238AB0C00010B8D913220A004A73D789C4D54E24816301802538E940198880371AE15C1D1007638C43856C00954C25CD595A471FE9D90056D60094CEA61933A9854E9F3801F2BBC6131001F792F6796ACB40D036605C80348C005F64F5AC374888CA42FD99A98025319EB950025713656F202200B767AB6A30E802D278F81CBA89004CD286360094FC03A7E01640245CED5A3C010100660FC578B60008641C8B105CC017F004E597E596E633BA5AB78B9C8F840C029917C9E389B439179927A3004F003511006610C658A200084C2989D0AE67BD07000606154B70E66DC0C01E99649545950B8AB34C8401A5CDA050043D319F31CB7EBCEE14
""")
