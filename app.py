from flask import Flask, render_template, request
import hashlib
import controller
from datetime import datetime
import envioemail

app = Flask(__name__)

origen=""

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/verificarUsuario", methods=["GET", "POST"])
def verificarUsuario():

    correo=request.form["txtusuario"]
    password=request.form["txtpass"]

    password2=password.encode()
    password2=hashlib.sha384(password2).hexdigest()

    respuesta =controller.consultar_usuario(correo, password2)
    global origen
    if len(respuesta)==0:
        origen=""
        mensaje ="Error de autentificación, verifique su usuario y contraseña"
        return  render_template("informacion.html", datas=mensaje)
    else:
        origen=correo
        respuesta2=controller.lista_destinatarios()
        return render_template("principal.html", listaD=respuesta2,usuario=respuesta)

    
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

        controller.registrarUsuario(name,email,password2,codigo2)
        mensaje="Sr "+name+ ",su codigo de activacion es :\n\n"+codigo2+ "\n\n Recuerde copiarlo y pegarlo para validarlo en la seccion de login y activar su cuenta.\n\nMuchas Gracias"
        envioemail.enviar(email,"Codido de Activacion",mensaje)
        
        mensajes="El Usuario "+ name+ " se ha registrado satisfactoriamnete"
        return  render_template("informacion.html", data=mensajes)
        
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

@app.route("/enviarED", methods=["GET", "POST"])
def enviarED():
   asunto=request.form["asunto"]
   mensaje=request.form["mensaje"]
   destino=request.form["destino"]
   controller.registrarMail(asunto,mensaje,origen,destino)
   envioemail.enviar(destino,"Nuevo mensaje", "Usted recibio un nuevo mensaje por favor ingrese a la plataforma")
   return "Email enviado Satisfactoriamente"

@app.route("/correosEnviados", methods=["GET", "POST"])
def correosEnviados():
    respuesta =controller.enviados(origen)
    return render_template("historial.html",listaCorreos=respuesta)
    
@app.route("/correosRecibidos", methods=["GET", "POST"])
def correosRecibidos():
    respuesta =controller.recibidos(origen)
    return render_template("historial.html",listaCorreos=respuesta)

@app.route("/updatePass", methods=["GET", "POST"])
def updatePass():
    passw=request.form["password"]
    password2=passw.encode()
    password2=hashlib.sha384(password2).hexdigest()
    controller.updatePassw(password2,origen)
    return "La contraseña se ha actualizado correctamente"