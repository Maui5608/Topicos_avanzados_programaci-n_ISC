from flask import Flask, render_template

app = Flask(_name_)

# Simulación de datos sin base de datos
cuentas = [
    {"folio": "#01", "mesa": 101, "total": 165, "servicio": "comedor"},
    {"folio": "#02", "mesa": 105, "total": 30, "servicio": "llevar"},
    {"folio": "#03", "mesa": 101, "total": 75, "servicio": "comedor"}
]

@app.route('/')
def index():
    return render_template('index.html', cuentas=cuentas)

if _name_ == '_main_':
    app.run(debug=True)
