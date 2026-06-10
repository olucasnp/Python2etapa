from flask import Flask

app = Flask(__name__)

@app.route("/decorator")
def decorate():
    return """
Um decorator em Python é um padrão de projeto estrutural que permite adicionar funcionalidades" 
    "a uma função ou método existente sem modificar seu código original. Ele é, essencialmente, uma função que recebe outra função como parâmetro, "
    estende seu comportamento e retorna uma nova função decorada
    
"""

if __name__ == "__main__":
    app.run(debug = True)