from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#config bd 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#modelos
db = SQLAlchemy(app)
class Esclavos(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100), nullable=False)
    matricula=db.Column(db.String(100), nullable=False)
     
with app.app_context():
    db.create_all()
@app.route('/')
def hello_world():
    return 'Hola, mundo'

@app.route('/esclavos')
def home():
    return render_template('hello.html')
@app.route('/editar')
def editarvista():
    return render_template('editar.html')


@app.route("/esclavos/guardar", methods=["POST"])
def esclavos_Guardar():
    matricula = request.form['matricula']
    nombre = request.form['nombre']
    return f"Matricula: {matricula} Nombre: {nombre}"


@app.route('/vista')
def vista_tabla():
    esclavos = Esclavos.query.all()
    return render_template('vista.html', esclavos=esclavos)


@app.route('/add', methods=["GET","POST"])
def guardar():
    if request.method=='POST':
        nombre=request.form['nombre']
        matricula=request.form['matricula']
        new_users=Esclavos (nombre=nombre, matricula=matricula)
        db.session.add(new_users)
        db.session.commit()
        message = 'Usuario agregado exitosamente!'
        return render_template('hello.html', message=message)
    return render_template('hello.html')

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    esclavo=Esclavos.query.get_or_404(id)
    try:
        db.session.delete(esclavo)
        db.session.commit()
        message='ELIMINACION EXISTOSA'
    except:
        db.session.rollback() 
        message='ERROR AL ELIMINAR REGISTRO'

    return redirect(url_for('vista_tabla'))
@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    esclavo = Esclavos.query.get_or_404(id)
    if request.method== 'POST':
        esclavo.nombre = request.form['nombre']
        esclavo.matricula = request.form['matricula']
        try:
            db.session.commit()
            return redirect(url_for('vista_tabla'))
        except:
            db.session.rollback() 
            message ='ERROR AL ACTUALIZAR REGISTRO'
            return render_template('editar.html', esclavo=esclavo, message=message)
    return render_template('editar.html', esclavo=esclavo)

if __name__ == '__main__':
    app.run(debug=True)
