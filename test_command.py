from i2c_transport import read_from_esp32, write_to_esp32

import time
import numpy as np


response_dict = {
    200: "RESPONSE_OK",
    100: "RESPONSE_FAIL",
    101: "RESPONSE_UNKNOW_CM",
    102: "RESPONSE_REQUIRED_ACK",
    103: "RESPONSE_DATA_UNCOMPLETED",
    104: "RESPONSE_BAD_REQUEST"
}

command_dict = {
    1 :   f"" ,      # exit 
    1000: f"\xC2",  # Send ACK to device

    1100: f"\x84",     # disable all pins
    1200: f"\x85",     # enable all pins
    1300: f"\x86",      # Get all pin values
    1401: f"\x83\x04",      # Get status flow 1
    1402: f"\x83\x0D",      # Get status flow 2
    1403: f"\x83\x10",      # Get status flow 3
    1404: f"\x83\x11",      # Get status flow 4
    1405: f"\x83\x12",      # Get status flow 5
    1406: f"\x83\x13",      # Get status flow 6
    1407: f"\x83\x17",      # Get status flow 7
    1408: f"\x83\x19",      # Get status flow 8
    1409: f"\x83\x1A",      # Get status flow 9
    1410: f"\x83\x1B",      # Get status flow 10
    1411: f"\x83\20",      # Get status flow 11
    1412: f"\x83\x21",      # Get status flow 12
    1413: f"\x83\x26",  # get invalid in status 

    1501: f"\x80\x04",      # Enable flow 1
    1502: f"\x80\x0D",      # Enable flow 2
    1503: f"\x80\x10",      # Enable flow 3
    1504: f"\x80\x11",      # Enable flow 4
    1505: f"\x80\x12",      # Enable flow 5
    1506: f"\x80\x13",      # Enable flow 6
    1507: f"\x80\x17",      # Enable flow 7
    1508: f"\x80\x19",      # Enable flow 8
    1509: f"\x80\x1A",      # Enable flow 9
    1510: f"\x80\x1B",      # Enable flow 10
    1511: f"\x80\20",      # Enable flow 11
    1512: f"\x80\x21",      # Enable flow 12
    1513: f"\x80\x26",  # Enable invalid flow

    1601: f"\x81\x04",      # Disable flow 1
    1602: f"\x81\x0D",      # Disable flow 2
    1603: f"\x81\x10",      # Disable flow 3
    1604: f"\x81\x11",      # Disable flow 4
    1605: f"\x81\x12",      # Disable flow 5
    1606: f"\x81\x13",      # Disable flow 6
    1607: f"\x81\x17",      # Disable flow 7
    1608: f"\x81\x19",      # Disable flow 8
    1609: f"\x81\x1A",      # Disable flow 9
    1610: f"\x81\x1B",      # Disable flow 10
    1611: f"\x81\x20",      # Disable flow 11
    1612: f"\x81\x21",      # Disable flow 12
    1613: f"\x81\x26",  # Disable invalid flow

    1701: f"\x82\x04",      # Get value flow 1
    1702: f"\x82\x0D",      # Get value flow 2
    1703: f"\x82\x10",      # Get value flow 3
    1704: f"\x82\x11",      # Get value flow 4
    1705: f"\x82\x12",      # Get value flow 5
    1706: f"\x82\x13",      # Get value flow 6
    1707: f"\x82\x17",      # Get value flow 7
    1708: f"\x82\x19",      # Get value flow 8
    1709: f"\x82\x1A",      # Get value flow 9
    1710: f"\x82\x1B",      # Get value flow 10
    1711: f"\x82\x20",      # Get value flow 11
    1712: f"\x82\x21",      # Get value flow 12
    1713: f"\x82\x26",  # Get value invalid flow


    4000: f"\xC0",  # reset device
    4100: f"\xC1",  # get device live_time
}

