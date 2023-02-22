from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cpf = db.Column(db.String(50))
    cars = db.relationship('Car', backref='owner', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50))
    model = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Car {}>'.format(self.model)

# User Routes

#Pronto
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        output.append({'id': user.id, 'name': user.name, 'cpf': user.cpf})
    return jsonify(output)

#Pronto
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    return jsonify({'id': user.id, 'name': user.name, 'cpf': user.cpf})

#Pronto
@app.route('/users', methods=['POST'])
def create_user():
    name = request.json["name"]
    cpf = request.json["cpf"]
    user = User(name=name, cpf=cpf)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'cpf': user.cpf})

#Pronto
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    user.name = request.json.get('name', user.name)
    user.cpf = request.json.get('cpf', user.cpf)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'cpf': user.cpf})

#Pronto
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

# Create Cars

#Pronto
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    output = []
    for car in cars:
        output.append({'id': car.id, 'color': car.color, 'model': car.model})
    return jsonify(output)

#Pronto
@app.route('/users/cars/<int:user_id>', methods=['GET'])
def get_user_cars(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    if user:
        if len(user.cars) == 0:
            return {'message': "Welcome! You haven't added any cars yet. If you don't have one, we have great offers to buy your own car now or if you already have one, you can register it on our platform!"}, 200
        else:
            cars = user.cars
            output = []
            for car in cars:
                output.append({'id': car.id, 'color': car.color, 'model': car.model})
            return jsonify({'id': user.id, 'name': user.name, 'cpf': user.cpf, "Cars":output})
    else:
        return {'message': 'User not found.'}, 404


#Pronto
@app.route('/users/cars/<int:user_id>', methods=['POST'])
def create_car(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'})
    if len(user.cars) < 3:  
        colorList = ['yellow', 'blue', 'gray']
        modelList = ['hatch','sedan','convertible']
        colors = request.json['color']
        models = request.json['model']
        if colors  in colorList and models in modelList :
            color = request.json['color']
            model = request.json['model']
            cars = Car(color=color, model=model, user_id=user_id)
            db.session.add(cars)
            db.session.commit()
            return jsonify({'id': cars.id, 'color': cars.color, 'model': cars.model})
        else:
            return {'message': 'Invalid cars color or model. Allowed types: ' + ', '.join(colorList) + ' or ' + ', '.join(modelList)}, 400
    else:
        return {'message': 'User has reached the maximum number of cars.'}, 400

        
#Pronto
@app.route('/users/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({'message': 'Car not found'})
    car.color = request.json.get('color', car.color)
    car.model = request.json.get('model', car.model)
    db.session.commit()
    return jsonify({'id': car.id, 'color': car.color, 'model': car.model})


@app.route('/users/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({'message': 'Car not found'})
    
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': 'Car deleted'})

@app.before_first_request
def create_tables():
    db.create_all()  
  
if __name__=="__main__":
    app.run()
        
