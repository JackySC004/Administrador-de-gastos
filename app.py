from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='Sexogay'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40))
    password=db.Column(db.String(30))

class Gastos(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60))
    price=db.Column(db.Float)


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
            return redirect('/vista_gastos')
    return render_template('login.html')


@app.route('/vista_gastos', methods=['GET','POST'])
def vista_gastos():
    if request.method == 'POST':
        name=request.form['name']
        price=request.form['price']
        new_purchase=Gastos(name=name, price=price)
        print(f" Compra: {new_purchase.name} - Precio: {new_purchase.price}")
        db.session.add(new_purchase)
        db.session.commit()
    return render_template('vista_gastos.html')

@app.route('/total_gastos', methods=['GET', 'POST'])
def total_gastos():
    total_gastos=Gastos.query.all()
    suma=sum([compra.price for compra in total_gastos])
    

    return render_template ('total_gastos.html', total_gastos=total_gastos,suma=suma)



if __name__ == "__main__":
    app.run(debug=True)