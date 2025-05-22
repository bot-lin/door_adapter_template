import time
from pymodbus.client.sync import ModbusTcpClient

from rmf_door_msgs.msg import DoorMode

class DoorClientAPI:
    def __init__(self, node, config):
        self.name = 'rmf_door_adapter'
        self.timeout = 5  # seconds
        self.debug = False
        self.connected = False
        self.node = node
        self.config = config  # use this config to establish connection
        self.client = ModbusTcpClient(self.config['host'], port=self.config['port'])

        count = 0
        self.connected = True
        while not self.check_connection():
            if count >= self.timeout:
                print("Unable to connect to door client API.")
                self.connected = False
                break
            else:
                print("Unable to connect to door client API. Attempting to reconnect...")
                count += 1
            time.sleep(1)

    def check_connection(self):
        ''' Return True if connection to the door API server is successful'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return self.client.connect()

    def open_door(self, door_id):
        if not self.connected:
            return False
        result = self.client.write_coil(door_id, True)
        return not result.isError()

    def close_door(self, door_id):
        ''' Return True if the door API server is successful receive close door command'''
        if not self.connected:
            return False
        result = self.client.write_coil(door_id, False)
        return not result.isError()

    def get_mode(self, door_id):
        ''' Return the door status with reference rmf_door_msgs. 
            Return DoorMode.MODE_CLOSED when door status is closed.
            Return DoorMode.MODE_MOVING when door status is moving.
            Return DoorMode.MODE_OPEN when door status is open.
            Return DoorMode.MODE_OFFLINE when door status is offline.
            Return DoorMode.MODE_UNKNOWN when door status is unknown'''
        if not self.connected:
            return DoorMode.MODE_OFFLINE
        result = self.client.read_holding_registers(door_id, 1)
        if result.isError():
            return DoorMode.MODE_UNKNOWN
        else:
            value = result.registers[0]
            if value == 0:
                return DoorMode.MODE_CLOSED
            elif value == 1:
                return DoorMode.MODE_OPEN
            elif value == 2:
                return DoorMode.MODE_MOVING
            else:
                return DoorMode.MODE_UNKNOWN
