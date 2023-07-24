import sys
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def GridSearch(model, modelGrid):
    ############################### Data Read #####################################
    archivo = input("1: MaldomDetector\n2: N-grams Masked\n-> ")

    # Test database (50k domains)
    if archivo == "1":
        domains = pd.read_excel("FeaturesDatabaseMaldom.xlsx") #Domain features
    elif archivo == "2":
        domains = pd.read_excel("FeaturesDatabaseMG.xlsx")     #Domain features
    else:
        print("Error")
        sys.exit(0)
    
    print("Finding optimal hyperparameters...")
    
    ############################# Data Division ###################################
    percentTest = 0.1                                # Testing percentage
    data = domains.drop(["Etiqueta"], axis = 1)      # Features by domain
    labels = domains.Etiqueta                        # 0->Benign | 1->DGA
    
    # Data Train and Data Test
    X_train, X_test, y_train, y_test = train_test_split(
                                   data, labels, test_size = percentTest, random_state = 42)

    modelGridSearch = GridSearchCV(model, modelGrid, cv=10)   # GridSearch
    modelGridSearch.fit(X_train, y_train)                     # Training
    modelBest = modelGridSearch.best_estimator_               # Best Random Forests
    modelPred = modelBest.predict(X_test)                     # Predictions
    
    # Random Forests Results
    Accuracy  = accuracy_score (y_test, modelPred)                     # Accuracy
    Precision = precision_score(y_test, modelPred, average='macro')    # Precision
    Recall    = recall_score   (y_test, modelPred, average='macro')    # Recall
    F1        = f1_score       (y_test, modelPred, average='macro')    # F1
    
    print("Accuracy:",   Accuracy)
    print("Precision:",  Precision)
    print("Recall:",     Recall)
    print("F1-score:",   F1)
    print("Best Parameters:", modelGridSearch.best_params_)
    
def knn_function():
    from sklearn.neighbors import KNeighborsClassifier
    KNN = KNeighborsClassifier()                # Model
    knnGrid = {                                 # Grid
        'n_neighbors': [25, 100, 150],          # Amount of neighbors
        'p'          : [1, 2, 10],              # Power parameter for the Minkowski metric
        'weights'    : ['uniform', 'distance']  # Weight function used in prediction
    }
    GridSearch(KNN, knnGrid)

def svm_function():
    from sklearn.svm import SVC
    SVM = SVC()                                 # Model
    svmGrid = {                                 # Grid
        'kernel': ['linear'],                   # Kernel type
        'C'     : [50, 100, 300],               # Regulator parameter
        'gamma' : ['scale', 'auto']             # Kernel coefficient
    }
    GridSearch(SVM, svmGrid)
        
def random_forest_function():
    from sklearn.ensemble import RandomForestClassifier
    RF = RandomForestClassifier()               # Model
    rfGrid = {                                  # Grid
        'n_estimators': [25, 50, 100],          # Amount of trees
        'max_depth'   : [50, 100],              # Max depth in each tree
        'max_features': ['sqrt', 'log2']        # Amount of features in each partition
    }
    GridSearch(RF, rfGrid)
    
def mlp_function():
    from sklearn.neural_network import MLPClassifier
    MLP = MLPClassifier()                       # Model
    mlpGrid = {                                 # Grid
        'hidden_layer_sizes': [(64,), (128,)],                  # Amount of hidden layers
        'activation'        : ['logistic', 'relu', 'identity'], # Activation Funtion
        'solver'            : ['adam', 'sgd'],
        'max_iter'          : [400]
    }
    GridSearch(MLP, mlpGrid)    
    
# Switch case
option = input("1: KNN\n2: SVM\n3: Random Forest\n4: MLP\n-> ")

switch_case = {
    '1': knn_function,
    '2': svm_function,
    '3': random_forest_function,
    '4': mlp_function
}

# Execute
func = switch_case.get(option)
if func:
    func()
else:
    print("Error")
