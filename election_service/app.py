from flask import Flask, request, jsonify
from models import db, Election
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
    data = request.json
    election = Election(
        title=data.get('title'),
        description=data.get('description'),
        start_time=datetime.fromisoformat(data.get('start_time')),
        end_time=datetime.fromisoformat(data.get('end_time')),
        status=data.get('status')
    )
    db.session.add(election)
    db.session.commit()
    return jsonify({'id': election.id}), 201

@app.route('/elections', methods=['GET'])
def get_elections():
    elections = Election.query.all()
    result = []
    for e in elections:
        result.append({
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'start_time': e.start_time.isoformat(),
            'end_time': e.end_time.isoformat(),
            'status': e.status
        })
    return jsonify(result)

@app.route('/elections/<int:id>', methods=['GET'])
def get_election(id):
    e = Election.query.get_or_404(id)
    return jsonify({
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'start_time': e.start_time.isoformat(),
        'end_time': e.end_time.isoformat(),
        'status': e.status
    })

@app.route('/elections/<int:id>', methods=['PUT'])
def update_election(id):
    election = Election.query.get_or_404(id)
    data = request.json
    election.title = data.get('title', election.title)
    election.description = data.get('description', election.description)
    if 'start_time' in data:
        election.start_time = datetime.fromisoformat(data['start_time'])
    if 'end_time' in data:
        election.end_time = datetime.fromisoformat(data['end_time'])
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
