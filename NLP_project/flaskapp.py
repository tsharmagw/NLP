from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    es,index_id=elastic_object()
    print(index_id["ach"])
    output=es.get(index=processed_text.lower(), doc_type="_doc",id=index_id[processed_text.lower()])
    return(output["_source"]["Pages"])

def elastic_object():
	from elasticsearch import Elasticsearch, RequestsHttpConnection
	from requests_aws4auth import AWS4Auth
	import boto3
	host = 'search-elasticnlp-ojs2iluobhrf4m7jhbzp77wvwq.us-east-1.es.amazonaws.com'

	region = 'us-east-1' 

	service = 'es'
	credentials = boto3.Session().get_credentials()
	print(credentials.access_key)
	awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)
	es = Elasticsearch(
	    hosts = [{'host': host, 'port': 443}],
	    http_auth = awsauth,
	    use_ssl = True,
	    verify_certs = True,
	    connection_class = RequestsHttpConnection
	)
	index_id={}
	data=open("index_file.csv","r").readlines()
	for i in data:
		key=i.split(",")[0]
		value=int(i.split(",")[1].replace("\n",""))
		index_id[key]=value
	return es,index_id


if __name__=="__main__":
    app.run(host="0.0.0.0", port=80)
