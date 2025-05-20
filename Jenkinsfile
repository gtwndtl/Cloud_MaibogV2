pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/your-service-name:latest"
        REGISTRY_CREDENTIALS = 'dockerhub-credentials-id'  // ตั้งใน Jenkins Credentials
        GIT_REPO = 'https://github.com/yourusername/yourrepo.git'
    }

    stages {
        stage('Checkout') {
            steps {
                // ดึงโค้ดจาก GitHub/GitLab
                git url: "${GIT_REPO}", branch: 'main'
            }
        }

        stage('Build') {
            steps {
                echo 'Build microservice here'
                // ตัวอย่างคำสั่ง build เช่น build nodejs, python, java
                sh './build.sh' // หรือใช้คำสั่งที่เหมาะกับโปรเจคของคุณ
            }
        }

        stage('Test') {
            steps {
                echo 'Run tests here'
                sh './test.sh' // รัน unit/integration tests
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${REGISTRY_CREDENTIALS}") {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying Docker container using docker-compose'
                // ตัวอย่างใช้ docker-compose deploy บนเครื่อง Jenkins
                sh 'docker-compose down'
                sh 'docker-compose up -d --build'
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
