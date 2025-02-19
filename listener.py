# import asyncio
# import struct


# def crc16(data: bytes) -> int:
#     """Calculate CRC-16/IBM checksum."""
#     crc = 0x0000
#     for byte in data:
#         crc ^= byte << 8
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x8005
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc


# def validate_packet(data: bytes) -> bool:
#     """Validate the received packet."""
#     if len(data) < 12:
#         print("Packet too short.")
#         return False

#     if data[:4] != b'\x00\x00\x00\x00':
#         print("Invalid preamble.")
#         return False

#     codec_id = data[4]
#     if codec_id != 0x08:
#         print(f"Invalid Codec ID: {codec_id}. Expected 0x08.")
#         return False

#     received_crc = struct.unpack(">H", data[-2:])[0]
#     calculated_crc = crc16(data[:-2])
#     if received_crc != calculated_crc:
#         print(f"CRC mismatch: received {received_crc}, calculated {calculated_crc}.")
#         return False

#     return True


# async def handle_tcp_client(reader, writer):
#     """Handle incoming TCP connections from GPS devices."""
#     try:
#         data = await reader.read(1024)
#         if not data:
#             print("No data received.")
#             return

#         if not validate_packet(data):
#             print("Invalid TCP packet received.")
#             return

#         print(f"Received valid TCP data: {data}")

#         record_count = data[5]
#         response = struct.pack(">BB", 0x08, record_count)
#         writer.write(response)
#         await writer.drain()
#     except Exception as e:
#         print(f"TCP Error: {e}")
#     finally:
#         writer.close()
#         await writer.wait_closed()


# class UDPServer(asyncio.DatagramProtocol):
#     def datagram_received(self, data, addr):
#         """Handle incoming UDP packets."""
#         print(f"Received UDP data from {addr}: {data}")

#         if validate_packet(data):
#             print(f"Received valid UDP data: {data}")
#             record_count = data[5]
#             response = struct.pack(">BB", 0x08, record_count)
#             self.transport.sendto(response, addr)
#         else:
#             print("Invalid UDP packet received.")

#     def connection_made(self, transport):
#         self.transport = transport


# async def start_servers():
#     """Start both TCP and UDP servers."""
#     tcp_server = await asyncio.start_server(handle_tcp_client, "0.0.0.0", 5055)
#     print("TCP server started on port 5055.")

#     loop = asyncio.get_running_loop()
#     udp_transport, _ = await loop.create_datagram_endpoint(UDPServer, local_addr=("0.0.0.0", 5055))
#     print("UDP server started on port 5055.")

#     async with tcp_server:
#         await tcp_server.serve_forever()

#     udp_transport.close()


# if __name__ == "__main__":
#     asyncio.run(start_servers())
