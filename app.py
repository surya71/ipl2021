from flask import Flask, render_template

app = Flask(__name__)

@app.route('/health')
def health():
    return "Health OK!"

@app.route('/')
def home():
    return render_template('home.html')

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html')



if __name__ =="__main__":
    app.run(debug=True)