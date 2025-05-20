from flask import Flask, request, jsonify
from models.models import db, Election, Candidate
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@election_db:5432/election_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/elections', methods=['POST'])
def create_election():
    data = request.get_json()
    try:
        election = Election(
            title=data.get('title'),
            description=data.get('description'),
            start_time=datetime.fromisoformat(data.get('start_time')),
            end_time=datetime.fromisoformat(data.get('end_time')),
            status=data.get('status')
        )
    except Exception as e:
        return jsonify({'error': 'Invalid datetime format', 'message': str(e)}), 400

    db.session.add(election)
    db.session.commit()
    return jsonify({'id': election.id}), 201

@app.route('/elections', methods=['GET'])
def get_elections():
    elections = Election.query.all()
    result = []
    for e in elections:
        candidates = [{'id': c.id, 'name': c.name} for c in e.candidates]
        result.append({
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'start_time': e.start_time.isoformat(),
            'end_time': e.end_time.isoformat(),
            'status': e.status,
            'candidates': candidates
        })
    return jsonify(result)

@app.route('/elections/<int:id>', methods=['GET'])
def get_election(id):
    e = Election.query.get_or_404(id)
    candidates = [{'id': c.id, 'name': c.name} for c in e.candidates]
    return jsonify({
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'start_time': e.start_time.isoformat(),
        'end_time': e.end_time.isoformat(),
        'status': e.status,
        'candidates': candidates
    })

@app.route('/elections/<int:id>', methods=['PUT'])
def update_election(id):
    election = Election.query.get_or_404(id)
    data = request.get_json()

    election.title = data.get('title', election.title)
    election.description = data.get('description', election.description)

    if 'start_time' in data:
        try:
            election.start_time = datetime.fromisoformat(data['start_time'])
        except Exception as e:
            return jsonify({'error': 'Invalid start_time format', 'message': str(e)}), 400

    if 'end_time' in data:
        try:
            election.end_time = datetime.fromisoformat(data['end_time'])
        except Exception as e:
            return jsonify({'error': 'Invalid end_time format', 'message': str(e)}), 400

    election.status = data.get('status', election.status)

    db.session.commit()
    return jsonify({'message': 'Election updated'})

@app.route('/elections/<int:id>', methods=['DELETE'])
def delete_election(id):
    election = Election.query.get_or_404(id)
    db.session.delete(election)
    db.session.commit()
    return jsonify({'message': 'Election deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
