'''Helper tools used by the programmer to load and process programming files'''

import fnmatch
import os

import intelhex
import yaml


HEX_HEADER_ADDRESS = 0x8003800


class Crc8:
    """ Implementation of 8-bit Cyclic Redundancy Check

    Generates CRC8 digests based off a specified generator polynomial
    """
    def __init__(self, generator=0x07):
        self._generator = generator
        self._lut = [0] * 256

        for divident in range(256):
            curbyte = divident
            for _ in range(8):
                if curbyte & 0x80 != 0:
                    curbyte = (curbyte << 1) & 0xFF
                    curbyte = (curbyte ^ generator) & 0xFF
                else:
                    curbyte = (curbyte << 1) & 0xFF
            self._lut[divident] = curbyte

    def digest(self, message):
        """ Calculate the CRC8 digest """
        crc = 0
        for msg in message:
            crc = self._lut[crc ^ msg]
        return crc


def pad_chunk(byte_string, chunk_size):
    """generates a string of varying length to ensure that
    write buffer size of 64-bit is always met"""
    while len(byte_string) < chunk_size:
        byte_string += b'\xff'
    return byte_string


def read_and_format_hex_file(file_name, start_addr, end_addr, chunk_size=256):
    """reads application hex binary and breaks it into chunks"""
    hexfile = intelhex.IntelHex()
    hexfile.loadhex(file_name)
    hexfile.padding = 0x00
    addr_list = [i[1] for i in hexfile.segments() if i[1] < end_addr and i[1] > start_addr]
    if not addr_list:
        return None
    end_address = max(addr_list)
    sector_data = hexfile.tobinarray(start=start_addr, end=end_address - 1)
    chunks = [sector_data[i:i + chunk_size] for i in range(0, len(sector_data), chunk_size)]
    return chunks


def read_header_from_hex_file(file_name):
    """Gets header bytes from given hex file"""
    hexfile = intelhex.IntelHex()
    hexfile.loadhex(file_name)
    try:
        header = hexfile.getsz(HEX_HEADER_ADDRESS)
    except intelhex.NotEnoughDataError:
        return None

    return yaml.safe_load(header)


def read_and_format_binary(file_name, chunk_size=256):
    """reads application binary and breaks it into chunks"""

    file = open(file_name, 'rb')

    count = 0
    chunks = []
    accumulator = b''
    eof = False
    while True:
        for _ in range(0, chunk_size):
            try:
                byte = file.read(1)
                accumulator += byte
            except TypeError:
                break
        if len(accumulator) < chunk_size:
            accumulator = pad_chunk(accumulator, chunk_size)
            eof = True
        chunks.append(accumulator)
        count += 1
        accumulator = b''
        if eof:
            break
    file.close()
    return chunks


def search_for_binary(pattern='*.bin', path="firmware"):
    '''search for the binary file based on the pattern provided'''

    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                relpath = os.path.join(root, name)
                abspath = os.path.abspath(relpath)
                return name, relpath, abspath
    raise FileNotFoundError
