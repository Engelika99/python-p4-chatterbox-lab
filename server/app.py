from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_serialized = [message.to_dict() for message in messages]

    response = make_response(
        jsonify(messages_serialized),
        200
    )
    return response

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if 'body' in data and 'username' in data:
        new_message = Message(body=data['body'], username=data['username'])
        db.session.add(new_message)
        db.session.commit()

        response = make_response(
            jsonify(new_message.to_dict()),
            201
        )
        return response

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()
    message = Message.query.filter_by(id=id).first()
    
    if 'body' in data:
        message.body = data['body']
        db.session.commit()

    response = make_response(
        jsonify(message.to_dict()),
        200
    )
    return response

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.filter_by(id=id).first()
    db.session.delete(message)
    db.session.commit()

    response = make_response(
        jsonify({"message": "Message successfully deleted"}),
        200
    )
    return response



if __name__ == '__main__':
    app.run(port=5555)
