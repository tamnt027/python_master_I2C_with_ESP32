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

    4000: f"Reset device",
    4001: f"Get Device Alive time",

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

                    if (send_byte[0] == f"\x83") : # get all flow status
                        print(f"status {data[1]}")

            else:
                print("Response error")


     
    print("Exit app")