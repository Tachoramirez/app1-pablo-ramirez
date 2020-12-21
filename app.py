#Llamamos los módulos que necesitemos para la práctica
from flask import Flask, render_template, url_for, redirect, request
from flask_material import Material
from flask_sqlalchemy import SQLAlchemy
 

#Configuramos el controlador "app.py" (editable sobre la marcha)
app = Flask(__name__)
app.debug = True
Material(app)


#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:12345@localhost:5432/escolares'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://iszrqvkmozunly:0e4f521e1026349c734537cfbe1d4c4d4b5c957ee30530273741115f9fdc6912@ec2-52-22-238-188.compute-1.amazonaws.com:5432/d4161cev4q8ko6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


#Modelo de datos
class Alumnos(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(30))
	apellido = db.Column(db.String(100))

lista = ["Nosotros", "Contacto", "Preguntas frecuentes"]
#Renderizamos las vistas con sus respectivos parámetros y funciones
@app.route('/', methods=['GET','POST'])
def index():
	global lista
	if request.method == "POST":
		print("request")
		campo_nombre = request.form['nombre']
		campo_apellido = request.form['apellido']
		alumno = Alumnos(nombre=campo_nombre,apellido=campo_apellido)
		db.session.add(alumno)
		db.session.commit()
		mensaje = "Alumno registrado"
		return redirect(url_for('index'))
	return render_template("index.html", variable = lista)
	#return redirect(url_for("acerca"))

@app.route('/acerca')
def acerca():
	consulta = Alumnos.query.all()
	return render_template("acerca.html", datos = consulta)

@app.route('/eliminar/<id>')
def eliminar(id):
	reg = Alumnos.query.filter_by(id = id).delete()
	db.session.commit()
	return redirect(url_for('acerca'))

@app.route('/editar/<id>')
def editar(id):
	reg = Alumnos.query.filter_by(id = id).first()
	return render_template('editar.html', alumno = reg)

@app.route('/actualizar', methods=['GET','POST'])
def actualizar():
	if request.method == "POST":
		query = Alumnos.query.get(request.form['id'])
		query.nombre = request.form['nombreE']
		query.apellido = apellido = request.form['apellidoE']
		db.session.commit()
		return redirect(url_for('acerca'))


if __name__ == "__main__":
	app.run()




