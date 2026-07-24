pipeline {
    agent any

    environment {
        PROJECT_NAME = "ai-media-assistant"
        COMPOSE_FILE = "docker-compose.yml"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                sh '''
                    echo "========================================"
                    echo "AI Media Assistant Deployment"
                    echo "========================================"

                    pwd
                    ls -la

                    echo ""
                    echo "Docker Version"
                    docker --version

                    echo ""
                    echo "Docker Compose Version"
                    docker compose version

                    echo ""
                    echo "Running Containers"
                    docker ps
                '''
            }
        }

        stage('Validate Docker Compose') {
            steps {
                sh '''
                    docker compose -f ${COMPOSE_FILE} config
                '''
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                    docker compose \
                        -p ${PROJECT_NAME} \
                        -f ${COMPOSE_FILE} \
                        build --pull
                '''
            }
        }

        stage('Stop Previous Deployment') {
            steps {
                sh '''
                    docker compose \
                        -p ${PROJECT_NAME} \
                        -f ${COMPOSE_FILE} \
                        down --remove-orphans || true
                '''
            }
        }

        stage('Start Deployment') {
            steps {
                sh '''
                    docker compose \
                        -p ${PROJECT_NAME} \
                        -f ${COMPOSE_FILE} \
                        up -d
                '''
            }
        }

        stage('Backend Health Check') {
            steps {
                sh '''
                    echo "Waiting for Backend..."

                    for i in $(seq 1 30)
                    do
                        if curl -fs http://localhost:8000/ > /dev/null
                        then
                            echo "Backend Started Successfully."
                            exit 0
                        fi

                        echo "Attempt $i/30"
                        sleep 5
                    done

                    echo ""
                    echo "Backend Failed"

                    docker compose \
                        -p ${PROJECT_NAME} \
                        -f ${COMPOSE_FILE} \
                        logs backend

                    exit 1
                '''
            }
        }

        stage('Frontend Health Check') {
            steps {
                sh '''
                    curl -fs http://localhost:3000 > /dev/null
                    echo "Frontend Started Successfully."
                '''
            }
        }

        stage('Running Containers') {
            steps {
                sh '''
                    echo ""
                    docker ps
                '''
            }
        }
    }

    post {

        success {

            sh '''
                PUBLIC_IP=$(curl -s ifconfig.me)

                echo ""
                echo "=============================================="
                echo "Deployment Successful"
                echo "=============================================="
                echo "Frontend : http://$PUBLIC_IP:3000"
                echo "Backend  : http://$PUBLIC_IP:8000"
                echo "Swagger  : http://$PUBLIC_IP:8000/docs"
                echo "=============================================="
            '''
        }

        failure {

            sh '''
                echo ""
                echo "Deployment Failed"

                docker compose \
                    -p ${PROJECT_NAME} \
                    -f ${COMPOSE_FILE} \
                    logs
            '''
        }

        always {

            sh '''
                echo ""
                echo "Cleaning Unused Docker Images..."

                docker image prune -f || true
            '''
        }
    }
}