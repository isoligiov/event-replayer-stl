def two_bytes_to_signed_int(high_byte, low_byte):
    # Combine high and low bytes to form a 16-bit integer
    combined = (high_byte << 8) | low_byte
    # Convert to signed integer
    signed_int = combined if combined < 32768 else combined - 65536
    return signed_int

def byte_to_signed_int(byte):
    if byte > 127:
        return byte - 256
    else:
        return byte