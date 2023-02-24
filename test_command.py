from .i2c_transport import read_from_esp32, write_to_esp32




response_dict = {
    200: "RESPONSE_OK",
    100: "RESPONSE_FAIL",
    101: "RESPONSE_UNKNOW_CM",
    102: "RESPONSE_REQUIRED_ACK",
    103: "RESPONSE_DATA_UNCOMPLETED",
}

command_dict = {

}


if __name__ == "__main__":

    ESP_I2C_address = 0x30

    # while True:
        # request ESP32 to get data



    write_to_esp32(ESP_I2C_address, f"\x86")
    
    # wait to process the request
    time.sleep(0.1)

    write_to_esp32(ESP_I2C_address, "")
    time.sleep(0.1)
    # Get the value from the ESP32
    data = read_from_esp32(ESP_I2C_address, 100)
    # if data :
    #     command = ord(data[0])
    #     print(response_command_dict[command])
    print(str(data))
    time.sleep(2)
