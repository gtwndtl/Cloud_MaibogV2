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

        stage('Cleanup Conflicting Containers') {
            steps {
                script {
                    echo "Cleaning up containers using ports 5001,5002,5003,5004 and 54321"

                    def ports = ['5001', '5002', '5003', '5004', '54321']

                    ports.each { port ->
                        def containerId = sh(script: "docker ps -aq --filter publish=${port}", returnStdout: true).trim()
                        if (containerId) {
                            echo "Stopping and removing container using port ${port}: ${containerId}"
                            sh "docker rm -f ${containerId}"
                        } else {
                            echo "No container found using port ${port}"
                        }
                    }
                }
            }
        }

        stage('Build Services') {
            steps {
                sh "docker-compose -f ${COMPOSE_FILE} build user_service election_service vote_service candidate_service"
            }
        }

        stage('Restart Services') {
            steps {
                // --force-recreate ช่วยให้ recreate container ใหม่ทุกครั้ง
                sh "docker-compose -f ${COMPOSE_FILE} up -d --force-recreate user_service election_service vote_service candidate_service"
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
