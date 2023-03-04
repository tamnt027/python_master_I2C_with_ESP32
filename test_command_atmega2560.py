import enum
from i2c_transport_native import read_from_arduino, write_to_arduino
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

    2000: f"\x90", # set pwm set pin value,
    2001: f"\x91", # get pwm pin value,
    2002: f"\x92\x10\x20\x30\x40\x50\x60\x70\x80\x90", # set all pin pwm value
    2003: f"\x93", # get all pin pwm value

    2100: f"\xA0", # get analog input value
    2101: f"\xA1", # get all ananlog input values

    2200: f"\xB0", # digital set pin mode
    2201: f"\xB1",  # digital get pin mode
    2202: f"\xB2", # digital get value 
    2203: f"\xB3", # digital set value

    4000: f"\xC0",  # reset device
    4100: f"\xC1",  # get device live_time
}

command_text_dict = {
    1 :   f"Exit loop" ,      # exit 

    1000: f"Send ack to device",  # Send ACK to device

    2000: f"set pwm set pin value", # set pwm set pin value,
    2001: f"get pwm pin value", # get pwm pin value,
    2002: f"set all pin pwm values", # set all pin pwm value
    2003: f"get all pin pwm values", # get all pin pwm value

    2100: f"get analog input value", # get analog input value
    2101: f"get all ananlog input values", # get all ananlog input values

    2200: f"digital set pin mode", # digital set pin mode
    2201: f"digital get pin mode",  # digital get pin mode
    2202: f"digital get value ", # digital get value 
    2203: f"digital set value", # digital set value


    4000: f"Reset device",
    4100: f"Get Device Alive time",

}

def get_pwm_pin_from_user():
    pwm_pin_list = [4, 5, 6, 7, 8, 9, 10, 11, 12]
    for i, pin in enumerate(pwm_pin_list,start=1):
        print(f"Pwm {i} pin {pin}") 
    pin_num = input("\nPlease enter pin number ")
    if int(pin_num) not in pwm_pin_list:
        print("Input wrong pin number")
        return None
    else:
        return int(pin_num) 

def get_analog_pin_from_user():
    analog_pin_list = [54, 55, 56, 57, 58, 59, 60, 61, 62]
    for i, pin in enumerate(analog_pin_list,start=1):
        print(f"Analog input {i} pin {pin}") 
    pin_num = input("\nPlease enter pin number ")
    if int(pin_num) not in analog_pin_list:
        print("Input wrong pin number")
        return None
    else:
        return int(pin_num) 


def get_analog_pin_from_user():
    analog_pin_list = [54, 55, 56, 57, 58, 59, 60, 61, 62]
    for i, pin in enumerate(analog_pin_list,start=1):
        print(f"Analog input {i} pin {pin}") 
    pin_num = input("\nPlease enter pin number ")
    if int(pin_num) not in analog_pin_list:
        print("Input wrong pin number")
        return None
    else:
        return int(pin_num) 

def get_digital_pin_from_user():
    digital_pin_list = [22, 23, 24, 25, 26, 27, 28, 29, 39, 34, 35, 36, 37, 40, 41, 39, 42, 43, 44, 45, 46, 47, 48, 49, 3]
    for i, pin in enumerate(digital_pin_list,start=1):
        print(f"Digital io {i} pin {pin}") 
    pin_num = input("\nPlease enter pin number ")
    if int(pin_num) not in digital_pin_list:
        print("Input wrong pin number")
        return None
    else:
        return int(pin_num)

def get_pwm_value_from_user(pwm_pin):
    pwm_value = input(f"\n Please input value for pin {pwm_pin}  [0, 511]")
    if int(pwm_value) not in range(0, 512):
        print("Wrong pwm value")
        return None
    else:
        return int(pwm_value)


def get_pin_mode_from_user():
    pin_mode = input(f"\n Please input pin mode, 0-output, 1-input ")
    if int(pin_mode) not in range(0, 2):
        print("Wrong pinmode  value")
        return None
    else:
        return int(pin_mode)

def get_pin_value_from_user():
    pin_value = input(f"\n Please input pin value, 0-low,  1-high")
    if int(pin_value) not in range(0, 2):
        print("Wrong pin value  value")
        return None
    else:
        return int(pin_value)

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
            break

        if command_id in command_dict:
            send_byte = command_dict[command_id]
            print (command_text_dict[command_id])

            if send_byte == f"\x90":  #set pwm set pin value
                pin_num = get_pwm_pin_from_user()
                if pin_num is None:
                    continue       

                pin_value = get_pwm_value_from_user(pin_num)
                if pin_value is None:
                    continue

                send_byte += chr(pin_num) + chr(pin_value)
            
            if send_byte == f"\x91": # get pwm pin value 
                pin_num = get_pwm_pin_from_user()
                if pin_num is None:
                    continue  
                send_byte += chr(pin_num)  

            if send_byte == f"\xA0": # get analog input value
                pin_num = get_analog_pin_from_user()
                if pin_num is None:
                    continue
                send_byte += chr(pin_num) 

            if send_byte == f"\xB0":  # digital set pin mode
                pin_num = get_digital_pin_from_user()
                if pin_num is None:
                    continue
                pin_mode = get_pin_mode_from_user()
                if pin_mode is None:
                    continue

                send_byte += chr(pin_num) + chr(pin_mode)

            if send_byte == f"\xB1":  # digital set pin mode
                pin_num = get_digital_pin_from_user()
                if pin_num is None:
                    continue
                send_byte += chr(pin_num)

            if send_byte == f"\xB2":  # digital get pin mode
                pin_num = get_digital_pin_from_user()
                if pin_num is None:
                    continue
                send_byte += chr(pin_num)

            if send_byte == f"\xB3":  # digital set pin mode
                pin_num = get_digital_pin_from_user()
                if pin_num is None:
                    continue

                pin_value = get_pin_value_from_user()
                if pin_value is None:
                    continue

                send_byte += chr(pin_num) + chr(pin_value)

            write_to_arduino(ESP_I2C_address, send_byte)
        
            # wait to process the request
            time.sleep(0.5)

            # Get the value from the ESP32
            data = read_from_arduino(ESP_I2C_address, 100)
            if data:
                print(f"Response code {response_dict[data[0]]}")

                if data[0] == 200:  # get other data when response ok only
                    if send_byte == f"\x91": # get pwm pin value 
                        print(f"Pwm has value {data[1]}")
                    if send_byte == f"\x93": # get all pwm pin value
                        for i in range(1, 10):
                            print(f"Pwm {i} = {data[i]}") 

                    if send_byte == f"\xA0": # get analog input value
                        values = np.frombuffer(bytearray(data[1:]), np.ushort)
                        print(f"Analog pin value {values[0]} ")

                    if send_byte == f"\xA1": # get all analog input value
                        values = np.frombuffer(bytearray(data[1:]), np.ushort)
                        for index, value in enumerate(values, start=1) :
                            print(f"Analog pin {index} value {value} ")

                    if send_byte == f"\xB1":  # digital set pin mode
                        if data[1] == 1 :
                            print("Pin mode is input")
                        elif data[1] == 0:
                            print("Pin mode is output")
                        else:
                            print("Undefine pin mode")

                    if send_byte == f"\xB2":  # digital get pin value
                        if data[1] == 1 :
                            print("Pin value is high")
                        elif data[1] == 0:
                            print("Pin value is low")
                        else:
                            print("Undefine pin value")


            else:
                print("Response error")
        else:
            print("Command not found")

     
    print("Exit app")