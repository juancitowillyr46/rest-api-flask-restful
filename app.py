from flask import Flask, jsonify
from flask_restful import reqparse, Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

api = Api(app, prefix='/api/')

parser = reqparse.RequestParser()
parser.add_argument('firstname')
parser.add_argument('lastname')
parser.add_argument('email')

class UsersList(Resource):
    def get(self):
        all_users = User.query.all()
        return users_schema.dump(all_users)
    
    def post(self):
        args = parser.parse_args()
        create = User(firstname=args['firstname'], lastname=args['lastname'], email=args['email'])
        db.session.add(create)
        db.session.commit()
        return user_schema.dump(create), 201;

class Users(Resource):
    def get(self, id):

        find = User.query.get_or_404(id)
        return user_schema.dump(find), 200;

    def put(self, id):
        args = parser.parse_args()
        find = User.query.get_or_404(id)
        find.firstname = args['firstname']
        find.lastname  = args['lastname']
        find.email     = args['email']
        db.session.commit()
        return user_schema.dump(find), 204;

    def delete(self, id):
        find = User.query.get_or_404(id)
        db.session.delete(find)
        db.session.commit()
        return user_schema.dump(find), 200;

api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<id>')

if __name__ == '__main__':
    app.run(debug=True)