from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return "Health OK!"

if __name__ =="__main__":
    app.run(debug=True)