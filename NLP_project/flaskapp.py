from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text']
	processed_text = text.split(",")
	es,index_id=elastic_object()
	pages_list=''
	for i in processed_text:
		output=es.get(index=i.lower(), doc_type="_doc",id=index_id[i.lower()])
		pages_list=pages_list+","+output["_source"]["Pages"]
	pages=pages_list.split(",")
	data=""
	for i in pages:
		if(i!=""):
			data=data+"<br><h1>"+i+"</h1><br>"
			data=data+read_file(i)

	return(data)
    

def read_file(filename):
	input_file_text = open(filename , encoding='utf-8').read()
	return input_file_text

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

	data1=open("index_file1.csv","r").readlines()
	for j in data1:
		key=j.split(",")[0]
		value=int(j.split(",")[1].replace("\n",""))
		index_id[key]=value
	
	return es,index_id


if __name__=="__main__":
    app.run(host="0.0.0.0", port=80)
