import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)

# 🔒 Clave secreta (segura con variable de entorno)
app.secret_key = os.getenv("SECRET_KEY")

# 📧 Configuración de correo (usa variables de entorno)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")  # tu Gmail
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")  # tu contraseña de aplicación

mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        if not nombre or not correo or not mensaje:
            flash("Por favor, completa todos los campos.", "danger")
            return redirect(url_for("index"))

        try:
            msg = Message(
                subject=f"Nuevo mensaje de contacto de {nombre}",
                sender=app.config["MAIL_USERNAME"],
                recipients=[app.config["MAIL_USERNAME"]],
                body=f"De: {nombre} <{correo}>\n\nMensaje:\n{mensaje}",
            )
            mail.send(msg)
            flash("¡Mensaje enviado correctamente!", "success")
        except Exception as e:
            print("Error:", e)
            flash("Ocurrió un error al enviar el mensaje.", "danger")

        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
