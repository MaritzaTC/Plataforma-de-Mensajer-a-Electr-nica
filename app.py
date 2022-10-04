from flask import Flask, render_template, request
import hashlib
import controller
from datetime import datetime
import envioemail

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/verificarUsuario", methods=["GET", "POST"])
def verificarUsuario():

    usuario=request.form["txtusuario"]
    password=request.form["txtpass"]

    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()

    respuesta =controller.consultar_usuario(usuario, password2)

    if len(respuesta)==0:
        mensaje ="Error de autentificación, verifique su usuario y contraseña"
        return  render_template("informacion.html", datas=mensaje)
    else:
        respuesta2=controller.lista_destinatarios(usuario)
        return render_template("principal.html", datas=respuesta2)

    
@app.route("/registrarUsuario", methods=["GET", "POST"])
def registrarUsuario():
    if request.method=="POST":
        name=request.form["txtnombre"]
        email=request.form["txtusuarioregistro"]
        passw=request.form["txtpassregistro"]

        password2=passw.encode()
        password2=hashlib.sha384(password2).hexdigest()

        codigo =datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-","")
        codigo2=codigo2.replace(".","")
        codigo2=codigo2.replace(" ","")
        codigo2=codigo2.replace(":","")
        print(codigo2)
        mensaje="Sr "+name+ ",su codigo de activacion es :\n\n"+codigo2+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"
        envioemail.enviar(email,mensaje,"Codido de Activacion")
        respuesta =controller.registrarUsuario(name,email,password2,codigo2)

    
        mensaje="El Usuario"+ name+ " se ha registrado satisfactoriamnete"
        return  render_template("informacion.html", data=mensaje)
        
@app.route("/enviarMail", methods=["GET", "POST"])
def enviarMail():
    if request.method=="POST":
        emailDestino=request.form["emailDestino"]
        asunto=request.form["asunto"]
        mensaje=request.form["mensaje"]
        mensaje2="Sr Usuario, usted recibio un mensaje nuevo, por favor ingrese a la plataforma para observar su email en la pestaña historial \n \n Muchas gracias"
        envioemail.enviar(emailDestino,mensaje2,"Nuevo Mensaje enviado")
        return "Email enviado satisfactoriamente"

@app.route("/activarUsuario", methods=["GET", "POST"])
def activarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        
        respuesta =controller.activarUsuario(codigo)
        if len(respuesta)==0:
            mensaje="El código de activacion es incorrevto verfique"
        else:
            mensaje="El usuario se ha registrado satisfactoriamente" 

        return render_template("informacion.html",datas=mensaje)
   