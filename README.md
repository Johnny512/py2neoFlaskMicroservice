# NEO4j API Microservice
    clone-> git@gitlab.one.twcbiz.com:jcastillo02/py2neo-flask-microservice.git
    Create Python Environment-> python -m venv env
    install packages-> python install requirements.txt
    Run the app using-> python app.py
## This API accepts a Cypher query two ways:
### 1. Via the front-end web page.
    Enter your cypher query into the text box and click "submit cypher".
    Use single quotes ' ' when entering query.
### 2. Via the API route /api.
    Use Postman to POST a cypher query in json format.
    1. Choose Header-> application/json
    2. Choose Body->raw->{"cypher": "MATCH (tom {name: 'Tom Hanks'}) RETURN tom"}