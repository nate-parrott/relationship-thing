import flask
app = flask.Flask(__name__)
import os
from classifiers import prob_couple_will_not_break_up

def serve_static(filename):
	path = os.path.join(os.path.dirname(__file__), filename)
	return open(path).read()

@app.route('/')
def index():
	return serve_static('index.html')

@app.route('/quiz')
def quiz():
	return serve_static('quiz.html')

@app.route('/quiz', methods=['POST'])
def get_result():
	feature_dict = {key: (values[0] if len(values) else '') for key, values in flask.request.form.iteritems()}
	print feature_dict
	p = prob_couple_will_not_break_up(feature_dict)
	return flask.redirect('/quiz/result/{0}'.format(p))

@app.route('/quiz/result/<prob>')
def result(prob):
	prob = float(prob)
	
	html_path = os.path.join(os.path.dirname(__file__), 'result.html')
	html = open(html_path).read()
	
	html = html.replace("<!--PERCENT-->", str(int(prob * 100)))
	
	return html

if __name__ == "__main__":
    app.run(debug=True)
