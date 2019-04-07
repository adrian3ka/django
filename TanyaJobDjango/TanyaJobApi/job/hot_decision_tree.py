from __future__ import unicode_literals
from .models import Job
import numpy as np
import pydotplus
import sklearn.datasets
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from IPython.display import Image, display
import MySQLdb

CATEGORICAL_VALUE = ["major", "degree", "industry", "field", "location", "job_level"]
CONTINUOUS_VALUE = ["max_age", "min_age", "max_salary", "work_exp", "min_salary"]

class JobData:
    title = ''
    degree = ''
    major = ''
    industry = ''
    min_age = 0
    max_age = 0
    field = ''
    location = ''
    job_level = ''
    work_exp = 0.0
    min_salary = 0
    max_salary = 0


class HotJobRecommendationDecisionTree:
    decision_tree_classifier = None
    collection = sklearn.datasets.base.Bunch()
    clf = tree.DecisionTreeClassifier()

    jobDatas = []  # other from title
    targetDatas = []  # title
    # Label Encoder
    labelDegrees = sklearn.preprocessing.LabelEncoder()
    labelMajors = sklearn.preprocessing.LabelEncoder()
    labelIndustries = sklearn.preprocessing.LabelEncoder()
    labelFields = sklearn.preprocessing.LabelEncoder()
    labelLocations = sklearn.preprocessing.LabelEncoder()
    labelJobLevels = sklearn.preprocessing.LabelEncoder()
    hotEncoder = sklearn.preprocessing.OneHotEncoder(handle_unknown='ignore')

    def train_model(self, max=999999):
        self.clf = RandomForestClassifier(max_depth=max, n_estimators=5)
        self.clf = self.clf.fit(self.collection.data, self.collection.target)
        return self.clf

    # This Method is to train the encoder also return the data
    def encodeDatas(self, encoder, datas):
        encoder.fit(datas)
        encodedData = encoder.transform(datas)
        return encodedData

    def decide(self, input_data):
        if self.decision_tree_classifier == None:
            self.generateDecisionTree()

        if input_data["location"] not in list(self.labelLocations.classes_):
            return ["Location Not in Recommendation List"]
        if input_data["degree"] not in list(self.labelDegrees.classes_):
            return ["Degree Not in Recommendation List"]
        if input_data["major"] not in list(self.labelMajors.classes_):
            return ["Major Not in Recommendation List"]
        if input_data["industry"] not in list(self.labelIndustries.classes_) and input_data["industry"] is not None:
            return ["Industry Not in Recommendation List"]
        if input_data["field"] not in list(self.labelFields.classes_) and input_data["field"] is not None:
            return ["Field Not in Recommendation List"]
        if input_data["job_level"] not in list(self.labelJobLevels.classes_) and input_data["job_level"] is not None:
            return ["Job Level in Recommendation List"]

        hot_data = np.array([self.labelDegrees.transform([input_data["degree"]])[0],
            self.labelMajors.transform([input_data["major"]])[0],
            self.labelIndustries.transform([input_data["industry"]])[0] if input_data["industry"] is not None else 99999,
            self.labelFields.transform([input_data["field"]])[0] if input_data["field"] is not None else 99999,
            self.labelLocations.transform([input_data["location"]])[0],
            self.labelJobLevels.transform([input_data["job_level"]])[0] if input_data["job_level"] is not None else 99999
        ])


        hot_encoded_data = self.hotEncoder.transform(hot_data.reshape(1, -1))
        list_value_input = [
            input_data["min_age"], input_data["max_age"],
            input_data["work_exp"],
            input_data["min_salary"], input_data["max_salary"]
        ]

        list_value_input.extend(hot_encoded_data.toarray()[0])

        value_input = np.array(list_value_input)
        return self.decision_tree_classifier.predict(
            value_input.reshape(1, -1))

    def __init__(self):
        print "Hot JobRecommendationDecisionTree Created"

    def generateDecisionTree(self):
        jobs = Job.objects.all()
        categorical_job_data = []

        listDegrees = []
        listMajors = []
        listIndustries = []
        listFields = []
        listLocations = []
        listJobLevels = []
        for job in jobs:
            listDegrees.append(job.degree)
            listMajors.append(job.major)
            listIndustries.append(job.industry)
            listFields.append(job.field)
            listLocations.append(job.location)
            listJobLevels.append(job.job_level)

        encodedDegrees = self.encodeDatas(self.labelDegrees, listDegrees)
        encodedMajors = self.encodeDatas(self.labelMajors, listMajors)
        encodedIndustries = self.encodeDatas(self.labelIndustries,
                                             listIndustries)
        encodedFields = self.encodeDatas(self.labelFields, listFields)
        encodedLocations = self.encodeDatas(self.labelLocations, listLocations)
        encodedJobLevels = self.encodeDatas(self.labelJobLevels, listJobLevels)

        for i in range(0, len(jobs) - 1):
            #hot model
            temp = []
            temp.append(encodedDegrees[i])
            temp.append(encodedMajors[i])
            temp.append(encodedIndustries[i])
            temp.append(encodedFields[i])
            temp.append(encodedLocations[i])
            temp.append(encodedJobLevels[i])
            categorical_job_data.append(temp)

        hotEncoderData = self.hotEncoder.fit_transform(categorical_job_data)

        i = 0 
        for hc in hotEncoderData:
            temp_data = [jobs[i].min_age, jobs[i].max_age, jobs[i].work_exp, jobs[i].min_salary, jobs[i].max_salary]
            temp_data.extend(hc.toarray()[0])
            print jobs[i].title
            temp_target = str(jobs[i].title.encode('utf-8'))

            self.jobDatas.append(temp_data)
            self.targetDatas.append(temp_target)
            i += 1
        active_features = ["Min Age", "Max Age","Work Exp", "Min Salary", "Max Salary"]
        active_features.extend(self.hotEncoder.active_features_)

        self.collection = sklearn.datasets.base.Bunch(
            data=np.array(self.jobDatas),
            target=np.array(self.targetDatas),
            feature_names=active_features,
            target_names=self.targetDatas)

        self.decision_tree_classifier = self.train_model()
