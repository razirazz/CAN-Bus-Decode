import struct

byte_data = [181, 4, 45, 0, 67, 0, 0, 129]

# Define the format based on the data type and arrangement
format_string = 'BBBBBBBB'  # B represents unsigned char (1 byte)

# Unpack the bytes
unpacked_data = struct.unpack(format_string, bytes(byte_data))

# Print the unpacked data
print(unpacked_data)