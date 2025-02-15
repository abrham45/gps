import asyncio
import struct
import binascii

def crc16(data: bytes) -> int:
    """Calculate CRC-16/IBM checksum."""
    crc = 0x0000
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x8005
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc

def validate_packet(data: bytes) -> bool:
    """Validate the received packet."""
    if len(data) < 12:
        print("Packet too short.")
        return False

    # Validate preamble (4 bytes)
    if data[:4] != b'\x00\x00\x00\x00':
        print("Invalid preamble.")
        return False

    # Validate Codec ID (1 byte)
    codec_id = data[4]
    if codec_id != 0x08:
        print(f"Invalid Codec ID: {codec_id}. Expected 0x08.")
        return False

    # Validate CRC-16 (last 2 bytes)
    received_crc = struct.unpack(">H", data[-2:])[0]
    calculated_crc = crc16(data[:-2])
    if received_crc != calculated_crc:
        print(f"CRC mismatch: received {received_crc}, calculated {calculated_crc}.")
        return False

    return True

async def handle_client(reader, writer):
    """Handle incoming connections from GPS devices."""
    try:
        data = await reader.read(1024)  # Read incoming binary packet
        if not data:
            print("No data received.")
            return

        if not validate_packet(data):
            print("Invalid packet received.")
            return

        # Process the valid data here
        print(f"Received valid data: {data}")

        # Send ACK response (Codec ID + Record Count)
        record_count = data[5]  # Assuming record count is at index 5
        response = struct.pack(">BB", 0x08, record_count)
        writer.write(response)
        await writer.drain()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        writer.close()
        await writer.wait_closed()

async def start_server():
    """Start the TCP server."""
    server = await asyncio.start_server(handle_client, "0.0.0.0", 5055)
    print("Server started on port 5055.")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_server())
