import serial
import crcmod
import struct

# COM port configuration
RelayCOMPort = 'COM8'

# all relay on/off command
allRelayOn = '01 06 00 34 00 01 09 C4'
allRelayOff = '01 06 00 34 00 00 C8 04'

class ZsRelay:
    def __init__(self, baudrate: int, serialPort: str, devPos: int):
        self.baudrate = baudrate
        self.serialPort = serialPort
        self.devPos = devPos

    def openSerial(self):
        self.serialPort = serial.Serial(self.serialPort, self.baudrate, timeout=1)
        return self.serialPort

    def closeSerial(self):
        self.serialPort.close()
        return self.serialPort
    
    def writeByte(self, command:bytes):
        self.serialPort.write(command)
        response = self.serialPort.read(self.serialPort.in_waiting)
        return response
    
    def switchCommand(self, relayAddress: int, relayState: int) -> bytes:
        devicePosition = self.devPos.to_bytes(1, byteorder='big')
        relayAddress = relayAddress.to_bytes(2, byteorder='big')
        relayState = relayState.to_bytes(2, byteorder='big')
        command = devicePosition + b'\x06' + relayAddress + relayState
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        crc_result = crc16(command)
        crc_result = struct.pack("<H", crc_result)
        full_command = command + crc_result
        return full_command

# def _openSerial(COM: str):
#     serialPort = serial.Serial(COM, 38400, timeout=1)
#     return serialPort

# def _closeSerial(serialPort: str):
#     serialPort.close()

# def crc16Modbus(command: bytes) -> bytes:
#     """
#     CRC16 Modbus calculation function
#     """
#     crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
#     crc_result = crc16(command)
#     crc_result = struct.pack("<H", crc_result)
#     return crc_result



# def _switchCommand(devicePosition: int, relayAddress: int, relayState: int) -> bytes:
#     """
#     default device position is 01 
#     on and off action is 06
#     relay address consist of 2 bytes i.e., 00 01 for channel 2
#     the next 2 bytes are the on and off state i.e., 00 00 for off and 00 01 for on
#     the last 2 bytes are the CRC-16 Modbus
#     the function takes in hex string for device position, relay address and relay state
#     the function returns a  command
#     """
#     devicePosition = devicePosition.to_bytes(1, byteorder='big')
#     relayAddress = relayAddress.to_bytes(2, byteorder='big')
#     relayState = relayState.to_bytes(2, byteorder='big')
#     command = devicePosition + b'\x06' + relayAddress + relayState
#     crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
#     crc_result = crc16(command)
#     crc_result = struct.pack("<H", crc_result)
#     full_command = command + crc_result
#     return full_command

# def writeByteSerial(serialPort: str, command: bytes) -> bytes:
#     serialPort.write(command)
#     response = serialPort.read(serialPort.in_waiting or 1)
#     return response