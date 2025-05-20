pipeline {
    agent any

    environment {
        GIT_REPO = 'https://github.com/gtwndtl/Cloud_MaibogV2.git'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: "${GIT_REPO}", branch: 'main'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying services using docker-compose'
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
