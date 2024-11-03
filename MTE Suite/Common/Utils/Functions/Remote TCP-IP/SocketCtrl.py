#Include necessary libraries
import socket 
import json

#These are functions to call Functions at the MTE App Remote Interface

class TestAppSocket:
  #Class that connects to the socket MTE app and sends and recieves Function Call and RTN messages.
  #Define Socket
  socket.setdefaulttimeout(10)
  socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #Define debug level
  DebugLevel = 1
  SequenceNumber = 0

  #--------------------------------------------------
  #     Connect to socket
  #--------------------------------------------------
  def App_Connect(self, IP,Port):
    #Connect
    print("\nConnecting to the socket App at " + IP + ", " + str(Port))
    self.SequenceNumber = 0
    try:
      self.socket_connection.connect((IP,Port)) 
    except:
      print("Could not connect to socket.  Verify:\n",\
        "    The IP and Port are correct\n",\
        "    There is network connectivity between your PC and the PC running the socket app.\n",\
        "    The socket app is runnign and is listening to the correct IP and port.\n",\
        )
      return [-1]
    else:
      #print("    Successfully Connected to socket App")
      return [0]
  #--------------------------------------------------

  #--------------------------------------------------
  #     Close socket Connection
  #--------------------------------------------------
  def App_Disconnect(self):
    self.socket_connection.close()
    return [0]
  #--------------------------------------------------

  #--------------------------------------------------
  #     FunctCall
  #--------------------------------------------------
  def FunctCall (self, *args):  
    self.SequenceNumber = self.SequenceNumber + 1
    FunctTimeout = args[0]
    FunctName = args[1]
    FunctArgs = args[2:]
    MsgBody = json.dumps({"Seq":self.SequenceNumber,"TimeOut" : FunctTimeout, "Funct":FunctName,"Args":FunctArgs})
    MsgLen = len(MsgBody)
    print ("Sending Message\n" + MsgBody + "\n")     
    MsgLenStr = '{0:03d}'.format(MsgLen)
    #Add Length Field
    Msg = MsgLenStr + MsgBody

    #Send message to socket  
    try:
      self.socket_connection.send(Msg.encode('ascii'))
    except socket.timeout:
      print("FunctCall Tx timed out!")
      return [-1, "FunctCall Tx timed out!"]
    except:
      print("Unknown exception!")
      return [-1, "Unknown exception while trying to send \"FunctCall\" message!"]
    else:
      #Receive Response
      try:
        RTN = self.socket_connection.recv(1024)
      except:
        return [-1, "Exception reading response to \"FunctCall\" message!"]
      else:
        RTN = RTN.decode('ascii')
        RTN = RTN[3:] # Remove Length

        #TODO - Decode data here.  Unpack JSON data
        print ("RTN Message\n" + RTN)
        return  [RTN]
  #--------------------------------------------------
  