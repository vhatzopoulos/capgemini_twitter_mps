import nltk
from sklearn import cross_validation
import numpy as np
import pickle
import random
import matplotlib.pyplot as plt

data = pickle.load(open('features_and_party_labels_grouped_by_mp','rb'))

#unlist as each element is a list of size one where the element
#is a tuple with features dict as zeroth element and party label as first
features_and_labels = [item for sublist in data for item in sublist]

size = len(features_and_labels)

#train-test split
train_fraction = 0.7


#do cross-validation on the training set
#cv = cross_validation.KFold(len(train_set), n_folds = 10, indices = True, shuffle = False, random_state = None)

repeats = 10
print "---------------------cv-------------------------"
classifiers = []
cv_accuracies = []

#repeat kFold cross validation repeats times
for r in range(repeats):

    #randomize
    random.shuffle(features_and_labels)

    train_set, test_set =  features_and_labels[:int(train_fraction*size)],features_and_labels[int(train_fraction*size):]

    #print len(train_set)
    #print len(test_set)
    #input()

    cv = cross_validation.KFold(len(train_set), n_folds = 10, indices = True, shuffle = False, random_state = None)
    fold = 0

    for train_cv, eval_cv in cv:

        classifier = nltk.NaiveBayesClassifier.train(train_set[train_cv[0]:train_cv[len(train_cv)-1]])
        accuracy = nltk.classify.accuracy(classifier,train_set[eval_cv[0]:eval_cv[len(eval_cv)-1]])

        print "repeat: ", r, " fold: ", fold
        print 'accuracy: ', accuracy

        classifiers.append(classifier)
        cv_accuracies.append(accuracy)

        fold += 1

#test the classifiers on the test set
test_accuracies = []
print "---------------------testing-------------------------"
for classifier in classifiers:
    #print classifier
    accuracy = nltk.classify.accuracy(classifier,test_set)
    print "accuracy: " , accuracy
    test_accuracies.append(accuracy)
    print classifier.show_most_informative_features()


print "mean accuracy", np.mean(test_accuracies)
print "std accuracy", np.std(test_accuracies)


plt.hist(test_accuracies)
plt.title("accuracies of 100 classifiers (10 repeats of cv with 10 folds) on test set of fraction " + str(len(test_set)/float(size)))
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
