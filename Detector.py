import joblib
import subprocess
import json
import time
import socket
import signal
import pandas as pd
import numpy as np
import tldextract
import warnings
from DataPreparation import DataPreparation
from maskgrams import maskgrams
#warnings.simplefilter(action='ignore', category=FutureWarning)

# Load machine learning models
ModelMaldom = joblib.load("./KNN-Maldom2.joblib")
ModelMG = joblib.load("./RF-MG.joblib")
print('Modelos Cargados')

Date = '2023-06-20'
Time = '17-00-01'
# Amount of queries
numqueries = 0
Count_RMA = 0
Count_Maldom = 0
Count_MG = 0

Whitelist = pd.read_excel('Whitelist.xlsx', sheet_name = 'Hoja1')

def obtener_sld(dominio):
    ext = tldextract.extract(dominio)
    return ext.domain


def interruptions(sig, frame):
    # Save results
    with open(f'/home/admin-user/bndf/DGA/Queries-{Date}.txt', 'a') as file:
        file.write(f"Consultas totales {Time}: {numqueries} \t RMA: {Count_RMA} \t Maldom: {Count_Maldom} \t MG: {Count_MG}\n")
    exit()

# DNS parameter extractor (domain and IP)
def parse_gelf_log(log):
    log_data = json.loads(log)
    domain = log_data.get("_name")
    ip_address = log_data.get("_ip")
    return domain, ip_address


# Listener
def receive_data():
    global numqueries
    global Count_RMA
    global Count_Maldom
    global Count_MG
    # Socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port 10000
    server_socket.bind(('10.0.2.96', 1235))

    # Listening
    server_socket.listen(1)

    while True:

        # Connection
        client_socket, client_address = server_socket.accept()

        # Amount of DNS queries
        numqueries = numqueries + 1

        # Receive data
        data = client_socket.recv(2048)
        #domain,ip = parse_gelf_log(data.decode('utf-8'))
        domain = data.decode('utf-8')
        SLD = obtener_sld(domain)
        print(domain)
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
                with open(f'/home/admin-user/bndf/DGA/Predictions-{Date}-{Time}.txt', 'a') as file:
                    file.write(f"{domain} \t\t {SLD} \t\t {RMA_prediction} \t\t {Maldom_prediction[0]} \t\t {MG_prediction[0]}\n")
        else:
            print('Dominio en Whitelist')
        # Close connection
        client_socket.close()

signal.signal(signal.SIGINT, interruptions)
receive_data()
