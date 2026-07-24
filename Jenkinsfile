pipeline {
    agent any

    environment {
        PROJECT_NAME = "ai-media-assistant"
        COMPOSE_FILE = "docker-compose.prod.yml"

        DOCKER_BUILDKIT = "1"
        COMPOSE_DOCKER_CLI_BUILD = "1"
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
                    echo "========================================"
                    echo "Waiting for Backend..."
                    echo "========================================"

                    BACKEND_OK=false

                    for i in $(seq 1 30)
                    do
                        if docker compose \
                            -p ${PROJECT_NAME} \
                            -f ${COMPOSE_FILE} \
                            exec -T backend \
                            curl -fs http://localhost:8000/ >/dev/null 2>&1
                        then
                            echo ""
                            echo "✅ Backend Started Successfully."
                            BACKEND_OK=true
                            break
                        fi

                        echo "Attempt $i/30..."
                        sleep 5
                    done

                    if [ "$BACKEND_OK" != "true" ]
                    then
                        echo ""
                        echo "❌ Backend Failed!"

                        docker compose \
                            -p ${PROJECT_NAME} \
                            -f ${COMPOSE_FILE} \
                            logs backend

                        exit 1
                    fi
                '''
            }
        }

        stage('Verify Frontend') {
            steps {
                sh '''
                    echo "========================================"
                    echo "Verifying Frontend..."
                    echo "========================================"

                    sleep 10

                    curl -fsI http://localhost:3000

                    echo ""
                    echo "✅ Frontend Verified Successfully."
                '''
            }
        }

        stage('Running Containers') {
            steps {
                sh '''
                    echo ""
                    echo "========================================"
                    echo "Running Containers"
                    echo "========================================"

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
                echo "🎉 Deployment Successful"
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
                echo "=============================================="
                echo "❌ Deployment Failed"
                echo "=============================================="

                docker compose \
                    -p ${PROJECT_NAME} \
                    -f ${COMPOSE_FILE} \
                    ps

                echo ""

                docker compose \
                    -p ${PROJECT_NAME} \
                    -f ${COMPOSE_FILE} \
                    logs
            '''
        }

        always {
            sh '''
                echo ""
                echo "Cleaning Docker..."

                docker image prune -f || true
                docker builder prune -f || true
            '''
        }
    }
}