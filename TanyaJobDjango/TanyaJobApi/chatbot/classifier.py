import sklearn.datasets as skd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import math 



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

        x_train_tf = self.count_vect.fit_transform(data_train.data)
        


        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_tf)

        self.classifier.fit(x_train_tfidf, data_train.target)
        #FOR DEBUG PURPOSE ONLY
        print data_train.target
        print len(self.count_vect.vocabulary_)
        print ("Print Vocabulary > " + str(self.count_vect.vocabulary_))

        for i in range(len(data_train.data)):
            print "Dokumen ke-",i
            print data_train.data[i].split('\n')
        all_array_temp2 = []
        all_array_temp = []
        for i in range(len(data_train.data)):
            for x in x_train_tfidf[i]:
                temp = x.toarray()[0]
                temp2 = x_train_tf[i].toarray()[0]
                print temp
                for t in range(len(temp2)):
                    if temp2[t] != 0:
                        temp2[t] = 1
                all_array_temp2.append(temp2)
                all_array_temp.append(temp)

        print sum(all_array_temp2)
        for i in range(len(data_train.data)):
            for x in x_train_tfidf[i]:
                temp = x.toarray()[0]
                temp2 = x_train_tf[i].toarray()[0]
                total_tfidf = 0
                for j in range(len(temp)):
                    idf = math.log(float((1 + len(data_train.data)))/(1 + sum(all_array_temp2)[j])) + 1.0000000000
                    tfidf = idf * temp2[j]
                    print "D : ", i,"\tT :", j, "\ttf(t,d) :", temp2[j],"\tdf(t) :", sum(all_array_temp2)[j],"\tidf :","%.5f" % idf,"\ttf-idf :","%.5f" % tfidf,"\ttf-idf (norm): ","%.5f" % temp[j]
                    total_tfidf += (tfidf * tfidf)
                print "Pembagi tfidf pada Dokumen ke-",i," >> ", math.sqrt(total_tfidf)
                print "-------------------------------------------------------------------------------------------------------"

        for i in range(len(data_train.data)):
            print "---------Dokumen ke-",i
            for x in x_train_tfidf[i]:
                temp = x.toarray()[0]
                temp2 = x_train_tf[i].toarray()[0]
                for j in range(len(temp)):
                    if j == 38 or j == 54 or j == 64:
                        print "Kata ke-",j ,"muncul sebanyak ", temp2[j], " kali dan memiliki nilai setelah dilakukan idf > ", temp[j]
        print self.classifier.class_count_
        print self.classifier.feature_count_
        for j in range(len(self.classifier.feature_count_[0])):
            if j == 38 or j == 54 or j == 64:
                print "Kata ke-",j ,"memiliki nilai sebesar Pada kategori False", self.classifier.feature_count_[0][j], " nilai akhir ", (self.classifier.feature_count_[0][j] + 1) / ( sum(self.classifier.feature_count_[0]) + len(self.count_vect.vocabulary_))
                print "Kata ke-",j ,"memiliki nilai sebesar Pada kategori True", self.classifier.feature_count_[1][j], " nilai akhir ",(self.classifier.feature_count_[1][j] + 1) / ( sum(self.classifier.feature_count_[1]) + len(self.count_vect.vocabulary_))
                print "----------------------------------------------------------------------------------------------------------"
        print sum(self.classifier.feature_count_[0])
        print sum(self.classifier.feature_count_[1])

    def predict(self, text):
        text_counts = self.count_vect.transform(text)
        print text_counts
        text_tfidf = self.tfidf_transformer.transform(text_counts)
        print self.tfidf_transformer.idf_
        print text_tfidf
        predicted = self.classifier.predict(text_tfidf)
        print self.classifier.predict_proba(text_tfidf)
        categories = []
        for x in predicted:
            if self.target[x] == "True":
                categories.append(True)
            else:
                categories.append(False)
        return categories
