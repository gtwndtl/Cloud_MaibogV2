from flask import Flask, request, jsonify
from models import db, User
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@user_db:5432/user_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


def create_admin_user():
    with app.app_context():
        if not User.query.filter_by(role='admin').first():
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@gmail.com',
                age=30,
                password=generate_password_hash('1234'),  # ตั้งรหัสผ่านเริ่มต้น
                role='admin',
                birthday=None,
                gender=None
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin@gmail.com / 1234")


@app.before_first_request
def initialize():
    create_admin_user()


def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({"msg": "Admins only!"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = generate_password_hash(data.get('password'))
    birthday = data.get('birthday')
    if birthday:
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=email,
        age=data.get('age'),
        password=hashed_password,
        role=data.get('role', 'user'),
        birthday=birthday,
        gender=data.get('gender')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
    })


@app.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "age": user.age,
            "role": user.role,
            "birthday": user.birthday.isoformat() if user.birthday else None,
            "gender": user.gender
        })
    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "role": user.role,
        "birthday": user.birthday.isoformat() if user.birthday else None,
        "gender": user.gender
    })


@app.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    user.role = data.get('role', user.role)
    birthday = data.get('birthday')
    if birthday:
        user.birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
    user.gender = data.get('gender', user.gender)

    # ถ้าอยากเปลี่ยนรหัสผ่าน ให้ส่ง password มา
    if data.get('password'):
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({"msg": "User updated successfully"})


@app.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"})


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(current_user_id)
    return jsonify({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "age": user.age,
        "birthday": user.birthday.isoformat() if user.birthday else None,
        "gender": user.gender
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
