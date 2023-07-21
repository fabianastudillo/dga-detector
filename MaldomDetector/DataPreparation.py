import math
import re
from itertools import groupby

def DataPreparation(domain):
    # Max number of sequential vowels
    max_vow = 0
    # Max number of sequential consonants
    max_cons = 0
    # Number of vowels
    vowels = 0
    # Number of consonants
    consonants = 0
    
    # Domain in lowercase
    word = domain.lower()
    # Vowels -> a
    word = re.sub('[eiouy]', 'a', word)
    # Consonants -> c
    word = re.sub('[^aeiouy\-\_]', 'c', word)
    
    # Count of vowels, consonants, max sequential vowels and max sequential consonants
    result = [(label, sum(1 for _ in group)) for label, group in groupby(word)]
    for key, count in result:
        if (key == 'a'):
            vowels = vowels + 1
        if (key == 'c'):
            consonants = consonants + 1
        if (key == 'a' and count > max_vow):
            max_vow = count
        elif (key == 'c' and count > max_cons):
            max_cons = count
    
    # Number of characters
    num_elem = len(domain)
    # Probability per character
    prob_elem = 1/num_elem
    # Joint of characters used in domain
    elem_set = set(domain)
    # Counter of each character
    c_pro_elem = []
    for element in elem_set:
        if (not element in '-_'):
            c_pro_elem.append(domain.count(element))
            
    # Probability of each character        
    f_pro=[i*prob_elem for i in c_pro_elem]
    
    # Domain entropy calculation
    entropy = 0
    for prob in f_pro:
        entropy = entropy+(prob*math.log(prob,2))
    entropy = round(entropy*(-1),2)
        
    # Randomness Measuring Algorithm
    if (entropy <= 2) and (num_elem < 5):
        category = 0 #"clean"
    elif (entropy > 3.24):
        category = 1 #"bot"
    elif (max_cons >= 4) or (max_vow >= 4):
        category = 1 #"bot"
    else:
        category = 0 #"clean"
    
    # Special Cases
    if (vowels == 0):
        vowels = 0.1
    if (max_vow == 0):
        max_vow = 0.1
    if (consonants == 0):
        consonants = 0.1
    if (max_cons == 0):
        max_cons = 0.1

    # Features selected by PCA
    F1 = entropy            # Domain Entropy
    F2 = max_cons           # Maximum number of sequential consonants
    F3 = max_vow            # Maximum number of sequential vowels
    F4 = num_elem           # Number of characters
    F5 = consonants         # Number od consonants
    F6 = vowels             # Number of vowels
    F7 = F1/F4              # Ratio entropy to length domain
    F8 = F5/F6              # Ratio consonants to vowels
    #F9 is not used         # Determined by PCA
    F10 = F6/F4             # Ratio vowels to length domain
    #F11 is not used        # Determined by PCA
    F12 = F3/F4             # Ratio max sequential vowels to length domain
    #F13 is not used        # Determined by PCA
    #F14 is not used        # Determined by PCA
    F15 = F2/F3             # Ratio max sequential consonants to max sequential vowels
    F16 = category          # Randomness (Output of RMA)
    Features = [F1,F2,F3,F4,F5,F6,F7,F8,F10,F12,F15,F16]

    return Features
