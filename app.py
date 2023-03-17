from flask import Flask, render_template, request
# from flask_sqlalchemy import (SQLAlchemy, table)
from sqlalchemy import (Table, text, inspect,Column, Integer, String, PrimaryKeyConstraint,ForeignKey, MetaData, create_engine)
from sqlalchemy.sql import select
from flask_bootstrap import Bootstrap
import unicodedata
from  separar_string import separar_cadena
from codigos_de_iconos import (LIBRO,COMILLAS_DOBLES,BOOKMARK,CONFIGURACION,HOME,LUPA,MENU_HAMBURGUESA,LIKE,FAVORITO)

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Generar la conexión
db = create_engine('sqlite:///database/biblia_con_comentario.db')
con = db.connect()
metadata = MetaData()

# Función para eliminar las tildes y ponerlo en Mayúsculas
def Format(libro):
    sin_tildes = unicodedata.normalize('NFD', libro).encode('ascii', 'ignore').decode('utf-8')
    return sin_tildes.upper()

# Función para verificar las tablas
def tabla_existe(nombre_tabla):
    inspector = inspect(db)
    if inspector.has_table(nombre_tabla):
        with db.connect() as conexion:
            consulta = text("SELECT name FROM sqlite_master WHERE type='table' AND name=:nombre_tabla")        
            resultado = conexion.execute(consulta, {"nombre_tabla": nombre_tabla}) 
            try:
                filas = resultado.fetchall()
                print("Resultado de la consulta:", filas)
                if filas != []:
                    return True
                else:
                    return False
            except:
                return False
    else:
        return False


def leer_versiculo(libro, capitulo, versiculo):   
    tabla_nombre = Format(libro)
    if tabla_existe(tabla_nombre):         
        tabla = Table(tabla_nombre, metadata, autoload_with=db, schema=None)

        # Crea la consulta
        s = select(tabla.columns.texto).where(
            (tabla.columns.capitulo == capitulo) & (tabla.columns.versiculo == versiculo)
        )

        # Ejecuta la consulta
        result = con.execute(s).fetchone()

        # Retorna el resultado
        if result is not None:
            return result[0]
        else:
            return None    
    else:
        return "Escribe bien la referencia"
    

def leer_comentario(libro, capitulo, versiculo):    
    tabla_nombre = Format(libro)
    if tabla_existe(tabla_nombre):         
        tabla = Table(Format(libro), metadata, autoload_with=db, schema=None)

        # Crea la consulta
        s = select(tabla.columns.comentario).where(
            (tabla.columns.capitulo == capitulo) & (tabla.columns.versiculo == versiculo)
        )

        # Ejecuta la consulta
        result = con.execute(s).fetchone()

        # Retorna el resultado
        if result is not None:
            return result[0]
        else:
            return None            
    else:
        return "Escribe bien la referencia"




@app.route('/', methods=['GET', 'POST'])
def verTexto():
    if request.method == 'POST':
        if 'inputBusqueda' in request.form:
            txtBusqueda = str(request.form['inputBusqueda'])        
            libro, capitulo, versiculo = separar_cadena(txtBusqueda)
            vTexto = leer_versiculo(libro, capitulo, versiculo)
            vComentario = leer_comentario(libro, capitulo, versiculo)
            vLibCapVer = txtBusqueda
            return render_template('index.html', tex=vTexto, coment=vComentario, LCV=vLibCapVer, LIBRO=LIBRO, COMILLAS_DOBLES=COMILLAS_DOBLES, BOOKMARK=BOOKMARK, CONFIGURACION=CONFIGURACION, HOME=HOME, LUPA=LUPA, MENU_HAMBURGUESA=MENU_HAMBURGUESA, LIKE=LIKE, FAVORITO=FAVORITO)
    # Si no se recibió un POST o el input estaba vacío, se renderiza la página con un valor por defecto
    return render_template('index.html', inputBusqueda='', tex='', coment='', LCV='', LIBRO=LIBRO, COMILLAS_DOBLES=COMILLAS_DOBLES, BOOKMARK=BOOKMARK, CONFIGURACION=CONFIGURACION, HOME=HOME, LUPA=LUPA, MENU_HAMBURGUESA=MENU_HAMBURGUESA, LIKE=LIKE, FAVORITO=FAVORITO)




# def verTetxo():
#     # Imprimo el texto
#     if request.method == 'POST':
#         # libro = request.form['libro']
#         # capitulo = int(request.form['capitulo'])
#         # versiculo = int(request.form['versiculo'])        

#         # vTexto = leer_versiculo(libro, capitulo, versiculo)
#         # vComentario = leer_comentario(libro, capitulo, versiculo)
#         # vLibCapVer = libro + " " + str(capitulo) + " : "+ str(versiculo)
#         # return render_template('index.html', tex=vTexto, coment=vComentario, lib=libro, cap=capitulo, ver=versiculo,LCV=vLibCapVer)
        
        
#         txtBusqueda = str(request.form['inputBusqueda'])      
        
#         print(txtBusqueda)

#         libro, capitulo, versiculo =separar_cadena(txtBusqueda)
#         vTexto = leer_versiculo(libro, capitulo, versiculo)
#         vComentario = leer_comentario(libro, capitulo, versiculo)
#         vLibCapVer = txtBusqueda
#         return render_template('index.html', tex=vTexto, coment=vComentario, LCV=vLibCapVer)      
#         # vLibCapVer = libro + " " + str(capitulo) + " : "+ str(versiculo)
#         # return render_template('index.html', tex=vTexto, coment=vComentario, lib=libro, cap=capitulo, ver=versiculo,LCV=vLibCapVer)              
#     else:
#         return render_template('index.html', inputBusqueda=request.args.get('inputBusqueda', default=''))   
#         # return render_template('index.html', libro=request.args.get('libro', default='GENESIS'), capitulo=request.args.get('capitulo', default=1), versiculo=request.args.get('versiculo', default=1))   

   



if __name__ == '__main__':
    app.run(debug=True)