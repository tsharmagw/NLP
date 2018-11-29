from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/jargon')
def my_jargon():
	jargons_list=[]
	data1=open("index_file1.csv","r").readlines()
	for j in data1:
		key=j.split(",")[0]
		jargons_list.append(key)

	data="<!DOCTYPE html><html><head>"
	data=data+"<title align=center>"+"Jargons List"+"</title>"
	data=data+"<h2 align=center>Jargons List</h2>"
	data=data+"<table style=width:100%>"
	for i in range(0,len(jargons_list),10):
		j=i
		data=data+"<tr>"
		while(j<(i+10) and j< len(jargons_list)):
			data=data+"<td>"+jargons_list[j]+"</td>"
			j=j+1
		data=data+"</tr>"


	data=data+"</table>"
	data=data+"</head></html>"
    # return render_template('jargon.html')
	return(data)

@app.route('/abbr')
def my_abbr():
	data=open("index_file.csv","r").readlines()
	abbr_list=[]
	for i in data:
		key=i.split(",")[0]
		abbr_list.append(key)

	data="<!DOCTYPE html><html><head>"
	data=data+"<title align=center>"+"Abbreviation List"+"</title>"
	data=data+"<h2 align=center>Abbreviation List</h2>"
	data=data+"<table style=width:100%>"
	for i in range(0,len(abbr_list),10):
		j=i
		data=data+"<tr>"
		while(j<(i+10) and j<len(abbr_list)):
			data=data+"<td>"+abbr_list[j]+"</td>"
			j=j+1
		data=data+"</tr>"


	data=data+"</table>"
	data=data+"</head></html>"
    # return render_template('jargon.html')
	return(data)

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
			start_index_list=[m.start() for m in re.finditer("/",i)]
			data=data+"<br><h1>"+"Page Name: "+i[start_index_list[-2]+1:start_index_list[-1]]+"</h1><br>"
			data=data+read_file(i,processed_text)

	return(data)
    

def read_file(filename,word_list):
	input_file_text = open(filename , encoding='utf-8').read()
	for i in word_list:
		start_index_list=[m.start() for m in re.finditer(i,input_file_text,re.IGNORECASE)]
		if(len(start_index_list)>0):
			a=0
			for j in start_index_list:
				index=j+a*13
				input_file_text=input_file_text[:index]+"<mark>"+input_file_text[index:index+len(i)]+"</mark>"+input_file_text[index+len(i):]
				a=a+1
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
