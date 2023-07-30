import joblib
import json
import time
import socket
import signal
import pandas as pd
import numpy as np
import warnings
import datetime
from DataPreparation import DataPreparation
from maskgrams import maskgrams

warnings.simplefilter(action='ignore', category=FutureWarning)

# Load machine learning models
ModelMaldom = joblib.load("/dga/models/KNN-Maldom.joblib")
ModelMG = joblib.load("/dga/models/RF-MG.joblib")

# Amount of queries
numqueries = 0
Count_RMA = 0
Count_Maldom = 0
Count_MG = 0

with open('/dga/others/Whitelist.txt', "r") as archivo:
        lista = archivo.read().splitlines()

Whitelist = pd.DataFrame()
Whitelist['Whitelist'] = lista

def interruptions(sig, frame):
    # Save results
    with open(f'/dga/results/Queries-{DateTime}.txt', 'a') as file:
        file.write(f"Consultas totales {DateTime}: {numqueries} \t RMA: {Count_RMA} \t Maldom: {Count_Maldom} \t MG: {Count_MG}\n")
    exit()

# Listener
def receive_data():
    global numqueries
    global Count_RMA
    global Count_Maldom
    global Count_MG
    
    # Socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port 1235
    server_socket.bind(('0.0.0.0', 9999))

    # Listening
    server_socket.listen(1)

    while True:
        Date = datetime.datetime.now()
        DateTime = Date.strftime("%d-%m-%Y-%H:%M:%S")
        Seg = Date.strftime("%S")
        
        if Seg == "00":
            Min = int(Date.strftime("%M"))
            start_time = time.time()
            timeout = 3598 - Min*60
            while time.time() - start_time < timeout:
                # Connection
                client_socket, client_address = server_socket.accept()
                
                # Amount of DNS queries
                numqueries = numqueries + 1
                
                # Receive data
                data = client_socket.recv(2048)
                msg  = data.decode('utf-8')
                    
                if len(msg.split(" ")) == 3:
                    IP   = msg.split(" ")[0]
                    SLD  = msg.split(" ")[1]
                    Rescode = msg.split(" ")[2]
                    Rescode = Rescode.replace("\n", "")
                    
                    if SLD not in Whitelist['Whitelist'].values:
                    # Feature extractor
                        featuresMaldom = DataPreparation(SLD)
                        featuresMaldomDF = pd.DataFrame(featuresMaldom)
                        featuresMG = maskgrams(SLD)
                        featuresMGDF = pd.DataFrame(featuresMG)

                    # Predictions
                        RMA_prediction = featuresMaldom[11]
                        Maldom_prediction = ModelMaldom.predict(featuresMaldomDF.T)
                        MG_prediction = ModelMG.predict(featuresMGDF.T)
                        if RMA_prediction == 1:
                            Count_RMA = Count_RMA + 1
                        if Maldom_prediction == 1:
                            Count_Maldom = Count_Maldom + 1
                        if MG_prediction == 1:
                            Count_MG = Count_MG + 1
                            
                    # DGA detection
                        if RMA_prediction == 1 or Maldom_prediction == 1 or MG_prediction == 1 :
                    # Save results
                            with open(f'/dga/results/Predictions-{DateTime}.txt', 'a') as file:
                                file.write(f"{SLD} \t{IP} \t{Rescode} \t{RMA_prediction} \t{Maldom_prediction[0]} \t{MG_prediction[0]}\n")

                    with open(f'/dga/results/Queries-{DateTime}.txt','w') as file:
                        file.write(f"Consultas totales {DateTime}: {numqueries} \t RMA: {Count_RMA} \t Maldom: {Count_Maldom} \t MG: {Count_MG}\n")

                    # Clear
                    del IP
                    del SLD
                    del Rescode

                # Close connection
                client_socket.close()

            numqueries = 0
            Count_RMA = 0
            Count_Maldom = 0
            Count_MG = 0

signal.signal(signal.SIGINT, interruptions)
receive_data()
