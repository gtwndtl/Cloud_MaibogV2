pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // ระบุ branch ให้ชัดเจน
                git branch: 'main', url: 'https://github.com/gtwndtl/Cloud_MaibogV2.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker-compose down || true
                    docker-compose up -d
                '''
            }
        }
    }
}
