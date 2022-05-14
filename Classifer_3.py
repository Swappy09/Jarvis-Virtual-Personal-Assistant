import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.calibration import CalibratedClassifierCV

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

model = None
count_vect = None
tfidf_transformer = None
x_tfidf = None
labels = None
data_file_name  = "Data.json"
model_file_name = "classifier_model.obj"
count_vect_file = "count_vector.obj"
tfidf_transformer_file = "tfidf_transformer.obj"
Dataset = {}

def remove_stop_words(sent):
    s = stopwords.words('english')
    # s.extend(["show","open","Show","Open"])
    s.remove("you")
    s.remove("me")
    s.remove("for")
    s.remove("do")
    s.remove("i")
    s.remove("did")
    stop_words = set(s)
    word_tokens = word_tokenize(sent)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    if len(filtered_sentence) == 0:
        return ""
    r = " ".join(filtered_sentence)
    return r
def getDataDict(filename):
        f = open(filename)
        text = f.read()
        f.close()
        return ast.literal_eval(text)

def init(training=False):
        global count_vect,tfidf_transformer,model,x_tfidf,labels,Dataset,data_file_name,model_file_name
        Dataset = getDataDict(data_file_name)
        if training :
            Dataset = getDataDict(data_file_name)
            labels = []
            data = []
            stop_words = set(stopwords.words('english'))
            for i in Dataset:
                if i[0]!="-":
                    for j in Dataset[i]['training']:
                        data.append(remove_stop_words(j))
                        labels.append(i)
            
            count_vect = CountVectorizer(ngram_range=(1,4))
            x_train = count_vect.fit_transform(data)
            tfidf_transformer = TfidfTransformer()
            x_train_tfd = tfidf_transformer.fit_transform(x_train)
            makeModel(model_file_name,x_train_tfd,labels)

        else:
            # Load Model,Count_Vect,Tfd_Vect
            model = pickle.load(open(model_file_name, 'rb'))
            count_vect = pickle.load(open(count_vect_file, 'rb'))
            tfidf_transformer = pickle.load(open(tfidf_transformer_file, 'rb'))
            
        
def makeModel(file_name,x_data,labels,set_global=True):
        global model,count_vect
        clf = SGDClassifier(loss="hinge")
        clf = CalibratedClassifierCV(clf)
        clf.fit(x_data,labels)
        # print(clf.score(x_tfidf,labels))
        if file_name!=None:
            f =  open(file_name, 'wb')
            pickle.dump(clf,f)
            f.close()
            f = open(count_vect_file,'wb')
            pickle.dump(count_vect,f)
            f.close()
            f = open(tfidf_transformer_file,'wb')
            pickle.dump(tfidf_transformer,f)
            f.close()
            print("Training Completed")
        if set_global==True:
             model = clf
        else:
            return clf
# Finds the mininum and returns 
# def getScore(modl,predicted,vect,labels):
    # least_score = min(modl.predict_proba(vect)[0])
    # return least_score

# Returns ->  { 'set_context': "intent_name" , "entities":{}" }
def setContext(predicted,context):
    global Dataset
    print(predicted)
    if Dataset[predicted]['sub_intents'] != [] :
        context = {'set_context':predicted,'entities':{}}
    return context

def intentClassifier(text,context={}):
    global count_vect,tfidf_transformer,model
    global Dataset

    # Remove Stop words 
    text = remove_stop_words(text)
    if text=="":
        return None,context
    text = [text]
    # If there is context present
    if context!={}:
    # Make Model + Predict
            intent = context['set_context']
            labels = []
            data = []
            for i in Dataset[intent]['sub_intents']:
                for j in Dataset[i]['training']:
                    data.append(j)
                    labels.append(i)
            c_t = CountVectorizer()
            x_ct = c_t.fit_transform(data)
            tfd = TfidfTransformer()
            x_tfd = tfd.fit_transform(x_ct)
            M = makeModel(None,x_tfd,labels,False)
            
            text_ = tfd.transform((c_t.transform(text)))
            predicted = M.predict(text_)[0]
            least_score = min(M.predict_proba(text_)[0])
            print(least_score)
            # elminate by THRESHOLD
            if least_score <= 0.14:
                return predicted,context
            else: 
                sub = Dataset[predicted]['training']
                print(sub)
                if text[0] in sub:
                    return predicted,context
                
         
# Classify with Main Intent
#     print(text)
    x_ct = count_vect.transform(text)
    x_tfd = tfidf_transformer.transform(x_ct)
    predicted = model.predict(x_tfd)      
    print(min(model.predict_proba(x_tfd)))
    least_score = min(model.predict_proba(x_tfd)[0])
    print(least_score)
    
    # elminate by THRESHOLD   
    if least_score <= 0.08:
            # Set Context if sub_intents found
            context  = setContext(predicted[0],context)
            return predicted[0],context
    else: 
                print("Else part")
                sub = Dataset[predicted[0]]['training']
                print(sub)
                if text[0] in sub:
                    return predicted,context
                else:
                    return None,context
            
init()
if __name__ == "__main__":
    pass
    while True:
        i = input(">>>")
        if i=="train":
            init(training=True)
            continue
        print(intentClassifier(i))
    
