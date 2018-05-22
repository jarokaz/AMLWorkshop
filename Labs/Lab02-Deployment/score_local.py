import pickle
from sklearn import datasets
from sklearn import linear_model

iris = datasets.load_iris()
X, y = iris.data, iris.target

# Load the pretrained model
filename = 'iris.sav'
clf = pickle.load(open(filename, 'rb'))
result = clf.score(X, y)
print(result)





