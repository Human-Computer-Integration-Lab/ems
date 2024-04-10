import time

class FakeSerialPort:

    def write(self, bytes):
        print("Fake serial device is writing to console")
        print(bytes)

    def read(self, size: int):
        while 1:
            time.sleep(1)
        