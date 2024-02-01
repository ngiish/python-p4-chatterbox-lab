from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_json = [{'id': messages.id, 'body': messages.body, 'username': messages.username, 'created_at': messages.created_at.isoformat(), 'updated_at': messages.updated_at.isoformat()}
                     for messages in messages]
    return jsonify(messages_json)

@app.route('/messages/<int:id>')
def messages_by_id(id):
    with app.app_context():
        session = Session(bind=db.engine)
        message = session.query(Message).get_or_404(id)

    # Your existing code for this route
    return jsonify({
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.isoformat(),
        'updated_at': message.updated_at.isoformat()
    })

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'id': new_message.id, 'body': new_message.body, 'username': new_message.username,
                    'created_at': new_message.created_at.isoformat(), 'updated_at': new_message.updated_at.isoformat()})

# Route to update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.json
    message.body = data['body']
    db.session.commit()
    return jsonify({'id': message.id, 'body': message.body, 'username': message.username,
                    'created_at': message.created_at.isoformat(), 'updated_at': message.updated_at.isoformat()})

# Route to delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'})


if __name__ == '__main__':
    app.run(port=5555)
