import time
from pyModbusTCP.client import ModbusClient

from rmf_door_msgs.msg import DoorMode

class DoorClientAPI:
    def __init__(self, node, 
                 ip_address, 
                 port):
        self.name = 'rmf_door_adapter'
        self.timeout = 5  # seconds
        self.debug = False
        self.connected = False
        self.node = node
        self.client = ModbusClient(ip_address, port=port, timeout=self.timeout, auto_open=True)
        self.client.open()

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

    def open_door(self):
        if not self.connected:
            return False
        result = self.client.write_coil(0, True)
        return not result.isError()

    def close_door(self):
        ''' Return True if the door API server is successful receive close door command'''
        if not self.connected:
            return False
        result = self.client.write_coil(0, False)
        return not result.isError()

    def get_mode(self):
        ''' Return the door status with reference rmf_door_msgs. 
            Return DoorMode.MODE_CLOSED when door status is closed.
            Return DoorMode.MODE_MOVING when door status is moving.
            Return DoorMode.MODE_OPEN when door status is open.
            Return DoorMode.MODE_OFFLINE when door status is offline.
            Return DoorMode.MODE_UNKNOWN when door status is unknown'''
        if not self.connected:
            return DoorMode.MODE_OFFLINE
        result = self.client.read_discrete_inputs(0, 1)
        if result.isError():
            return DoorMode.MODE_OFFLINE
        else:
            value = result.bits[0]
            if value:
                return DoorMode.MODE_OPEN
            else:
                return DoorMode.MODE_CLOSED
            