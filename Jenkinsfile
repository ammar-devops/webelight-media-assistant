pipeline {
    agent any

    environment {
        PROJECT_NAME = "ai-media-assistant"
        COMPOSE_FILE = "docker-compose.yml"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Project Information') {
            steps {
                sh '''
                echo "========================================="
                echo "AI Media Assistant Deployment"
                echo "Workspace : $WORKSPACE"
                echo "========================================="
                pwd
                ls -la
                '''
            }
        }

        stage('Verify Docker') {
            steps {
                sh '''
                docker --version
                docker compose version
                '''
            }
        }

        stage('Validate Compose File') {
            steps {
                sh '''
                docker compose -f ${COMPOSE_FILE} config
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                docker compose -p ${PROJECT_NAME} \
                -f ${COMPOSE_FILE} build
                '''
            }
        }

        stage('Stop Old Containers') {
            steps {
                sh '''
                docker compose -p ${PROJECT_NAME} \
                -f ${COMPOSE_FILE} down || true
                '''
            }
        }

        stage('Start Containers') {
            steps {
                sh '''
                docker compose -p ${PROJECT_NAME} \
                -f ${COMPOSE_FILE} up -d
                '''
            }
        }

        stage('Wait For Backend') {
            steps {
                sh '''
                echo "Waiting for backend..."

                for i in $(seq 1 30)
                do
                    if curl -fs http://localhost:8000/ >/dev/null
                    then
                        echo "Backend Started Successfully."
                        exit 0
                    fi

                    echo "Attempt $i / 30"
                    sleep 5
                done

                echo "Backend failed to start."

                docker compose -p ${PROJECT_NAME} \
                -f ${COMPOSE_FILE} logs backend

                exit 1
                '''
            }
        }

        stage('Check Frontend') {
            steps {
                sh '''
                curl -I http://localhost:3000
                '''
            }
        }

        stage('Running Containers') {
            steps {
                sh '''
                docker ps
                '''
            }
        }
    }

    post {

        success {

            echo "Deployment Successful"

            sh '''
            PUBLIC_IP=$(curl -s ifconfig.me)

            echo ""
            echo "===================================="
            echo "Frontend : http://$PUBLIC_IP:3000"
            echo "Backend  : http://$PUBLIC_IP:8000"
            echo "Swagger  : http://$PUBLIC_IP:8000/docs"
            echo "===================================="
            '''
        }

        failure {

            echo "Deployment Failed"

            sh '''
            docker compose -p ${PROJECT_NAME} \
            -f ${COMPOSE_FILE} logs
            '''
        }

        always {

            sh '''
            docker image prune -f || true
            '''
        }
    }
}