#Machine Learning: RF, SVM, KNN y MLP
#Universidad de Cuenca
#Adrian Fernandez & Linder Quizhpe

import MethodsML
import pandas as pd
import joblib

############################### Data Read #####################################
domains = pd.read_excel("FeaturesDatabaseMaldom.xlsx") #Domain features

############################# Data Division ###################################
percentTest = 0.1                                # Testing percentage
folds = 10                                       # Cross fold

data = domains.drop(["Label"], axis = 1)         # Features by domain
labels = domains.Etiqueta                        # 0->Benign | 1->DGA

# Data Train and Data Test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
                                   data, labels, test_size = percentTest)

########################## Machine Learning Models ############################
# K-Nearest Neighbors
neighbors = 100                 # Number of neighbors
distanceMetric = 10             # Minkowski power
distanceWeight = "uniform"      # Weight function
KNN = MethodsML.KNearestNeighbors(X_train, y_train, neighbors, 
                                  distanceMetric, distanceWeight, folds)
joblib.dump(KNN, "KNN.joblib")

# Support Vectorial Machines
core = "rbf"                    # Kernel type
reg = 50                        # Regularization parameter
gam = "scale"                   # Kernel coefficient
SVM = MethodsML.SupportVectorialMachines(X_train, y_train, core, reg, folds, gam)
joblib.dump(SVM, "SVM.joblib")

# Random Forest
estimators = 1000               # Number of trees
depth = 50                      # Deep of each tree
typeCriterion = "gini"          # Split criterion
features = "sqrt"               # Maximum number of features
RF = MethodsML.RandomForest(X_train, y_train, estimators, 
                            depth, typeCriterion, features, folds)
joblib.dump(RF, "RF.joblib")

 
# Multi-Layer Perceptron
act = "relu"                    # Activation function
learning = 0.001                # Learning rate initial
learning_type = "invscaling"    # Learning rate
hidden = 128                    # Number of hidden layers
MLP = MethodsML.MultiLayerPerceptron(X_train, y_train, act, 
                                     learning, learning_type, hidden, folds)
joblib.dump(MLP, "MLP.joblib")

'''
############################ Modelos Entrenados ###############################
#RF = joblib.load(f"./RF-{sufijo}.joblib")
#SVM = joblib.load(f"./SVM-{sufijo}.joblib")
#KNN = joblib.load(f"./KNN-{sufijo}.joblib")
#MLP = joblib.load(f"./MLP-{sufijo}.joblib")

################################ Resultados ###################################
#Metricas de Evaluacion: RF, SVM, KNN, MLP
#R_RF  = Results.Metrics("Random Forest:",               RF,  y_test, RF.predict(X_test))
#R_SVM = Results.Metrics("Support Vectorial Machines:",  SVM, y_test, SVM.predict(X_test))
#R_KNN = Results.Metrics("K-Nearest Neighbors:",         KNN, y_test, KNN.predict(X_test))
R_MLP = Results.Metrics("Multi-Layer Perceptron:",      MLP, y_test, MLP.predict(X_test))

#Matriz de Confusion
#Results.Graphics("Random Forest",              RF, RF.predict(X_test) , X_train, X_test, y_train, y_test)
#Results.Graphics("Support Vectorial Machines", SVM, SVM.predict(X_test), X_train, X_test, y_train, y_test)
#Results.Graphics("K-Nearest Neighbors",        KNN, KNN.predict(X_test), X_train, X_test, y_train, y_test)
#Results.Graphics("Multi-Layer Perceptron",     MLP, MLP.predict(X_test), X_train, X_test, y_train, y_test)
'''
