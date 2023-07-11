import pandas as pd
from DataPreparation import DataPreparation

# Read the domains database
filetxt = open("Database.txt")
domains = filetxt.readlines()

FullFeatures = []

# Extract the SLD of each Domain and calculate of vector V
for domain in domains:    
    FullFeatures.append(DataPreparation(domain.split(".")[0]))

# Vector V
IndexF=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F10', 'F12', 'F15', 'F16']

# Save the vectors V of each domain
Datos = pd.DataFrame(FullFeatures, columns=IndexF)
Datos.to_excel("FeaturesDatabaseMaldom.xlsx", index=False)
