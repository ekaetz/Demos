import pywinusb.hid as hid
import time


k_MessageNull = 0x0
k_MessageReboot = 0x1
k_MessageIsp = 0x2
k_MessageOnline = 0x3
k_MessageSetOutput = 0x4
k_MessageGetOutput = 0x5
k_MessageGetInput = 0x6

k_CycleTestRun = 0x0
k_CycleTestReady = 0x1
k_RemoteCycleStart = 0x2

g_SignalInfo = [
    ( 0, 0 ),
    ( 1, 0 ),
    ( 0, 1 )
]


class CDeathstarControl:

    def __init__( self ):
        self.vid  = 0x28DE
        self.pid = 0x9000
        self.name = "Deathstar USB Control"
        self.timeout = 0.1 # seconds

    def RawHandler(self, data):
        rawData = "".join( [ chr(x) for x in data if x != 0 ] )
        self.receiveQueue.append( rawData )

    def OpenHID( self ):
        hids = hid.find_all_hid_devices()
        for device in hids:
            if device.vendor_id == self.vid and device.product_id == self.pid:
                self.gpioDevice = device
                self.gpioDevice.open()
                self.receiveQueue = []
                self.gpioDevice.set_raw_data_handler( self.RawHandler )
                self.outReports = self.gpioDevice.find_output_reports()
                self.hid_open_flag = True
                return True
        self.hid_open_flag = False
        return False

    def Init( self ):
        bSuccess = self.OpenHID()
        if not bSuccess:
            return False
        self.SetSignalState( k_RemoteCycleStart, 0 )
        return True

    def SetStartRelayON(self):
        self.SetSignalState( k_RemoteCycleStart, 1 )
        return True     

    def SetStartRelayOFF(self):
        self.SetSignalState( k_RemoteCycleStart, 0 )
        return True     

    def ReadRunningState(self):
        ioState = self.GetSignalState( k_CycleTestReady )
        return ioState     

    def SendSimpleMessage( self, msgType, ioAddr, ioState ):
        if self.hid_open_flag == True:
            self.buf = [ 0 ] * 65
            self.buf[ 0 ] = 0
            self.buf[ 1 ] = msgType
            self.buf[ 2 ] = ioAddr
            self.buf[ 3 ] = ioState
            self.outReports[ 0 ].set_raw_data( self.buf )
            self.outReports[ 0 ].send()
            return True
        else:
            print "ERROR:  HID connection not open in SendSimpleMessage()."
            return False;

    def ReceiveSimpleMessage( self, signal ):
        message = None
        startTime = time.time()
        while time.time() - startTime < self.timeout:
            if len( self.receiveQueue ) > 0:
                message = self.receiveQueue[ 0 ]
                self.receiveQueue = self.receiveQueue[ 1 : ]
        ( inOut, inAddr, ioStateText ) = message.split()
        inAddr = int( inAddr )
        ioState = None
        if ioStateText == "true":
            ioState = 1
        elif ioStateText == "false":
            ioState = 0
        return ( inOut, inAddr, ioState )

    def GetSignalState( self, signal ):
        ( ioAddr, isOutput ) = g_SignalInfo[ signal ]
        msgType = [ k_MessageGetInput, k_MessageGetOutput ][ isOutput ]
        bSuccess = self.SendSimpleMessage( msgType, ioAddr, 0 )
        if not bSuccess:
            return None
        ( inOut, inAddr, ioState ) = self.ReceiveSimpleMessage( signal )
        if inAddr != ioAddr or inOut != "input":
            return None
        return ioState

    def SetSignalState( self, signal, ioState ):
        ( ioAddr, isOutput ) = g_SignalInfo[ signal ]
        bSuccess = self.SendSimpleMessage( k_MessageSetOutput, ioAddr, ioState )
        if not bSuccess:
            return False
        ( inOut, inAddr, ioState ) = self.ReceiveSimpleMessage( signal )
        if inAddr != ioAddr or inOut != "ouput":
            return None
        return ioState

    def WaitUntilSignalState( self, signal, targetIoState, maxWaitSeconds ):
        startTime = time.time()
        while time.time() - startTime < maxWaitSeconds:
            ioState = self.GetSignalState( signal )
            if ioState == None:
                return False
            if ioState == targetIoState:
                return True
        print "ERROR:  Timed out in WaitUntilSignalState()."
        return False

    def StartCycle( self ):
        bSuccess = self.SetSignalState( k_RemoteCycleStart, 0 )
        if bSuccess == None:
            print "ERROR:  Deathstar communication failure."
            return False
        bSuccess = self.WaitUntilSignalState( k_CycleTestReady, 1, 5.0 )
        print bSuccess
        if not bSuccess:
            print "ERROR:  Deathstar timeout."
            return False;
        bSuccess = self.SetSignalState( k_RemoteCycleStart, 1 );
        if bSuccess == None:
            print "ERROR:  Deathstar communication failure."
            return False;
        bSuccess = self.WaitUntilSignalState( k_CycleTestRun, 1, 1.0 )
        if not bSuccess:
            print "ERROR:  Deathstar timeout."
            return False
        return True

    def TestCycleDone( self ):
        return ( self.GetSignalState( k_CycleTestRun ) != 1 )


def main():
    dcon = CDeathstarControl()
    dcon.Init()
    dcon.StartCycle()
    while True:
        bDone = dcon.TestCycleDone()
        print bDone
        if bDone:
            break
    print "done!"
    return dcon


if __name__ == "__main__":
    main()
