from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "¡Hola desde Flask en el puerto 9999 para la prueba CI/CD!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
