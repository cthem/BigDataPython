import pandas as pd
import os
import numpy as np
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import UtilsPandas as up


def question_c(features_file, output_folder):
    feature_df = pd.read_csv(features_file)
    kf = KFold(n_splits=10)
    grid_features, targets = preprocess_data(feature_df)
    folds_idxs = list(kf.split(grid_features))
    folds_idxs = list(kf.split(grid_features))
    trips_array = np.asarray(grid_features)
    targets = np.asarray(targets)

    classifiers = ["knn", "logreg", "randfor"]
    accuracies = {}
    # classify
    for classifier in classifiers:
        print("Testing classifier [%s]" % classifier)
        # train & test each classifier
        # for each fold
        accuracies[classifier] = []
        for i, (train_idx, val_idx) in enumerate(folds_idxs):
            print("\tClassifing fold %d/%d" % (i + 1, len(folds_idxs)))
            train = (trips_array[train_idx], targets[train_idx])
            val = (trips_array[val_idx], targets[val_idx])
            if classifier == "knn":
                k = 5
                res = knn_classification(train, val, targets, k)
            elif classifier == "logreg":
                res = logreg_classification(train, val)
            elif classifier == "randfor":
                res = randfor_classification(train, val)
            accuracies[classifier].append(res)
        titlestr = "%s, overall accuracy: %2.4f" % (classifier, np.mean(accuracies[classifier]))
        up.barchart(list(range(1, 11)), accuracies[classifier], title=titlestr, ylabel="accuracy",
                       save=os.path.join(output_folder, classifier))


def preprocess_data(feature_df):
    targets = []
    data = []
    for index, row in feature_df.iterrows():
        targets.append(row["journeyId"])
        train_points = row["points"]
        train_points = eval(train_points)
        points = []
        for point in train_points:
            points.append(point[1])
        data.append(points)
    for i,d in enumerate(data):
        print(targets[i], d)
    # get maximum length of feature lists
    maxlen = len(max(data, key=lambda x: len(x)))
    data = [[int(d[1:]) for d in dlist] for dlist in data]
    # pad to the maximum length
    for i, datum in enumerate(data):
        if len(datum) < maxlen:
            data[i] = datum + [3 for _ in range(maxlen - len(datum))]

    # convert journey ids to numbers
    num_ids = {}
    targets_nums = []
    for t in targets:
        if t not in num_ids:
            num_ids[t] = len(num_ids)
        targets_nums.append(num_ids[t])
    # count occurences
    hist = []
    for jid in num_ids:
        occurences = sum([1 if t == jid else 0 for t in targets])
        hist.append((jid, occurences))

    sorted(hist, key=lambda x: x[1])
    print("Most frequent 5 jids:")
    for (jid, occ) in hist[:5]:
        print(jid, ":", occ)
    return data, targets_nums


def knn_classification(train, val, targets, k):
    # folds contains 10 tuples (training and test sets)
    knn_classifier = KNeighborsClassifier(n_neighbors=k)
    knn_classifier.fit(train[0], train[1])
    res = knn_classifier.predict(val[0])
    # TODO fix the below
    # print(classification_report(res, np.array(twenty_train.target)[test_index], target_names=twenty_train.target_names))
    return accuracy_score(res, val[1])


def logreg_classification(train, val):
    lr_classifier = LogisticRegression()
    lr_classifier.fit(train[0], train[1])
    res_prob = lr_classifier.predict_proba(val[0])
    # get probabilty argmax for the predicted class
    res = np.argmax(res_prob, axis=1)
    return accuracy_score(res, val[1])


def randfor_classification(train, val):
    rf_classifier = RandomForestClassifier()
    rf_classifier.fit(train[0], train[1])
    res = rf_classifier.predict(val[0])
    return accuracy_score(res, val[1])


def improve_classification():
    pass
