from collections import Counter
import numpy as np
import re

def maskgrams(domain):
    # Initial values
    vowels = 0
    consonants = 0
    totaltop = 0
    totalleast = 0
    squaresum = 0
    squaresum2 = 0
    bigrams = []
    features = np.zeros(44)

    # Dictionaries
    pattern = ['cc','cv','vc','ccc','cvc','vcc','vcv']
    gram1top = ['a', 'e', 'i', 'o', 's','r','n','t']
    gram1least = ['f', 'k', 'w', 'v', 'x','j','z','q']
    gram2top = ['in','er','an','re','es','ar','on','or','te','al','st','ne','en']
    gram3top = ['ing','ion','ine','ter','lin','ent','the','ers','and','est','tio','tra',
    'tor','art']
    
    # Domain in lowercase
    word = domain.lower()  
    
    # Number of characters
    features[0] = len(word)
    # Number of different characters
    features[1] = len(Counter(word))
    
    # Masks
    # Vowels -> v
    word = re.sub('[aeiou]', 'v', word)
    # Numbers -> n
    word = re.sub('[0123456789]', 'n', word)
    # Symbol -> s
    word = re.sub('[.-_]', 's', word)
    # Consonants -> c
    word = re.sub('[^vns\-\_]', 'c', word)
    
    # Count of vowels and consonants
    for key in word:
        if (key == 'v'):
            vowels = vowels + 1
        if (key == 'c'):
            consonants = consonants + 1   
    
    # Number of consonants
    features[2] = consonants
    # Number of vowels
    features[3] = vowels
    
    # Amount of different 1-gram
    charfreq = Counter(domain)

    if len(charfreq) > 1:
        # Calculate of 1-gram mean
        mean1gram = features[0]/len(charfreq)
        features[4] = mean1gram
        
        # Square sums for each 1-gram different
        for letter in charfreq:
            squaresum = squaresum + np.power(charfreq[letter] - mean1gram, 2) 
        
        # Calculate of 1-gram variance    
        variance1gram = squaresum/(len(charfreq) -1)
        features[5] = variance1gram
        
        # Calculate of 1-gram standard deviation
        devstd1gram = np.sqrt(variance1gram)
        features[6] = devstd1gram
    
    else:
        features[4] = len(domain)
        features[5] = 0
        features[6] = 0
    
    # Calculate of all 2-grams
    for i in range(len(domain)-1):
        bigram = domain[i:i+2]
        bigrams.append(bigram)
        
    # Amount of different 2-grams
    bigramfreq = Counter(bigrams)
        
    if  len(bigramfreq) > 1:
        # Calculate of 2-grams mean
        mean2gram = len(bigrams)/len(bigramfreq)
        
        # Square sums for each 2-grams different
        for twoletters in bigramfreq:
            squaresum2 = squaresum2 + np.power(bigramfreq[twoletters] - mean2gram, 2) 
        
        # Calculate of 2-gram variance    
        variance2gram = squaresum2/(len(bigramfreq) -1)
        
        # Calculate of 2-gram standard deviation
        devstd2gram = np.sqrt(variance2gram)
        features[7] = devstd2gram
    else:
        features[7] = 0
        
    # Find especific patterns sequency
    for i in range(8,14):
        features[i] = len(list(re.finditer(fr"(?={pattern[i-8]})", word)))
    
    # The most and the least 1-gram used
    for letter in domain:
        if letter in gram1top:
            totaltop += 1
        if letter in gram1least:
            totalleast += 1
    features[15] = totaltop/features[0]
    features[16] = totalleast/features[0]
    
    # The most 2-grams used 
    for i in range(17,29):
        features[i] = len(list(re.finditer(fr"(?={gram2top[i-17]})", domain)))
    
    # The most 3-grams used
    for i in range(30,43):
        features[i] = len(list(re.finditer(fr"(?={gram3top[i-30]})", domain)))
        
    return features
