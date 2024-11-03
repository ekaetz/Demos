#Include necessary libraries
import SocketCtrl
import time

TestAppSocket = SocketCtrl.TestAppSocket()

global DebugLevel
DebugLevel = 1

#--- Connect ---
IP = "127.0.0.1"
Port = 8512                                               
Ret = TestAppSocket.App_Connect(IP,Port)
print(Ret)

if Ret[0] == 0:
#Call Function
  #TestAppSocket.Get(Timeout,FunctionName,[Arg1,Arg2, ...])
  
  Result = TestAppSocket.FunctCall(5,"FunctTestSuccess","23","56")
  #print(str(Result) + "\n")

  Result = TestAppSocket.FunctCall(5,"FunctTestError","Arg1","Arg2")
  #print(str(Result) + "\n")

  Result = TestAppSocket.FunctCall(5,"MoveStatus")
  #print(str(Result) + "\n")

  Result = TestAppSocket.FunctCall(5,"MoveStatus")
  #print(str(Result) + "\n")

  Result = TestAppSocket.FunctCall(30,"MoveAbs","92","35")
  #print(str(Result) + "\n")

  time.sleep(2) 
  Result = TestAppSocket.FunctCall(30,"MoveAbs","-45","-29")
  #print(str(Result) + "\n")
  
  #--- Disconnect ---
  Result = TestAppSocket.App_Disconnect()
  print(str(Result) + "\n")

###################################################  
