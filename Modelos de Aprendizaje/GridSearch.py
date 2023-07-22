import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

############################### Data Read #####################################
domains = pd.read_excel("FeaturesDatabaseMaldom.xlsx") #Domain features
#domains = pd.read_excel("FeaturesDatabaseMG.xlsx") #Domain features

############################# Data Division ###################################
percentTest = 0.1                                # Testing percentage
data = domains.drop(["Etiqueta"], axis = 1)      # Features by domain
labels = domains.Etiqueta                        # 0->Benign | 1->DGA

# Data Train and Data Test
X_train, X_test, y_train, y_test = train_test_split(
                                   data, labels, test_size = percentTest, random_state = 42)
print('Datos Spliteados')

'''
################################# KNN #########################################
KNN = KNeighborsClassifier()
knnGrid = {
    'n_neighbors': [25, 100, 150],          # Amount of neighbors
    'p'          : [1, 2, 10],              # Power parameter for the Minkowski metric
    'weights'    : ['uniform', 'distance']  # Weight function used in prediction
}

knnGridSearch = GridSearchCV(KNN, knnGrid, cv=10) # GridSearch
knnGridSearch.fit(X_train, y_train)               # Training
knnBest = knnGridSearch.best_estimator_  # Best KNN
knnPred = knnBest.predict(X_test)         # Prediction

# Calcular las métricas de evaluación
knnAccuracy  = accuracy_score(y_test, knnPred)
knnPrecision = precision_score(y_test, knnPred, average='macro')
knnRecall    = recall_score(y_test, knnPred, average='macro')
knnF1        = f1_score(y_test, knnPred, average='macro')

print("KNN Accuracy:",  knnAccuracy)
print("KNN Precision:", knnPrecision)
print("KNN Recall:",    knnRecall)
print("KNN F1-score:",  knnF1)
print("KNN Best Parameters:", knnGridSearch.best_params_)
#100; 10; Uniform
#150; 1; Uniform
'''

'''
################################# SVM #########################################
SVM = SVC()                         # Model
svmGrid = {                         # Grid
    'kernel': ['linear', 'rbf'],    # Kernel type
    'C'     : [50, 100, 300],       # Regulator parameter
    'gamma' : ['scale', 'auto']     # Kernel coefficient
}

svmGridSearch = GridSearchCV(SVM, svmGrid, cv=3)  # GridSearch
svmGridSearch.fit(X_train, y_train)                # Training
svmBest = svmGridSearch.best_estimator_            # Best SVM
svmPred = svmBest.predict(X_test)                  # Predictions

# SVM Results
svmAccuracy   = accuracy_score(y_test, svmPred)                    # Accuracy
svmPrecision  = precision_score(y_test, svmPred, average='macro')  # Precision
svmRecall     = recall_score(y_test, svmPred, average='macro')     # Recall
svmF1         = f1_score(y_test, svmPred, average='macro')         # F1-Score
print("SVM Accuracy:",  svmAccuracy)
print("SVM Precision:", svmPrecision)
print("SVM Recall:",    svmRecall)
print("SVM F1-score:",  svmF1)
print("SVM Best Parameters:", svmGridSearch.best_params_)
#LINEAR; 300; Scale
'''

'''
################################# MLP #########################################
MLP = MLPClassifier()               # Model
mlpGrid = {                         # Grid
    'hidden_layer_sizes': [(64,), (128,)],          # Amount of hidden layers
    'activation'        : ['logistic', 'relu', 'identity'], # Activation Funtion
    'solver'            : ['adam', 'sgd'],
    'max_iter'          : [400]
}

mlpGridSearch = GridSearchCV(MLP, mlpGrid, cv=10)   # GridSearch
mlpGridSearch.fit(X_train, y_train)                 # Training
mlpBest = mlpGridSearch.best_estimator_             # Best MLP
mlpPred = mlpBest.predict(X_test)                   # Predictions

# MLP Results
mlpAccuracy   = accuracy_score(y_test, mlpPred)                   # Accuracy
mlpPrecision  = precision_score(y_test, mlpPred, average='macro') # Presicion
mlpRecall     = recall_score(y_test, mlpPred, average='macro')    # Recall
mlpF1         = f1_score(y_test, mlpPred, average='macro')        # F1-Score

print("MLP Accuracy:",  mlpAccuracy)
print("MLP Precision:", mlpPrecision)
print("MLP Recall:",    mlpRecall)
print("MLP F1-score:",  mlpF1)
print("MLP Best Parameters:", mlpGridSearch.best_params_)
#RELU; 128; ADAM; INVSCALING
#RELU; 128; ADAM; INVSCALING
'''

'''
############################ Random Forest ####################################
RF = RandomForestClassifier()       # Model
rfGrid = {                          # Grid
    'n_estimators': [100, 1000, 1500],          # Amount of trees
    'max_depth'   : [ 50, 100],                 # Max depth in each tree
    'criterion'   : ['gini', 'entropy'],        # Function to measure the quality of a partition
    'max_features': ['sqrt', 'log2']            # Amount of features in each partition
}

rfGridSearch = GridSearchCV(RF, rfGrid, cv=10)      # GridSearch
rfGridSearch.fit(X_train, y_train)                  # Training
rfBest = rfGridSearch.best_estimator_               # Best Random Forests
rfPred = rfBest.predict(X_test)                     # Predictions

# Random Forests Results
rfAccuracy  = accuracy_score(y_test, rfPred)                      # Accuracy
rfPrecision = precision_score(y_test, rfPred, average='macro')    # Precision
rfRecall    = recall_score(y_test, rfPred, average='macro')       # Recall
rfF1        = f1_score(y_test, rfPred, average='macro')           # F1

print("Random Forests Accuracy:",   rfAccuracy)
print("Random Forests Precision:",  rfPrecision)
print("Random Forests Recall:",     rfRecall)
print("Random Forests F1-score:",   rfF1)
print("Random Forests Best Parameters:", rfGridSearch.best_params_)
#1000; 50; gini; sqrt
'''
