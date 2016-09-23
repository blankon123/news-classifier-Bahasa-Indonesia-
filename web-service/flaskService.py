from flask import Flask, jsonify, request
import json
from newsModule import *

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

from datetime import datetime as dt
import cPickle as pickle
from datetime import datetime as dt


app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
		#json_ = request.json
	with open('sample1.json') as data_file:    
		dataJson = json.load(data_file)
	ids     = [z['id'] for z in dataJson['text']]
	X_train = [z['text'] for z in dataJson['text']]
	y_preds = clf.predict(X_train).tolist()
	resp = [{'id':ids[i],'flag':y_preds[i]*2} for i in range(0,len(ids))]
	return jsonify(resp)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
	dataJson= request.json
	ids     = [z['id'] for z in dataJson['text']]
	X_train = [z['text'] for z in dataJson['text']]
	y_preds = clf.predict(X_train).tolist()
	resp = [{'id':ids[i],'flag':y_preds[i]*2} for i in range(0,len(ids))]
	return jsonify(resp)

@app.route('/relearn', methods=['GET'])
def relearn():
	vectPost = TfidfVectorizer(stop_words=stopwords,preprocessor=posTag,decode_error='ignore')
	#vectStem = TfidfVectorizer(stop_words=stopwords,preprocessor=rmStem,decode_error='ignore')
	mnb = MultinomialNB(alpha=0.1)
	dataDeploy = pickle.load( open( ".."+"\\"+"v1.4\DATA_SHORT.p", "rb" ) )
	ydataDeploy= pickle.load( open( ".."+"\\"+"v1.4\DATA_TARGET.p", "rb" ) )

	modlDeploy = mnb
	vectDeploy = vectPost
	pipeDeploy = Pipeline([('vect', vectDeploy),('clf', modlDeploy)])
	modelReady = pipeDeploy.fit(dataDeploy, ydataDeploy)
	
	date = dt.now().strftime("%d-%m-%Y %I%p")
	joblib.dump(modelReady, 're-learn\model '+date+'.pkl')
	return "Sukses Learn"+date

if __name__ == '__main__':
	clf         = joblib.load('model3.pkl')
	app.run(port=8080)