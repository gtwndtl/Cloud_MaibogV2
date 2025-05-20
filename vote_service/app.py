from flask import Flask, request, jsonify
from models.models import db, Vote
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@vote_db:5432/vote_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/votes', methods=['POST'])
def create_vote():
    data = request.json
    vote = Vote(
        user_id=data.get('user_id'),
        candidate_id=data.get('candidate_id'),
        election_id=data.get('election_id'),
        timestamp=datetime.utcnow()
    )
    db.session.add(vote)
    db.session.commit()
    return jsonify({'id': vote.id}), 201

@app.route('/votes', methods=['GET'])
def get_votes():
    votes = Vote.query.all()
    result = []
    for v in votes:
        result.append({
            'id': v.id,
            'user_id': v.user_id,
            'candidate_id': v.candidate_id,
            'election_id': v.election_id,
            'timestamp': v.timestamp.isoformat()
        })
    return jsonify(result)

@app.route('/votes/<int:id>', methods=['GET'])
def get_vote(id):
    v = Vote.query.get_or_404(id)
    return jsonify({
        'id': v.id,
        'user_id': v.user_id,
        'candidate_id': v.candidate_id,
        'election_id': v.election_id,
        'timestamp': v.timestamp.isoformat()
    })

@app.route('/votes/<int:id>', methods=['DELETE'])
def delete_vote(id):
    v = Vote.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    return jsonify({'message': 'Vote deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
