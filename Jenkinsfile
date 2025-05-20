pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                // สมมุติว่ามี Dockerfile อยู่ใน repo
                sh 'docker-compose build'
            }
        }

        stage('Deploy') {
            steps {
                // สั่งรัน docker-compose แบบ detached
                sh 'docker-compose up -d'
            }
        }
    }
}
