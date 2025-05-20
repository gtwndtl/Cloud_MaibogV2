pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/gtwndtl/Cloud_MaibogV2.git'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                git url: "${GIT_REPO}", branch: 'main'
            }
        }

        stage('Build') {
            steps {
                sh "docker-compose -f ${COMPOSE_FILE} build"
            }
        }

        stage('Deploy') {
            steps {
                sh "docker-compose -f ${COMPOSE_FILE} down"
                sh "docker-compose -f ${COMPOSE_FILE} up -d"
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
    }
}
