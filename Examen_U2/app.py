from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="maui",
        database="reservas_citas"
    )

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citas")
        citas = cursor.fetchall()
    except Exception as e:
        flash(f"Error al obtener citas: {e}", "danger")
        citas = []
    finally:
        conn.close()
    
    return render_template('index.html', citas=citas)

@app.route('/add', methods=['POST'])
def add():
    nombre = request.form['nombre'].strip()
    fecha = request.form['fecha'].strip()
    hora = request.form['hora'].strip()
    estado = "Pendiente"

    if not nombre or not fecha or not hora:
        flash("Todos los campos son obligatorios", "warning")
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO citas (nombre, fecha, hora, estado) VALUES (%s, %s, %s, %s)",
            (nombre, fecha, hora, estado)
        )
        conn.commit()
        flash("Cita agregada con éxito", "success")
    except Exception as e:
        flash(f"Error al agregar cita: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    estado = request.form['estado'].strip()
    
    if estado not in ["Pendiente", "Confirmada"]:
        flash("Estado inválido", "warning")
        return redirect('/')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE citas SET estado = %s WHERE id = %s", (estado, id))
        conn.commit()
        flash("Estado actualizado con éxito", "success")
    except Exception as e:
        flash(f"Error al actualizar estado: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM citas WHERE id = %s", (id,))
        conn.commit()
        flash("Cita eliminada con éxito", "success")
    except Exception as e:
        flash(f"Error al eliminar cita: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
