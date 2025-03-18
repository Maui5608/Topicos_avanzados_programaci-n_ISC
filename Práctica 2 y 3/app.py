from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesario para usar flash()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="maui",
        database="control_tareas"
    )

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas_2")
        tareas = cursor.fetchall()
    except Exception as e:
        flash(f"Error al obtener tareas: {e}", "danger")
        tareas = []
    finally:
        conn.close()
    
    return render_template('index.html', actividades=tareas)

@app.route('/add', methods=['POST'])
def add():
    actividad = request.form['actividad'].strip()

    if not actividad:
        flash("La actividad no puede estar vacía", "warning")
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la actividad ya existe
        cursor.execute("SELECT COUNT(*) FROM tareas_2 WHERE nombre = %s", (actividad,))
        (existe,) = cursor.fetchone()

        if existe > 0:
            flash("La actividad ya existe en la lista", "warning")
        else:
            cursor.execute("INSERT INTO tareas_2 (nombre) VALUES (%s)", (actividad,))
            conn.commit()
            flash("Tarea agregada con éxito", "success")

    except Exception as e:
        flash(f"Error al agregar tarea: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas_2 WHERE id = %s", (id,))
        conn.commit()
        flash("Tarea eliminada con éxito", "success")
    except Exception as e:
        flash(f"Error al eliminar tarea: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    actividad = request.form['actividad'].strip()

    if not actividad:
        flash("La actividad no puede estar vacía", "warning")
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas_2 SET nombre = %s WHERE id = %s", (actividad, id))
        conn.commit()
        flash("Tarea actualizada con éxito", "success")
    except Exception as e:
        flash(f"Error al actualizar tarea: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')
