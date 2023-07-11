def RandomForest(X_train, y_train, estimators, depth, typeCriterion, features, fold):
    #Definicion y ajuste del modelo ML
    from sklearn.ensemble import RandomForestClassifier
    RF = RandomForestClassifier(n_estimators = estimators,
                                    criterion = typeCriterion,
                                    max_features = features,
                                    max_depth = depth)
    
    CrossFold(RF, X_train, y_train, fold)    
    RF.fit(X_train, y_train)
    return RF

def SupportVectorialMachines(X_train, y_train, nucleo, reg, folds):
    #Definicion y ajuste del modelo ML
    from sklearn import svm
    SVM = svm.SVC(kernel = nucleo, C = reg, gamma='auto')

    CrossFold(SVM, X_train, y_train, folds)
    SVM.fit(X_train, y_train)
    return SVM    

def KNearestNeighbors(X_train, y_train, K, distanceMetric, distanceWeight, folds):
    #Definicion y ajuste del modelo ML
    from sklearn.neighbors import KNeighborsClassifier
    KNN = KNeighborsClassifier(n_neighbors = K, 
                               p = distanceMetric,
                               weights = distanceWeight,)
    
    CrossFold(KNN, X_train, y_train, folds)
    KNN.fit(X_train, y_train)
    return KNN

def MultiLayerPerceptron(X_train, y_train, act, learning, hidden, folds):
    #Definicion y ajuste del modelo ML
    from sklearn.neural_network import MLPClassifier
    MLP = MLPClassifier(activation = act,
                        max_iter = 400,
                        hidden_layer_sizes = (hidden,),   
                        learning_rate_init = learning,
                        learning_rate='invscaling',
                        solver='adam',
                        power_t=0.01
                        )
    
    CrossFold(MLP, X_train, y_train, folds)
    MLP.fit(X_train, y_train)
    return MLP

def CrossFold(Model, X_train, y_train, folds):
    from sklearn.model_selection import cross_val_score
    ModelFold = cross_val_score(Model, X_train, y_train, cv = folds)
    print("Accuracy Average - K Fold:", ModelFold.mean(),"\n")
