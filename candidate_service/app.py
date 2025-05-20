from flask import Flask, request, jsonify
from models.models import db, Candidate
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@candidate_db:5432/candidate_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/candidates', methods=['POST'])
def create_candidate():
    data = request.json
    candidate = Candidate(
        name=data.get('name'),
        election_id=data.get('election_id')
    )
    db.session.add(candidate)
    db.session.commit()
    return jsonify({'id': candidate.id}), 201

@app.route('/candidates', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    result = []
    for c in candidates:
        result.append({
            'id': c.id,
            'name': c.name,
            'election_id': c.election_id
        })
    return jsonify(result)

@app.route('/candidates/<int:id>', methods=['GET'])
def get_candidate(id):
    c = Candidate.query.get_or_404(id)
    return jsonify({
        'id': c.id,
        'name': c.name,
        'election_id': c.election_id
    })

@app.route('/candidates/<int:id>', methods=['PUT'])
def update_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    data = request.json
    candidate.name = data.get('name', candidate.name)
    candidate.election_id = data.get('election_id', candidate.election_id)
    db.session.commit()
    return jsonify({'message': 'Candidate updated'})

@app.route('/candidates/<int:id>', methods=['DELETE'])
def delete_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    db.session.delete(candidate)
    db.session.commit()
    return jsonify({'message': 'Candidate deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
