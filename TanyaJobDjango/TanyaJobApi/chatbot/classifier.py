import sklearn.datasets as skd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


class TextClassifier:
    classifier = MultinomialNB()
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    target = []

    def __init__(self):
        print "Learning Classifier"
        categories = [
            'Age', 'Degree', 'Facilities', 'Field', 'Industry', 'JobLevel',
            'Major', 'Salary', 'Location', 'WorkExperience', 'SkillSet', 'Other'
        ]
        data_train = skd.load_files(
            './chatbot/CustomCorpusChatbot',
            categories=categories)
        self.target = data_train.target_names
        x_train_tf = self.count_vect.fit_transform(data_train.data)

        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_tf)

        self.classifier.fit(x_train_tfidf, data_train.target)

    def predict(self, text):
        text_counts = self.count_vect.transform(text)
        text_tfidf = self.tfidf_transformer.transform(text_counts)
        predicted = self.classifier.predict(text_tfidf)
        categories = []
        for x in predicted:
            categories.append(self.target[x])
        return categories


class FreshGraduateClassifier:
    classifier = MultinomialNB()
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    target = []

    def __init__(self):
        print "Learning FreshGraduateClassifier"
        categories = ['True', 'False']
        data_train = skd.load_files(
            './chatbot/CustomCorpusChatbot/FreshGraduate',
            categories=categories)
        self.target = data_train.target_names

        print data_train.data


        x_train_tf = self.count_vect.fit_transform(data_train.data)


        print ("Print Vocabulary > " + str(self.count_vect.vocabulary_))

        for i in range(len(data_train.data)):
            print "Dokumen ke-",i
            print data_train.data[i].split('\n')

        for x in x_train_tf[7]:
            print x

        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_tf)

        for x in x_train_tfidf[7]:
            print x

        print x_train_tf
        print x_train_tfidf

        self.classifier.fit(x_train_tfidf, data_train.target)

    def predict(self, text):
        text_counts = self.count_vect.transform(text)
        print text_counts
        text_tfidf = self.tfidf_transformer.transform(text_counts)
        print text_tfidf
        predicted = self.classifier.predict(text_tfidf)
        categories = []
        for x in predicted:
            if self.target[x] == "True":
                categories.append(True)
            else:
                categories.append(False)
        return categories
