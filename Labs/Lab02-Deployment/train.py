import pickle
from sklearn import datasets
from sklearn import linear_model

# Train the model
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf = linear_model.LogisticRegression()
clf.fit(X, y)  

# Save the trained model
filename = "iris.sav"
pickle.dump(clf, open(filename, 'wb'))




