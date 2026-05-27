from flask import Flask, render_template, request
from calculadora import calcular

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method =="POST":
        return calcular()
    return render_template("index.html", etapas="", resultado="")

if __name__ == '__main__':
    app.run(debug=True)