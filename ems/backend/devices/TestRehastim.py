import Rehastim
import FakeSerialPort
import FrontEnd

if __name__ == "__main__":
    fsd = FakeSerialPort.FakeSerialPort()
    rr = Rehastim.Rehastim.fromPort("COM3")
    # rr.stim(5, 1, 200, 1)
    fe = FrontEnd.Device(rr)
    fe.calibrate()
