from flask import Flask, request, make_response
import subprocess

app = Flask(__name__)

app.secret_key = open('/home/admin/secret.txt','r').read()

@app.route('/')
def home():
	response = make_response(open(__file__,'r').read())
	response.headers["Content-Type"] = "text/text"
	return response

@app.route('/secure')
def secure():
	url = request.args.get('url').lower()
	if not url:
		return make_response("Missing Parameter.")

	disallowed_chars = ['&', '|', ';', '\n', '`', '$(', ' ', '%']

	if any(c in url for c in disallowed_chars):
		return make_response("Bad Input.")

	blacklist = ['file','ftp','dict','gopher','ldap']

	if any(protocol in url for protocol in blacklist):
		return make_response("Protocol not supported.")

	result = subprocess.run(['curl', url, '-m','15'], stdout=subprocess.PIPE)
	response = make_response(result.stdout.decode())
	response.headers["Content-Type"] = "text/text"
	return response

if __name__ == '__main__':
	app.run('0.0.0.0',8080)
