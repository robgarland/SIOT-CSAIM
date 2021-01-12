import socket, csv, threading, time, serial, boto3
from datetime import datetime

PORT = 5050
SERVER = "192.168.1.172"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!"
FILENAME = "acceldata2.csv"
S3BUCKET = "siotbucket"

data = []

#setting up socket server to communicate with pc
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
#setting up serial bus to connect to arduino
ser = serial.Serial("/dev/ttyACM0",115200,timeout=1)
s3 = boto3.client("s3")
#preprocessing data to be appending to running array
def adddata(tic, toc):
    lista = []
    ser.flush()
    ser.write(b"1")
    livedata = ser.readline().decode("utf-8").rstrip()
    if livedata:
        evaldata = eval(livedata)
        lista.append(evaldata[0])
        lista.append(evaldata[1])
        lista.append(evaldata[2])
        lista.append(datetime.fromtimestamp(float(format(toc,".3f"))).strftime("%Y-%m-%d %H:%M:%S.%f"))
        data.append(lista)
        tic = toc
        return tic
    return tic

#function to handle live data - creating a 2s buffer (notification to collect takes approx .7 sec to arrive and so to caputure the data before the exevnt in question/around the event we need a buffer.
def livedata():
     #using serial baudrate of 115200 to ensure good sampling frequency can be otained - baudrate of 9600 means 0.01s travel time (not ideal if we want a period of this).
    datamaxsize = 100
    #freqarr = []
    tic = float(time.time())
    while True:
        toc = float(time.time())
        if abs(tic-toc) >= 0.0199: #creating samling rate of 80Hz
            if int(len(data)) <= datamaxsize:
                tic = adddata(tic, toc)
            else:
                data.pop(0)
                tic = adddata(tic, toc)
                
def handle_client(conn, addr):
    print("New Connection:",addr,"connected.")
    connected = True
    counter = 0
    while connected:
        msg = conn.recv(1).decode(FORMAT)
        ts = time.time()
        if msg == "1":
            for i in range(len(data)):
                listb = data.pop()
                CSVWriter.writerow(listb)
                counter +=1
        elif msg == DISCONNECT_MESSAGE:
            connected = False
            
    csv_file.close()
    conn.close()
    print("Connection:",addr,"closed. CSV file closed.",counter,"datapoints added.")
    if counter > 0:
        try:
            s3.upload_file(FILENAME,S3BUCKET,FILENAME)
        except:
            print("S3 Bucket Backup Failed")
        else:
            print("CSV Successfully Backed Up to S3 Bucket.")
    
def openCSV():
    global csv_file, CSVWriter
    try: #if file exists
        csv_file = open(FILENAME,'r',newline = "")
    except: #if file doesn't exist
        csv_file = open(FILENAME,'w',newline = "")
        CSVWriter = csv.writer(csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        CSVWriter.writerow(["X acceleration (m/s^2)", "Y acceleration (m/s^2)", "Z acceleration (m/s^2)", "Timestamp"])
    else:
        csv_file.close()
        csv_file = open(FILENAME,'a',newline = "")
        CSVWriter = csv.writer(csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)

def start():
    print("Server is starting ......")
    server.listen()
    print("Server is listening on:",SERVER)
    serialthread = threading.Thread(target=livedata)
    serialthread.start() #starting thread to process serial connection to arduino
    while True:
        conn, addr = server.accept() #blocking line..
        openCSV()
        serverthread = threading.Thread(target=handle_client, args = (conn, addr))
        serverthread.start() #starting thread to process server/client
        print("Active Connections:", (threading.activeCount() -1))
        print("Total Active Threads:", (threading.activeCount()))

if __name__ == "__main__":

    start()
