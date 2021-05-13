#!/usr/bin/env python
import os
import json
from flask import Flask, g, Response, request, render_template, jsonify, url_for
from pandas import DataFrame
from neo4j import GraphDatabase, basic_auth

app = Flask(__name__)

#password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("johnny", "jc123456"), encrypted=False)

def runQuery(query):
    """https://neo4j.com/docs/labs/apoc/current/export/json/#export-json-stream-export
        6.2.4.4. Export results of Cypher query to JSON
    """
    db = get_db()
    apoc = f"""
            CALL apoc.export.json.query(
	        "{query}",
	        null,
	        {{stream: true}}
            )
            YIELD data
            RETURN data
        """
    print(apoc)
    results = db.run(apoc)
    db.close()
    return results

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()

@app.route("/", methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        
        try:
            query = request.form['content']
            results = runQuery(query) #executes query with APOC and returns bolt object
            result = results.single()[0] #returns string 'data' from bolt object
            resultdict = json.loads(result) #converts string data to python dict
            resultDataFrame = DataFrame.from_dict(resultdict) #converts dict to Pandas DataFrame
            resulthtml = resultDataFrame.to_html(header="true") #converts DataFrame to html

            return render_template('index.html', results=resulthtml)
        except Exception as e:
            return render_template('index.html', error=e)
    else: 
        return render_template('index.html')


@app.route("/api", methods=['POST'])
def _api():
    
    try:
        cypher = request.json['cypher'] #returns json body cypher query
        results = runQuery(cypher) #executes query with APOC and returns bolt object
        result = results.single()[0] #returns string data from bolt object
        resultdict = json.loads(result) #converts string data to python dict
        return jsonify(resultdict) #returns http response object with json payload
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run(debug=True)
