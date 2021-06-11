# -*- coding: utf-8 -*-
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk.stem import WordNetLemmatizer 
import re
import contractions as contractions
import gensim
from gensim.corpora import WikiCorpus
import smart_open
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
nltk.download('universal_tagset')

class preprocess_fun:
    
    def preprocess_fun(self):{ }

    def ranking(self,X, Y):
        X = X.split('\n\n')
        score_for_each_para = Y
        return [x for _, x in sorted(zip(score_for_each_para, X))]

    def cosine_similarity(self,set1, set2):
        X_set = list(set1)
        Y_set = set2
        c = 0
        l1 = set1
        l2 = set2
        rvector = len(l1)
        # cosine formula
        for i in range(rvector):
            c += l1[i] * l2[i]
        cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
        return cosine

    def cleaning(self,text):
      line = contractions.fix(text)
      line = re.sub(r'\'(\w|\s)','',line)
      line = re.sub(r'(\.{2,}|\,|\?+|!+|\:|\-\-|\'\'|``|\(|\))','',line)
      line = re.sub(r'[`\!@#$%^&\*()\_+={}\:\;<>\?\|\-\.]',' ', line)
      line = line.lower()
      return line
    
    def tokenization(self,text):
      text_list = word_tokenize(text)
      return text_list;
    
    def removeStopWords(self,text_list):
      llist=[]
      stopwordsList = stopwords.words('english')
      for word in text_list:
        if word not in stopwordsList:
           llist.append(word)
      return llist
    
    def normalization(self,text_list):
      llist=[]
      lemmatizer = WordNetLemmatizer() 
      for word in text_list:
           llist.append(lemmatizer.lemmatize(word))
      return llist
    
    def preprocessing(self,file,flag):
      if(flag==1):
        file_name = open(file,'r')
        # file_create = open('/content/drive/MyDrive/Sem2/IR/Project/Dataset/processed_cleaned.txt','w')
        text = self.cleaning(file_name.read())
        llist = self.tokenization(text)
        llist = self.removeStopWords(llist)
        llist = self.normalization(llist)
        return llist
        # file_create.write(llist)
          
      elif(flag==0):
           text = self.cleaning(file)
           llist = self.tokenization(text)
           llist = self.removeStopWords(llist)
           llist = self.normalization(llist)
           return llist
       
    def getPosTag(self,words):
    
        #Getting POS Tag
        tagList = nltk.pos_tag(words,  tagset='universal')
    
        #Format - WORD_POSTAG
        for i in range(len(words)):
            words[i] = words[i] + '_' + tagList[i][1]
    
        return words

    def getWord2VecModel(self):
        print("loading word2vec model")
        model = KeyedVectors.load_word2vec_format('C:/Users/rahul/Downloads/model.txt', binary=False, unicode_errors='ignore')
        print("loaded model")
        return model
    
    def getWord2Vec(self,fileid,model):
        # words = preprocessing('/content/drive/MyDrive/' + fileid + '.txt', 1)
        words = self.preprocessing(fileid,0)
        #words = ['dog', 'trees', 'king']
        #The I/P to model is words with it's POS Tag
        words = self.getPosTag(words)
    
        # model - trained on wikipedia dump

    
        combinedVector = [0]*300
        #Getting vectors for words
        for word in words:
          if word in model: 
            vector = model[word]
    
            for i in range(len(vector)):
              combinedVector[i] += vector[i] 
    
    
            for i in range(len(combinedVector)):
              combinedVector[i] = combinedVector[i]/ len(words)
          
    
        return combinedVector
    
    def loadmodelD2V(self):
      print("loading model")
      model = gensim.models.Doc2Vec.load('C:/Users/rahul/Downloads/doc2vec.bin')
      print("loaded model")
      return model
    
    def getDoc2Vec(self,sents,model):
      s=""
      for lines in sents:
          s=s+lines
      sents=s
      para_list = sents.split('\n\n')
      Vec_list = []
      for para in para_list:
        test_data = self.preprocessing(para,0)
        vec = model.infer_vector(test_data)
        Vec_list.append(vec)
      print(len(para_list))
      print(len(Vec_list))     
      return Vec_list 



