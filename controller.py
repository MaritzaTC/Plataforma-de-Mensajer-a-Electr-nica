import sqlite3

    
def consultar_usuario(correo, password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+correo+"'and password='"+password+"'and estado='1'"
    cursor.execute(consulta)
    result=cursor.fetchall()
    return result

def lista_destinatarios():
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where estado='1'"
    cursor.execute(consulta)
    result=cursor.fetchall()
    return result
    
def enviados(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora, u.nombreUsuario from mensajeria m, usuarios u where m.origen='"+correo+"' and m.destino=u.correo"
    cursor.execute(consulta)
    result=cursor.fetchall()
    return result

def recibidos(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora, u.nombreUsuario from mensajeria m, usuarios u where m.destino='"+correo+"' and m.origen=u.correo"
    cursor.execute(consulta)
    result=cursor.fetchall()
    return result
    
def registrarMail(asunto,mensaje,origen,destino):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,origen,destino,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def registrarUsuario(name,email, password,codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into usuarios (nombreUsuario,correo,password,estado,codigoactivacion) values ('"+name+"','"+email+"','"+password+"','0','"+codigo+"')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def updatePassw(pwd,correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set password='"+pwd+"' where correo='"+correo+"'"
    db.commit()
    return "1"
    
def activarUsuario(codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    db.commit()
    consulta2="select *from usuarios where codigoactivacion='"+codigo+"'and estado='1'"
    cursor.execute(consulta2)
    result=cursor.fetchall()
    return result
    return "1"