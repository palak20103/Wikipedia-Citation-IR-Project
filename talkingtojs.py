import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
import scrappingfiles as scrap
import pre
from pre import preprocess_fun

app = flask.Flask(__name__)
CORS(app)

@app.route('/test', methods=['POST'])
def test():
    if not request.json:
        output = {
            'demo': "not done"
        }
    else:

        PageName = request.json['page']
        Query = request.json['query']
        currenturl = 'https://en.wikipedia.org/wiki/' + PageName
        CitationsExtData, CitationsIntData, QueryString = scrap.getCitationsQuery(currenturl, Query)

        v1 = ob.getDoc2Vec(CitationsExtData, model)
        v2 = ob.getWord2Vec(QueryString,model2)
        scores = []
        for i in range(len(v1)):
            scores.append(ob.cosine_similarity(v1[i], v2))
        s = ""
        for lines in CitationsExtData:
            s = s + lines
        CitationsExtData = s
        rank = ob.ranking(CitationsExtData, scores)

        output = {'demo': "done",
                  'data': QueryString,
                  'citations': CitationsExtData,
                  'res': rank[0]
                  }

    return jsonify(output), 201


global ob
global model
global model2
ob = preprocess_fun()
model = ob.loadmodelD2V()
model2 = ob.getWord2VecModel()
app.run(debug=True)
