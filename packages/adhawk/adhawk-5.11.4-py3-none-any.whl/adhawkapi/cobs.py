""" Implementations of helper classes for encoding and decoding """

from .com import InvalidLengthError


class COBSCodec():
    """ Helper class for encoding and decoding frames"""

    @staticmethod
    def encode(packet_data):
        """ Encode one packet and return COBS encoded frame, appending an EOF character """
        serial_data = [0]
        zero_pointer = 0
        for i, byte in enumerate(packet_data):
            if byte == 0:
                # have the previous zero pointer point to this
                serial_data[zero_pointer] = (i + 1) - zero_pointer
                # mark this as the new zero pointer
                serial_data.append(0)
                zero_pointer = i + 1
            else:
                serial_data.append(byte)
        # stuff in the last zero, and have the last zero pointer point to it
        serial_data.append(0)
        serial_data[zero_pointer] = (len(serial_data) - 1) - zero_pointer
        return serial_data

    @staticmethod
    def partial_decode(data, partial_len):
        '''Decode one frame up to the specified partial length

        Returns:
            decoded contents, not including the EOF character
        '''
        copydata = list(data[:partial_len + 1])
        zero_pointer = copydata[0]
        while zero_pointer < len(copydata):
            next_zero_pointer = zero_pointer + copydata[zero_pointer]
            copydata[zero_pointer] = 0
            zero_pointer = next_zero_pointer
        # remove the first zero pointer
        return bytes(copydata[1:])

    @staticmethod
    def decode(serial_data):
        """ Decode one frame and return its contents, not including the EOF character """
        # decode all the zeros
        serial_data = list(serial_data)
        zero_pointer = serial_data[0]
        while zero_pointer < len(serial_data):
            next_zero_pointer = zero_pointer + serial_data[zero_pointer]
            serial_data[zero_pointer] = 0
            zero_pointer = next_zero_pointer
        if zero_pointer != len(serial_data):
            raise InvalidLengthError('Malformed COBS packet')
        # remove the first zero pointer
        return bytes(serial_data[1:])
