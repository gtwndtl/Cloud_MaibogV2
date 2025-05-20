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
                sh "docker-compose -f ${COMPOSE_FILE} build user_service election_service vote_service candidate_service"
            }
        }

        stage('Stop & Remove Old Services') {
            steps {
                sh """
                    docker-compose -f ${COMPOSE_FILE} stop user_service election_service vote_service candidate_service || true
                    docker-compose -f ${COMPOSE_FILE} rm -f user_service election_service vote_service candidate_service || true
                """
            }
        }

        stage('Restart Services') {
            steps {
                sh "docker-compose -f ${COMPOSE_FILE} up -d user_service election_service vote_service candidate_service"
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
