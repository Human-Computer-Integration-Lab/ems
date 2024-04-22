import threading


class SerialListener(threading.Thread):
    def __init__(self, serial_device, decoder):
        threading.Thread.__init__(self)
        self.ser = serial_device
        self.decoder = decoder

    def run(self):
        print("Started a listening SerialThread on " + str(self.ser))
        while 1:
            v = self.ser.read(size=1)
            # print(len(v))
            if len(v) > 0:
                # v = v.decode("utf-8").rstrip('\r\n') #not sure if needed for EMS SERIAL RESPONSE
                if SERIAL_THREAD_DEBUG:
                    print("SERIAL_THREAD_RESPONSE:" + str(v))
                if SERIAL_THREAD_DEBUG:
                    print(v.encode("hex"))
