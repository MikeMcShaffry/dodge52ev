import can

with can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000) as bus:
    msg = can.Message(arbitration_id=0x7de, data=[0, 25, 0, 1, 3, 1, 4, 1])
    bus.send(msg)

