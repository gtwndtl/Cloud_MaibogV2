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

        stage('Force Remove Conflicting Containers') {
            steps {
                sh '''
                    echo "Cleaning containers using ports 5001–5004 (user/election/vote/candidate services)"
                    for port in 5001 5002 5003 5004; do
                      CONTAINER_ID=$(docker ps -aq --filter "publish=$port")
                      if [ ! -z "$CONTAINER_ID" ]; then
                        echo "Stopping and removing container on port $port -> $CONTAINER_ID"
                        docker rm -f "$CONTAINER_ID"
                      fi
                    done
                '''
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
