from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import plotly.express as px
import plotly.io as pio
from io import BytesIO
import base64

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='Sexogay'
db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40))
    password=db.Column(db.String(30))
    gastos=db.relationship('Gastos',lazy='select')

class Gastos(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60))
    price=db.Column(db.Float)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    category=db.Column(db.String(200))


with app.app_context():
    db.create_all()

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        new_user=User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('registration.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        user=User.query.filter_by(name=name).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/vista_gastos')
    return render_template('login.html')


@app.route('/vista_gastos', methods=['GET','POST'])
@login_required
def vista_gastos():
    nombre=current_user.name
    if request.method == 'POST':
        name=request.form['name']
        price=request.form['price']
        category=request.form['category']
        new_purchase=Gastos(name=name, price=price, user_id=current_user.id, category=category)
        print(f" Compra: {new_purchase.name} - Precio: {new_purchase.price}")
        db.session.add(new_purchase)
        db.session.commit()
    return render_template('vista_gastos.html', nombre=nombre)

@app.route('/total_gastos', methods=['GET', 'POST'])
@login_required
def total_gastos():
    total_gastos=Gastos.query.filter_by(user_id=current_user.id)
    suma=sum([compra.price for compra in total_gastos])
    return render_template ('total_gastos.html', total_gastos=total_gastos,suma=suma)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/login')

@app.route('/grafico_pastel', methods=['POST', 'GET'])
@login_required
def grafico_pastel():
    user_purchases=Gastos.query.filter_by(user_id=current_user.id).all()
    



if __name__ == "__main__":
    app.run(debug=True)