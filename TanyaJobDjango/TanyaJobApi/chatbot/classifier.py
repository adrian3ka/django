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
        categories = ['Age',
                      'Degree',
                      'Facilities',
                      'Field',
                      'Industry',
                      'JobLevel',
                      'Major',
                      'Salaries',
                      'Location',
                      'WorkExperiences']
        data_train = skd.load_files('./chatbot/CustomCorpusChatbot', categories=categories,
                                encoding='ISO-8859-1')
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