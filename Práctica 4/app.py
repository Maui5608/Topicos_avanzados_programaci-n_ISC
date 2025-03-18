from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesario para usar flash()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="maui",
        database="inventario_recetas"
    )

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recetas")
        recetas = cursor.fetchall()
    except Exception as e:
        flash(f"Error al obtener recetas: {e}", "danger")
        recetas = []
    finally:
        conn.close()
    
    return render_template('index.html', recetas=recetas)

@app.route('/add', methods=['POST'])
def add():
    nombre = request.form['nombre'].strip()
    ingredientes = request.form['ingredientes'].strip()
    pasos = request.form['pasos'].strip()

    if not nombre or not ingredientes or not pasos:
        flash("Todos los campos son obligatorios", "warning")
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si la receta ya existe
        cursor.execute("SELECT COUNT(*) FROM recetas WHERE nombre = %s", (nombre,))
        (existe,) = cursor.fetchone()

        if existe > 0:
            flash("La receta ya existe en el inventario", "warning")
        else:
            cursor.execute(
                "INSERT INTO recetas (nombre, ingredientes, pasos) VALUES (%s, %s, %s)",
                (nombre, ingredientes, pasos)
            )
            conn.commit()
            flash("Receta agregada con éxito", "success")

    except Exception as e:
        flash(f"Error al agregar receta: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recetas WHERE id = %s", (id,))
        conn.commit()
        flash("Receta eliminada con éxito", "success")
    except Exception as e:
        flash(f"Error al eliminar receta: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    nombre = request.form['nombre'].strip()
    ingredientes = request.form['ingredientes'].strip()
    pasos = request.form['pasos'].strip()

    if not nombre or not ingredientes or not pasos:
        flash("Todos los campos son obligatorios", "warning")
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE recetas SET nombre = %s, ingredientes = %s, pasos = %s WHERE id = %s",
            (nombre, ingredientes, pasos, id)
        )
        conn.commit()
        flash("Receta actualizada con éxito", "success")
    except Exception as e:
        flash(f"Error al actualizar receta: {e}", "danger")
    finally:
        conn.close()
    
    return redirect('/')

