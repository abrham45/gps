import asyncio
import struct

def parse_codec8_packet(data):
    """ Parses Codec 8 binary packet """
    if len(data) < 12:
        return None, None  # Invalid packet

    codec_id = data[4]  # Codec ID should be 0x08
    record_count = data[5]  # Number of records

    if codec_id != 0x08:
        return None, None  # Invalid codec

    # Extract Timestamp (8 bytes)
    timestamp = struct.unpack(">Q", data[6:14])[0]

    # Extract GPS data
    latitude = struct.unpack(">i", data[14:18])[0] / 10000000.0
    longitude = struct.unpack(">i", data[18:22])[0] / 10000000.0
    speed = struct.unpack(">H", data[22:24])[0]  # Speed in km/h

    parsed_data = {
        "timestamp": timestamp,
        "latitude": latitude,
        "longitude": longitude,
        "speed": speed
    }

    return parsed_data, record_count

async def handle_client(reader, writer):
    """ Handles GPS tracker connection """
    try:
        data = await reader.read(1024)  # Read incoming binary packet
        if not data:
            return

        parsed_data, record_count = parse_codec8_packet(data)

        if parsed_data:
            print(f"Received GPS Data: {parsed_data}")  # Print to terminal

            # Send ACK response (Codec ID + Record Count)
            response = struct.pack(">BB", 0x08, record_count)
            writer.write(response)
            await writer.drain()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        writer.close()

async def start_server():
    """ Starts the AsyncIO TCP Server """
    server = await asyncio.start_server(handle_client, "0.0.0.0", 5055)
    print("TCP Server listening on port 5055...")

    async with server:
        await server.serve_forever()

# Run the TCP server
asyncio.run(start_server())
