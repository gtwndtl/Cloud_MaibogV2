pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/gtwndtl/Cloud_MaibogV2.git'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: "${GIT_REPO}", branch: 'main'
            }
        }

        stage('Build Services') {
            steps {
                sh '''
                docker-compose -f ${COMPOSE_FILE} build \
                    user_service election_service vote_service candidate_service
                '''
            }
        }

        stage('Restart Services') {
            steps {
                sh '''
                docker-compose -f ${COMPOSE_FILE} up -d \
                    user_service user_db \
                    election_service election_db \
                    candidate_service candidate_db \
                    vote_service vote_db
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
