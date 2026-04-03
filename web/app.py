from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    return render_template("report.html", subject="Dummy Subject")

if __name__ == "__main__":
    app.run(debug=True)