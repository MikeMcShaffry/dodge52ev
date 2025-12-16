import can
import cantools
import time

# Load the DBC file
try:
    db = cantools.database.load_file('EV-can_ZE0.dbc')
except FileNotFoundError:
    print("Error: EV-can_ZE0.dbc not found. Please place it in the same directory.")
    exit()

def main():
    """
    Initializes the CAN bus and continuously reads and decodes messages.
    """
    try:
        # Initialize the CAN bus interface (ensure 'can0' is correct for your setup)
        bus = can.interface.Bus(channel='can0', bustype='socketcan')
        print("Successfully connected to can0.")
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

