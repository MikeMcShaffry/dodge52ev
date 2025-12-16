import can
import cantools
import time

# file = 'EV-can_ZE0.dbc'
file = 'CAR-can_AZE0_fixed.dbc'

# Load the DBC file
try:
    db = cantools.database.load_file(file)
except FileNotFoundError:
    print("Error: {file}% not found. Please place it in the same directory.")
    exit()


def evCan(bus):                    
    print("Listening for LBC messages (SOC, SOH)...")

    while True:
        message = bus.recv()  # Wait for a message

        
        if message.arbitration_id == 0x55B: # LBC SOC message ID
            try:
                decoded_message = db.decode_message(message.arbitration_id, message.data)
                soc = decoded_message.get('LBC_StateOfCharge')
                if soc is not None:
                    print(f"Received LBC SOC: {soc:.1f}%")
            except Exception as e:
                print(f"Error decoding message 0x55B: {e}")

        elif message.arbitration_id == 0x5B3: # LBC SOH message ID
            try:
                decoded_message = db.decode_message(message.arbitration_id, message.data)
                soh = decoded_message.get('SOH')
                if soh is not None:
                    print(f"Received SOH: {soh:.1f}%")
            except Exception as e:
                print(f"Error decoding message 0x5B3: {e}")

def carCan(bus):                    
    print("Listening for CAR-CAN messages ...")
    soh = 0
    gids = 0
    speed = 0
    temp = 0

    while True:
        message = bus.recv()  # Wait for a message
        
        if message.arbitration_id == 0x5B3: # LBC SOH message ID
            try:
                decoded_message = db.decode_message(message.arbitration_id, message.data)
                soh = decoded_message.get('BatteryStateOfHealth')
                gids = decoded_message.get('BatteryGIDS')
                temp = decoded_message.get('BatteryPackTemperature')
            except Exception as e:
                print(f"Error decoding message 0x5B3: {e}")


        elif message.arbitration_id == 0x280: # VehicleSpeedCluster
            try:
                decoded_message = db.decode_message(message.arbitration_id, message.data)
                speed = decoded_message.get('VehicleSpeedCluster')
            except Exception as e:
                print(f"Error decoding message 0x280: {e}")
             
        print(f"SOH: {soh:.1f}%   ", end="")
        print(f"Gids: {gids}   ", end="")
        print(f"BattTemp: {temp}    ", end="")
        print(f"Speed: {speed:.1f} mph    ", end="\r")             
             
#        else:
#           print(f"Message ID in hex ", hex(message.arbitration_id))

def main():
    """
    Initializes the CAN bus and continuously reads and decodes messages.
    """
    try:
        # Initialize the CAN bus interface (ensure 'can0' is correct for your setup)
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
        print("Successfully connected to can0.")
        
        if file.startswith("EV"):
            evCan(bus)
        elif file.startswith("CAR"):
            carCan(bus)
        else:
            print("Unrecognized CAN bus data")             

    except can.CanError as e:
        print(f"CAN Error: {e}")
        print("Please ensure the 'can0' interface is up ('sudo ip link set can0 up type can bitrate 500000')")
    except KeyboardInterrupt:
        print("\nShutting down logger.")
    finally:
        if 'bus' in locals() and bus:
            bus.shutdown()

if __name__ == "__main__":
    main()

