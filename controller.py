import sqlite3

def consultar_usuario(usuario, password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+usuario+"'and password='"+password+"'and estado='1'"
    cursor.execute(consulta)
    result=cursor.fetchall()
    return result

def lista_destinatarios(usuario):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+usuario+"'"
    cursor.execute(consulta)
    result=cursor.fetchall()
    return result

def registrarUsuario(name,email, password,codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into usuarios (nombreUsuario,correo,password,estado,codigoactivacion) values ('"+name+"','"+email+"','"+password+"','0','"+codigo+"')"
    cursor.execute(consulta)
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