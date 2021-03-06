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
import gc
import MySQLdb
from django.db import connection, transaction
from sklearn.tree._tree import TREE_LEAF

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

    MINIMUM_AGREED_TREE = 3
    TREE_COUNT = 50
    MAX_DEPTH = 700
    PARALEL_ESTIMATOR = 2
    THRESHOLD = float(MINIMUM_AGREED_TREE) / float(TREE_COUNT)

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
        self.clf = RandomForestClassifier(max_depth=max, n_estimators=self.TREE_COUNT, n_jobs = self.PARALEL_ESTIMATOR, criterion="gini", bootstrap=False, verbose=10)
        self.clf = self.clf.fit(self.collection.data, self.collection.target)
        return self.clf

    # This Method is to train the encoder also return the data
    def encodeDatas(self, encoder, datas):
        encoder.fit(datas)
        encodedData = encoder.transform(datas)
        return encodedData

    def cost_complexity_prune(self, inner_tree, index, threshold):
        print inner_tree.value[index].max(), threshold
        if inner_tree.value[index].min() < threshold:
            # turn node into a leaf by "unlinking" its children
            inner_tree.children_left[index] = TREE_LEAF
            inner_tree.children_right[index] = TREE_LEAF
        # if there are shildren, visit them as well
        if inner_tree.children_left[index] != TREE_LEAF:
            self.cost_complexity_prune(inner_tree, inner_tree.children_left[index], threshold)
        if inner_tree.children_right[index] != TREE_LEAF:
            self.cost_complexity_prune(inner_tree, inner_tree.children_right[index], threshold)

    def decide(self, input_data):
        if self.decision_tree_classifier == None:
            self.generateDecisionTree()

        if input_data["location"] not in list(self.labelLocations.classes_):
            input_data["location"] = 'Tidak disebutkan'
            #return ["Location Not in Recommendation List"]
        if input_data["degree"] not in list(self.labelDegrees.classes_):
            input_data["degree"] = 'Tidak disebutkan'
            #return ["Degree Not in Recommendation List"]
        if input_data["major"] not in list(self.labelMajors.classes_):
            input_data["major"] = 'Tidak disebutkan'
            #return ["Major Not in Recommendation List"]
        if input_data["industry"] not in list(self.labelIndustries.classes_) or input_data["industry"] is None:
            cursor = connection.cursor()
            cursor.execute("SELECT industry FROM tanyajob_chat.job_job WHERE major = '" + input_data["major"] + "' GROUP BY industry ORDER BY COUNT(*) DESC LIMIT 1;")
            records = cursor.fetchone()
            print records[0]
            input_data["industry"] = records[0]
            
            cursor.close()
            #return ["Industry Not in Recommendation List"]
        if input_data["field"] not in list(self.labelFields.classes_) or input_data["field"] is None:
            cursor = connection.cursor()
            cursor.execute("SELECT field FROM tanyajob_chat.job_job WHERE major = '" + input_data["major"] + "' GROUP BY field ORDER BY COUNT(*) DESC LIMIT 1;")
            records = cursor.fetchone()
            print records[0]
            input_data["field"] = records[0]
            
            cursor.close()
            #return ["Field Not in Recommendation List"]
        if input_data["job_level"] not in list(self.labelJobLevels.classes_) or input_data["job_level"] is None:
            input_data["job_level"] = 'Staff'
            #return ["Job Level in Recommendation List"]
        if input_data["work_exp"] is None:
            input_data["work_exp"] = 0

        #print input_data

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
        temp = self.decision_tree_classifier.predict_proba(
            value_input.reshape(1, -1))
        vote_result = temp[0]
        recommended_job = []
        for i in range(len(vote_result)):
            if vote_result[i] > 0:
                print vote_result[i], self.THRESHOLD, " > ", self.decision_tree_classifier.classes_[i]
            if vote_result[i] >= self.THRESHOLD:
                recommended_job.append({
                    "title" : self.decision_tree_classifier.classes_[i],
                    "score" : vote_result[i],
                })
        #print recommended_job
        ordered_job = sorted(recommended_job, key=lambda k: k['score'], reverse=True)
        #print ordered_job 
        extracted_title = []
        for o in ordered_job:
            extracted_title.append(o["title"])

        if len(extracted_title) == 0:
            extracted_title = self.decision_tree_classifier.predict(
            value_input.reshape(1, -1))

        gc.collect()
        return extracted_title

    def __init__(self):
        print "Hot JobRecommendationDecisionTree Created"

    def generateDecisionTree(self):
        print "-----------------------Getting All Job-------------------------"
        jobs = Job.objects.all()
        categorical_job_data = []

        listDegrees = []
        listMajors = []
        listIndustries = []
        listFields = []
        listLocations = []
        listJobLevels = []
        print "-----------------------Loop All Job----------------------------"
        for i in range(0, len(jobs) - 1):
            listDegrees.append(jobs[i].degree)
            listMajors.append(jobs[i].major)
            listIndustries.append(jobs[i].industry)
            listFields.append(jobs[i].field)
            listLocations.append(jobs[i].location)
            listJobLevels.append(jobs[i].job_level)
        gc.collect()

        encodedDegrees = self.encodeDatas(self.labelDegrees, listDegrees)
        encodedMajors = self.encodeDatas(self.labelMajors, listMajors)
        encodedIndustries = self.encodeDatas(self.labelIndustries,
                                             listIndustries)
        encodedFields = self.encodeDatas(self.labelFields, listFields)
        encodedLocations = self.encodeDatas(self.labelLocations, listLocations)
        encodedJobLevels = self.encodeDatas(self.labelJobLevels, listJobLevels)

        print "-----------------------Encode All Job--------------------------"
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

        del listDegrees 
        del listMajors 
        del listIndustries
        del listFields
        del listLocations
        del listJobLevels
        gc.collect()

        i = 0 
        print "--------------------Hot Encode All Job-------------------------"
        for hc in hotEncoderData:
            temp_data = [jobs[i].min_age, jobs[i].max_age, jobs[i].work_exp, jobs[i].min_salary, jobs[i].max_salary]
            temp_data.extend(hc.toarray()[0])
            temp_target = str(jobs[i].title.encode('utf-8'))

            self.jobDatas.append(temp_data)
            self.targetDatas.append(temp_target)
            i += 1
        gc.collect()
        active_features = ["Min Age", "Max Age","Work Exp", "Min Salary", "Max Salary"]
        active_features.extend(self.hotEncoder.active_features_)

        self.collection = sklearn.datasets.base.Bunch(
            data=np.array(self.jobDatas),
            target=np.array(self.targetDatas),
            feature_names=active_features,
            target_names=self.targetDatas)

        del jobs
        gc.collect()
        print "-----------------------Train All Job---------------------------"
        self.decision_tree_classifier = self.train_model(self.MAX_DEPTH)
        self.jobDatas = None
        self.targetDatas = None
        gc.collect()
        for i in range(len(self.decision_tree_classifier.estimators_)):
            print "Depth ", self.decision_tree_classifier.estimators_[i].tree_.node_count
            #self.decision_tree_classifier.prune_tree()
            #self.cost_complexity_prune(self.decision_tree_classifier.estimators_[i].tree_, 1, 10)
            print "Depth ", self.decision_tree_classifier.estimators_[i].tree_.node_count
            print "----------------------------------------------------------"
