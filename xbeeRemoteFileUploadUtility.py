from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from datetime import datetime


#todo: change port
port = "COM6"
baud_rate = 9600
local_xbee = XBeeDevice(port, baud_rate)

ota_filesystem_image = ".\OTA_FW_Update_Files\<insert-OTA-file-image-here>image.fs.ota"
ota_filesystem_version = 0.23


def get_xbee_name_from_user():
    address = input("Enter the XBee 64-bit address: ")  # 0013A20041C86564

    try:
        remote_xbee = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string(address))
        print("Created remote_xbee", type(remote_xbee), remote_xbee)  # debug
        return remote_xbee
    except Exception as e:
        print(e)
        exit(-1)


def update_remote_filesystem(remote_xbee):
    print("updating remote device filesystem")
    remote_xbee.update_filesystem_image(ota_filesystem_image, progress_callback=progress_callback)

    print("Filesystem updated successfully!")

    print("Resetting remote_xbee")
    remote_xbee.reset()


def progress_callback(task, percent):
    print("%s: %d%%" % (task, percent))


def handle_rx_packet(xbee_message):
    print("----------------------------------")
    print("RECEIVED from %s>> %s >> %s" % (
        xbee_message.remote_device.get_64bit_addr(),
        str(datetime.fromtimestamp(xbee_message.timestamp)),
        xbee_message.data.decode()))


def main():

    try:
        print("opening local_xbee")
        local_xbee.open()
    except Exception as e:
        print("Can't open local_xbee")
        print(e)
        exit(1)
    local_xbee.add_data_received_callback(handle_rx_packet)
    print("waiting for data")

    remote_xbee = get_xbee_name_from_user()

    local_xbee.add_data_received_callback(handle_rx_packet)
    print("waiting for data")

    while True:
        pass


main()
