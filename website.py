from flask import Flask
app = Flask(__name__)
import os

@app.route('/')
def index():
	index_path = os.path.join(os.path.dirname(__file__), 'index.html')
	return open(index_path).read()

if __name__ == "__main__":
    app.run(debug=True)
