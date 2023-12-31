import pandas as pd
from maskgrams import maskgrams

# Read the domains database
filetxt = open("Database.txt")
domains = filetxt.readlines()

FullFeatures = []

# Extract the SLD of each Domain and calculate of the 44 features
for domain in domains:    
    FullFeatures.append(maskgrams(domain.split(".")[0]))

# Features
IndexF=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 
        'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 
        'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'F30', 'F31', 
        'F32', 'F33', 'F34', 'F35', 'F36', 'F37', 'F38', 'F39', 'F40', 'F41', 
        'F42', 'F43', 'F44']

# Save the vectors V of each domain
Datos = pd.DataFrame(FullFeatures, columns=IndexF)
Datos.to_excel("FeaturesDatabaseMG.xlsx", index=False)
