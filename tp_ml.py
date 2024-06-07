# -*- coding: utf-8 -*-
"""TP_ML

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mNYMjLh1lKK57B2IbdI18sBpMw57ZKkS
"""

from google.colab import drive

drive.mount('/content/drive')

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

df = pd.read_csv("/content/drive/MyDrive/Colab2/dataset.csv")

display(df)

"""Question 1.1 :  
Les différentes colonnes (27) sont les différentes caracréristiques physilogiques de différents individus (Genre, âge, taille, poids vue audition, analyse d'urine et sanguine, dentition, fumeur ou non).

Il y a 55702 entrées dans le jeu de donné (5 individus)



"""

df.isnull()

df.isnull().sum()

"""Question 1.1 : Il y a 12 entrée ayant des valeurs Null"""

df['smoking'].plot(kind='hist', bins=20, title='Smoke')

dff=df[df['smoking']==1]

print("La moyenne d'âge des fumeurs est de : " + str(dff['age'].mean()) +' ans')
print("La taille moyenne des fumeurs est de : " + str(dff['height(cm)'].mean()) +' cm')
print("Le poid moyen des fumeurs est de : " + str(dff['weight(kg)'].mean()) +' kg')

df.boxplot()

df_ab_age=df[df['age']>80]
display(df_ab_age)

"""Il y a 4 personne dont l'âge est abérrant :


*   180 ans
*   1200 ans
*   3000 ans
*   40 000 ans








"""

ecart_type=df['hemoglobin'].std()
print("L'écart type pour l'hémoglobine est : " + str(ecart_type))

df['smoking'].plot(kind='hist', bins=20, title='Smoking proportion')

"""Mon ordinateur n'arrive à afficher un pie chart donc voici tout de même un histogramme

Pour les hommes:
"""

df_Male_S=df[df['gender']=='M']
print(df_Male_S['smoking'].value_counts())
df_Male_S['smoking'].plot(kind='hist', bins=20, title='Smoking proportion Male')

"""Pour les femmes:


"""

df_Female_S=df[df['gender']=='F']
print(df_Male_S['smoking'].value_counts())
df_Female_S['smoking'].plot(kind='hist', bins=20, title='Smoking proportion Female')

df_Male_TrueS=df_Male_S[df_Male_S["smoking"]==1]
print("L'âge moyen des hommes fumeurs est de : " + str(df_Male_TrueS['age'].mean()) +' ans')

"""1.4 Analyse corrélation

Impossible de faire la matrice de corrélation car gender oral et tartar ne sont pas des valeurs qui peuvent être convertie en float

2.1
"""

df2=df.dropna()
display(df2)

"""J'ai supprimé les valeurs manquantes, au vue de la taille du dataset l'impact est minime

2.2 Encodage des catégories

"""

df2=pd.get_dummies(df2, prefix=['gender'], columns = ['gender'])
df2=pd.get_dummies(df2, prefix=['tartar'], columns = ['tartar'])
df2=pd.get_dummies(df2, prefix=['oral'], columns = ['oral'])

display(df2)

mat_corr=df2.corr()

plt.figure(figsize=(28,28))
sns.heatmap(mat_corr, annot=True, linewidth=0.5 ,linecolor="White")

"""On aurait pu enlever les variables avec le moins de corrélattions pour optimiser le dataset.

Suite 1.4 :

Les valeurs les plus corrélés entre elle sont :

- Taille et genrder_M
- AST et ALT
- gender_M et hemoglobin

Les variables les plus corrélés à la variables cibles fumeurs sont :
- gender_M
- hemoglobin
- height(cm)

Partie 3 : Logistic Regression
"""

X = df2.drop('smoking',axis=1)
y=df2['smoking']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

"""En utilisant la fonction train_test_split on a comme partition:

80% pour l'entrainement
20% pour le test

Il faut séparer le dataset pour que le modèle sois assez sensible sans pour autatn être trop spécifique
"""

clf = LogisticRegression(random_state=0, solver='saga', max_iter=1000).fit(X_train, y_train)

clf.score(X_test, y_test)

"""On test pour KNN:"""

neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y)

y_pred=neigh.predict(X_test)
confusion_mat_result = confusion_matrix(y_pred, y_test)
accuracy_score(y_test, y_pred)

"""On test pour un arbre de décision :"""

clf2 = DecisionTreeClassifier()
clf2.fit(X_train, y_train)
clf2.score(X_test, y_test)

"""On test pour un RandomTree :"""

clf3 = RandomForestClassifier( random_state=0)
clf3.fit(X_train, y_train)
clf3.score(X_test, y_test)

"""On test pour Gradiant Boosting Classifier:"""

clf = GradientBoostingClassifier(random_state=0).fit(X_train, y_train)
clf.score(X_test, y_test)

"""On cherche maitenant à optimiser les hyperparamètre:

Regression Logistic
"""

clf=LogisticRegression()
h_parameters_clf={
    'C': [0.01, 0.1, 1, 10, 100],
    'max_iter': [100, 200, 300, 400,500],
    'solver': ['liblinear', 'lbfgs']

}
grid_search_clf = GridSearchCV(estimator=clf, param_grid=h_parameters_clf, cv=5, scoring='accuracy')
grid_search_clf.fit(X_train, y_train)
best_model_clf = grid_search_clf.best_estimator_
pred_clf = best_model_clf.predict(X_test)
print(grid_search_clf.best_params_)
print(pred_clf)

"""KNN :"""

param_grid_neigh = {
    'n_neighbors': [3, 5, 7, 9],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan']
}

grid_search_neigh = GridSearchCV(estimator=neigh, param_grid=param_grid_neigh, cv=5, scoring='accuracy')
grid_search_neigh.fit(X_train, y_train)
print(grid_search_neigh.best_params_)
best_model_neigh = grid_search_neigh.best_estimator_
pred_neigh = best_model_neigh.predict(X_test)

"""Je ne sais pas si c'est un problème de connection (je suis de retour dans ma campagne lyonnaise) mais les code pour déterminer les hypers paramètres n'aboutissent pas. Je peut donc pas effectuer de manière efficace le parameter tuning. Avec les éléments que je possède le modèle le plus efficace est le random tree."""