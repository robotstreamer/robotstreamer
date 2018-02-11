from socketIO_client import SocketIO, LoggingNamespace

  

chatSocket = SocketIO("robotstreamer.com", 6776, LoggingNamespace)


print chatSocket


