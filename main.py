from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    executor_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order")


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String)
    start_date = db.Column(db.String, nullable=True)
    end_date = db.Column(db.String, nullable=True)
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor = db.relationship(User, foreign_keys=executor_id)
    customer = db.relationship(User, foreign_keys=customer_id)


db.create_all()

with open('data/users.json') as f:
    users_json = json.load(f)
for user in users_json:
    user_object_class = User(id=user['id'], first_name=user['first_name'], last_name=user['last_name'], age=user['age'],
                             email=user['email'], role=user['role'], phone=user['phone'])
    db.session.add(user_object_class)
with open('data/offers.json') as f:
    offers_json = json.load(f)
for offer in offers_json:
    offer_object_class = Offer(id=offer['id'], order_id=offer['order_id'], executor_id=offer['executor_id'])
    db.session.add(offer_object_class)
with open('data/orders.json') as f:
    orders_json = json.load(f)
for order in orders_json:
    order_object_class = Order(id=order['id'], name=order['name'], description=order['description'],
                               start_date=datetime.strptime(order['start_date'], '%m/%d/%Y').date(),
                               end_date=datetime.strptime(order['end_date'], '%m/%d/%Y').date(),
                               address=order['address'], price=order['price'], customer_id=order['customer_id'],
                               executor_id=order['executor_id'])
    db.session.add(order_object_class)
db.session.commit()


@app.route('/')
def page_index():
    return "Урок 16"


@app.route('/users', methods=["POST", "GET"])
def get_all_users():
    all_users = db.session.query(User).all()  # нужно получить пользователь при обращении к базе
    return render_template('form.html', all_users=all_users)


@app.route('/users/<int:uid>', methods=["POST", "GET", "PUT", "DELETE"])
def get_user_by_id(uid):
    if request.method == "PUT":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        email = request.form['email']
        role = request.form['role']
        phone = request.form['phone']
        db.session.query(User).filter(User.id == uid).update([{'first_name': first_name, 'last_name': last_name, 'age' : age, 'email' : email, 'role': role, 'phone' : phone}])
        db.session.commit()
    if request.method == "DELETE":
        db.session.query(User).filter(User.id == uid).delete()
        db.session.commit()
        return render_template('form.html', all_users=db.session.query(User).all())
    user = db.session.query(User).filter(User.id == uid).all()
    return render_template('form_put.html', all_users=user, id=uid)


@app.route('/user_add', methods=["POST","GET"])
def added_user():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        email = request.form['email']
        role = request.form['role']
        phone = request.form['phone']
        user_object_class = User(first_name=first_name, last_name=last_name, age=age,
                                 email=email, role=role, phone=phone)
        db.session.add(user_object_class)
    all_users = db.session.query(User).all()
    return render_template('form.html', all_users=all_users)


@app.route('/orders')
def get_all_orders():
    all_orders = db.session.query(Order).all()
    return render_template('form_order.html', all_orders=all_orders)


@app.route('/orders/<int:uid>', methods=["POST", "GET", "PUT", "DELETE"])
def get_order_by_id(uid):
    if request.method == "PUT":
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        address = request.form['address']
        price = request.form['price']
        customer_id = request.form['customer_id']
        executor_id = request.form['executor_id']
        db.session.query(Order).filter(Order.id == uid).update([{'name': name, 'description': description,
                                                               'start_date': start_date, 'end_date': end_date, 'address': address,
                                                               'price': price, 'customer_id': customer_id, 'executor_id':executor_id}])
        db.session.commit()
    if request.method == "DELETE":
        db.session.query(Order).filter(Order.id == uid).delete()
        db.session.commit()
        return render_template('form_order.html', all_users=db.session.query(Order).all())
    order = db.session.query(Order).filter(Order.id == uid).all()
    return render_template('order_put.html', all_orders=order, id=uid)


@app.route('/order_add', methods=["POST", "GET"])
def added_order():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        address = request.form['address']
        price = request.form['price']
        customer_id = request.form['customer_id']
        executor_id = request.form['executor_id']
        order_object_class = Order(name=name, description=description, start_date=start_date, end_date=end_date,
                               address=address,
                               price=price, customer_id=customer_id, executor_id=executor_id)
        db.session.add(order_object_class)
    all_orders = db.session.query(Order).all()
    db.session.commit()
    return render_template('form_order.html', all_orders=all_orders)


@app.route('/offers')
def get_all_offers():
    all_offers = db.session.query(Offer).all()
    return render_template('form_offer.html', all_offers=all_offers)


@app.route('/offers/<int:uid>', methods=["POST", "GET", "PUT", "DELETE"])
def get_offer_by_id(uid):
    if request.method == "PUT":
        order_id = request.form['order_id']
        executor_id = request.form['executor_id']
        db.session.query(Offer).filter(Offer.id == uid).update([{'order_id': order_id, 'executor_id': executor_id,}])
        db.session.commit()
    if request.method == "DELETE":
        db.session.query(Offer).filter(Offer.id == uid).delete()
        db.session.commit()
        return render_template('form_offer.html', all_users=db.session.query(User).all())
    offer = db.session.query(Offer).filter(Offer.id == uid).all()
    return render_template('offer_put.html', all_offers=offer, id=uid)


@app.route('/offer_add', methods=["POST", "GET"])
def added_offer():
    if request.method == "POST":
        order_id = request.form['order_id']
        executor_id = request.form['executor_id']
        offer_object_class = Offer(order_id=order_id, executor_id=executor_id)
        db.session.add(offer_object_class)
        db.session.commit()
    all_offers = db.session.query(Offer).all()
    return render_template('form_offer.html', all_offers=all_offers)


app.run()
