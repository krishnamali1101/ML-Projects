import pydotplus
from sklearn.datasets import load_iris
from sklearn import tree
from IPython.display import Image, display

def load_data_set():
	"""
	Loads the iris data set

	:return:        data set instance
	"""
	iris = load_iris()
	return iris

def train_model(iris):
	"""
	Train decision tree classifier

	:param iris:    iris data set instance
	:return:        classifier instance
	"""
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(iris.data, iris.target)
	return clf

def display_image(clf, iris):
	"""
	Displays the decision tree image

	:param clf:     classifier instance
	:param iris:    iris data set instance
	"""
	dot_data = tree.export_graphviz(clf, out_file=None,
									feature_names=iris.feature_names,
									class_names=iris.target_names,
									filled=True, rounded=True)

	graph = pydotplus.graph_from_dot_data(dot_data)
	display(Image(data=graph.create_png()))

if __name__ == '__main__':
	iris_data = load_iris()
	decision_tree_classifier = train_model(iris_data)
	display_image(clf=decision_tree_classifier, iris=iris_data)