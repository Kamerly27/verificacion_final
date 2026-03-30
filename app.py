from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

# ---------------- INICIO ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CONSULTAR ----------------
@app.route("/consultar", methods=["POST"])
def consultar():
    doc = request.form["documento"]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM estudiantes WHERE documento=%s", (doc,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return render_template("index.html", error="Documento no encontrado")

    estudiante = {
        "documento": row[0],
        "p_apellido": row[1],
        "s_apellido": row[2],
        "p_nombre": row[3],
        "s_nombre": row[4],
        "titulo": row[5],
        "universidad": row[6],
        "escalafon": row[7],
        "num_escalafon": row[8],
        "tipo_escalafon": row[9],
        "graduado": row[10]
    }

    return render_template("index.html", resultado=estudiante)

# ---------------- LOGIN ----------------
CLAVE_ADMIN = "1234"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        clave = request.form["clave"]
        if clave == CLAVE_ADMIN:
            return render_template("registro.html")
        else:
            return render_template("login.html", error="Clave incorrecta")
    return render_template("login.html")

# ---------------- GUARDAR ----------------
@app.route("/guardar", methods=["POST"])
def guardar():

    datos = (
        request.form["documento"],
        request.form["p_apellido"],
        request.form["s_apellido"],
        request.form["p_nombre"],
        request.form["s_nombre"],
        request.form["titulo"],
        request.form["universidad"],
        request.form["escalafon"],
        request.form["num_escalafon"],
        request.form["tipo_escalafon"],
        request.form["graduado"]
    )

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO estudiantes 
        (documento,p_apellido,s_apellido,p_nombre,s_nombre,titulo,
        universidad,escalafon,num_escalafon,tipo_escalafon,graduado)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, datos)

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")

# ---------------- VERIFICAR PUBLICO ----------------
@app.route("/verificar/<doc>")
def verificar(doc):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM estudiantes WHERE documento=%s", (doc,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("publico.html", estudiante=row)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