command_text_dict = {
    1 :   f"Exit loop" ,      # exit 

    1000: f"Send ack to device",  # Send ACK to device

    1100: f"Disable all pins",     # disable all pins
    1200: f"Enable all pins",     # enable all pins
    1300: f"Get all pin values",      # Get all pin values
    1401: f"Get status flow 1",  
    1402: f"Get status flow 2",  
    1403: f"Get status flow 3",  
    1404: f"Get status flow 4",  
    1405: f"Get status flow 5",  
    1406: f"Get status flow 6",  
    1407: f"Get status flow 7",  
    1408: f"Get status flow 8",  
    1409: f"Get status flow 9",  
    1410: f"Get status flow 10",  
    1411: f"Get status flow 11",  
    1412: f"Get status flow 12",  
    1413: f"Get invalid pin status",

    1501: f"Enable flow 1", 
    1502: f"Enable flow 2", 
    1503: f"Enable flow 3",
    1504: f"Enable flow 4",
    1505: f"Enable flow 5",
    1506: f"Enable flow 6",
    1507: f"Enable flow 7",
    1508: f"Enable flow 8",
    1509: f"Enable flow 9",
    1510: f"Enable flow 10",
    1511: f"Enable flow 11",
    1512: f"Enable flow 12",
    1513: f"Enable invalid flow", 

    1601: f"Disable flow 1", 
    1602: f"Disable flow 2", 
    1603: f"Disable flow 3",
    1604: f"Disable flow 4",
    1605: f"Disable flow 5",
    1606: f"Disable flow 6",
    1607: f"Disable flow 7",
    1608: f"Disable flow 8",
    1609: f"Disable flow 9",
    1610: f"Disable flow 10",
    1611: f"Disable flow 11",
    1612: f"Disable flow 12",
    1613: f"Disable invalid flow", 

    1701: f"Get value flow 1", 
    1702: f"Get value flow 2", 
    1703: f"Get value flow 3",
    1704: f"Get value flow 4",
    1705: f"Get value flow 5",
    1706: f"Get value flow 6",
    1707: f"Get value flow 7",
    1708: f"Get value flow 8",
    1709: f"Get value flow 9",
    1710: f"Get value flow 10",
    1711: f"Get value flow 11",
    1712: f"Get value flow 12",
    1713: f"Get value invalid flow", 


    4000: f"Reset device",
    4100: f"Get Device Alive time",

}

def print_all_flow_value(data):

    float_array = np.frombuffer(bytearray(data), np.float32)
    for index, f in enumerate(float_array):
        print(f" Flow {index + 1} =  {f}")



if __name__ == "__main__":

    ESP_I2C_address = 0x30

    while True:
        # request ESP32 to get data

        command_id = input("\nPlease enter command id: ")
        command_id = int(command_id)
        if command_id == 1:
            break;

        if command_id in command_dict:
            send_byte = command_dict[command_id]
            print (command_text_dict[command_id])

            write_to_esp32(ESP_I2C_address, send_byte)
        
            # wait to process the request
            time.sleep(0.5)

            write_to_esp32(ESP_I2C_address, "")
            time.sleep(0.1)
            # Get the value from the ESP32
            data = read_from_esp32(ESP_I2C_address, 100)
            if data:
                print(f"Response code {response_dict[data[0]]}")

                if data[0] == 200:  # get other data when response ok only
                    if (send_byte == f"\x86") :  # get all flow value
                        print_all_flow_value(data[1:])

                    if (send_byte[0] == f"\x83") : # get  flow status
                        print(f"status {data[1]}")

                    if (send_byte[0] == f"\x82") : # get  flow value
                        values = np.frombuffer(bytearray(data[1:]), np.float32)
                        print(f"value {values[0]}")
                    if send_byte[0] ==  f"\xC1":
                        print(f"data size {len(data)}")
                        values = np.frombuffer(bytearray(data[1:]), np.uint32)
                        print(f"alive time {values[0] /1000} sec")

            else:
                print("Response error")
        else:
            print("Command not found")

     
    print("Exit app")