from .models import Job
import numpy as np
import pydotplus
import numpy as np
import sklearn.datasets
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn import preprocessing
from IPython.display import Image, display
import MySQLdb


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

class JobRecommendationDecisionTree:
    decision_tree_classifier = None
    collection = sklearn.datasets.base.Bunch()
    clf = tree.DecisionTreeClassifier()

    jobDatas = [] # other from title
    targetDatas = [] # title
    # Label Encoder
    labelDegrees = sklearn.preprocessing.LabelEncoder()
    labelMajors = sklearn.preprocessing.LabelEncoder()
    labelIndustries = sklearn.preprocessing.LabelEncoder()
    labelFields = sklearn.preprocessing.LabelEncoder()
    labelLocations = sklearn.preprocessing.LabelEncoder()
    labelJobLevels = sklearn.preprocessing.LabelEncoder()

    def train_model(self,max=999999):
        self.clf = tree.DecisionTreeClassifier(max_depth=max)
        self.clf = self.clf.fit(self.collection.data, self.collection.target)
        return self.clf

    # This Method is to train the encoder also return the data
    def encodeDatas(self, encoder, datas):
        encoder.fit(datas)
        encodedData = encoder.transform(datas)
        return encodedData

    def display_image(self):
        dot_data = tree.export_graphviz(self.decision_tree_classifier, out_file=None,
                                        feature_names=self.collection.feature_names,
                                        class_names=self.collection.target_names,
                                        filled=True, rounded=True)

        graph = pydotplus.graph_from_dot_data(dot_data)
        display(Image(data=graph.create_png()))
        # Create PNG
        graph.write_png("iris.png")

    def decide(self, input_data):
        if self.decision_tree_classifier == None:
            self.generateDecisionTree()
        list_value_input = [
            self.labelDegrees.transform([input_data["degree"]])[0],
            self.labelMajors.transform([input_data["major"]])[0],
            self.labelIndustries.transform([input_data["industry"]])[0],
            input_data["min_age"],
            input_data["max_age"],
            self.labelFields.transform([input_data["field"]])[0],
            self.labelLocations.transform([input_data["location"]])[0],
            self.labelJobLevels.transform([input_data["job_level"]])[0],
            input_data["work_exp"],
            input_data["min_salary"],
            input_data["max_salary"]
        ]

        value_input = np.array(list_value_input)
        return self.decision_tree_classifier.predict(value_input.reshape(1, -1))

    def __init__(self) :
         print "JobRecommendationDecisionTree Created"

    def generateDecisionTree(self):
        jobs = Job.objects.all()
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
        encodedIndustries = self.encodeDatas(self.labelIndustries, listIndustries)
        encodedFields = self.encodeDatas(self.labelFields, listFields)
        encodedLocations = self.encodeDatas(self.labelLocations, listLocations)
        encodedJobLevels = self.encodeDatas(self.labelJobLevels, listJobLevels)

        for i in range(0, len(jobs) - 1):
            temp_data = [encodedDegrees[i], encodedMajors[i], encodedIndustries[i], 
                         jobs[i].min_age, jobs[i].max_age, encodedFields[i], encodedLocations[i],
                         encodedJobLevels[i], jobs[i].work_exp, jobs[i].min_salary, jobs[i].max_salary]

            listDegrees.append(job.degree)
            listMajors.append(job.major)
            listIndustries.append(job.industry)
            listFields.append(job.field)
            listLocations.append(job.location)
            listJobLevels.append(job.job_level)

            temp_target = str(jobs[i].title)
            self.jobDatas.append(temp_data)
            self.targetDatas.append(temp_target)

        self.collection = sklearn.datasets.base.Bunch(
            data=np.array(self.jobDatas), 
            target=np.array(self.targetDatas),
            feature_names=["Last Degree", "Major", "Industry","Min Age", "Max Age","Fields","Locations","Job Levels","Work Exp", "Min Salary", "Max Salary"], 
            target_names=self.targetDatas)
        
        self.decision_tree_classifier = self.train_model()
        self.display_image()
