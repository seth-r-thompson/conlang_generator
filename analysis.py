import nltk
import sklearn
import matplotlib.pyplot as plt

path = "" # commented out

dataset = sklearn.datasets.load_files(path)
corpus, classes = dataset.data, dataset.target

corpus_train, corpus_test, class_train, class_test = sklearn.model_selection.train_test_split(corpus, classes, test_size = 0.2)

vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=nltk.word_tokenize, encoding="UTF-16-LE")
train = vectorizer.fit_transform(corpus_train)
test = vectorizer.transform(corpus_test)

classifier = sklearn.svm.SVC(kernel="linear").fit(train, class_train)
accuracy = sklearn.metrics.accuracy_score(class_test, classifier.predict(test))

print(accuracy)

sklearn.metrics.plot_confusion_matrix(classifier, test, class_test)
plt.show()