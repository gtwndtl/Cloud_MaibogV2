FROM jenkins/jenkins:lts

USER root

# ติดตั้ง Docker CLI และ Docker Compose
RUN apt-get update && \
    apt-get install -y docker.io curl && \
    curl -SL https://github.com/docker/compose/releases/download/v2.24.6/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose && \
    usermod -aG docker jenkins

# ตรวจสอบว่า docker-compose ถูกติดตั้ง
RUN docker --version && docker-compose --version

USER jenkins
