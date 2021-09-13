# I did not write this specific program; Genwald did
# Check out his Github profile at https://github.com/Genwald
# Additionally, this program (nus3volume.py) can be found at https://gist.github.com/Genwald/d4e39d5ccc9e98266914efd1a2e4e813

import struct

def round_up_to_multiple(value, multiple):
    mod = value%multiple
    if mod == 0:
        return value
    return value + multiple - mod
    
def read_offset(file, offset, size):
    file.seek(offset)
    return file.read(size)
    
def read_int(file, offset, endian):
    return int.from_bytes(read_offset(file, offset, 4), endian)
    
def read_int_byte(file, offset):
    return int.from_bytes(read_offset(file, offset, 1), "little")
    
def read_float_little(file, offset):
    return struct.unpack('<f', read_offset(file, offset, 4))[0]
    
def write_float_little(file, offset, value):
    bytes = struct.pack('<f', value)
    file.seek(offset)
    file.write(bytes)

class InvalidMagic(Exception):
    pass
    
class UnsupportedEntry(Exception):
    pass
    
class BankReader:
    def _get_tone_offset(self):
        toc_size = read_int(self.file, 0x10, "little")
        chunk_count = read_int(self.file, 0x14, "little")
        total_offset = 0x14 + toc_size
        for i in range(chunk_count):
            chunk_size = read_int(self.file, 0x18+(i*8)+4, "little")
            if read_offset(self.file, 0x18+(i*8), 4) == b"TONE":
                return 8+total_offset
            total_offset += 0x08 + chunk_size
            
    def _get_entry_count(self):
        return read_int(self.file, self.tone_offset, "little")

    def __init__(self, file):
        self.file = file
        if(read_offset(self.file, 0, 4) != b"NUS3" 
        or read_offset(self.file, 8, 4) != b"BANK"
        or read_offset(self.file, 12, 4) != b"TOC "):
            raise InvalidMagic
        self.tone_offset = self._get_tone_offset()
        self.entry_count = self._get_entry_count()
        
    def _get_name_offset(self, idx):
        tone_header_offset = read_int(self.file, self.tone_offset+4+(idx*8), "little")
        #tone_header_size  = read_int(self.file, self.tone_offset+4+(idx*8)+4, "little")
        entry_offset = self.tone_offset+tone_header_offset
        flags = read_int_byte(self.file, entry_offset+7)
        name_size_offset = entry_offset + 8
        if flags & 0x80:
            name_size_offset += 4
        name_offset = name_size_offset + 1
        name_size = read_int_byte(self.file, name_size_offset)
        return (name_offset, name_size)

    def _get_volume_offset(self, idx):
        name_offset, name_size = self._get_name_offset(idx)
        unk1_offset = name_offset-1 + round_up_to_multiple(name_size+1, 4) + 0xC
        unk1 = read_int(self.file, unk1_offset, "little")
        # feels a bit hacky
        if unk1 != 0x000022E8:
            return None
        return unk1_offset+4
        
    def set_volume(self, idx, value):
        if idx >= self.entry_count:
            raise IndexError
        offset = self._get_volume_offset(idx)
        if offset == None:
            raise UnsupportedEntry
        write_float_little(self.file, offset, value)

    def get_volume(self, idx):
        if idx >= self.entry_count:
            raise IndexError
        offset = self._get_volume_offset(idx)
        if offset == None:
            raise UnsupportedEntry
        return read_float_little(self.file, offset)
        
    def get_name(self, idx):
        if idx >= self.entry_count:
            raise IndexError
        name_offset, name_size = self._get_name_offset(idx)
        return read_offset(self.file, name_offset, name_size).decode()

def main():
    import sys
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("usage: nus3volume.py [path to nus3bank] [idx] [new value (optional)]")
        return
        
    path = sys.argv[1]
    idx = int(sys.argv[2])
    if len(sys.argv) == 4:
        new_val = float(sys.argv[3])
    else:
        new_val = None

    with open(path, mode='r+b') as file:
        try:
            bank = BankReader(file)
        except InvalidMagic:
            print("Invalid Magic\nMust use a nus3bank file")
            return
        
        try:
            name = bank.get_name(idx)
            print(name)
            volume = bank.get_volume(idx)
            print( "current volume: " + str(volume) )
            if new_val != None:
                bank.set_volume(idx, new_val)
                print( "Volume set to " + str(new_val) )
        
        # example unsupported entries in se_common: 460, 303, 404
        except UnsupportedEntry:
            print("This entry type is unsupported")
            return
        except IndexError:
            print("Index out of range")
            return
        

if __name__ == "__main__":
    main()