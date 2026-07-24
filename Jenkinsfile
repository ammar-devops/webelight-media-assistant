pipeline {
    agent any

    environment {
        PROJECT_NAME = "ai-media-assistant"
        COMPOSE_FILE = "docker-compose.yml"
    }

    options {
        timestamps()
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout Source') {
            steps {
                echo "Checking out source..."
                checkout scm
            }
        }

        stage('Project Info') {
            steps {
                sh '''
                echo "========================================"
                echo "AI Media Assistant Deployment"
                echo "Workspace: $WORKSPACE"
                pwd
                ls -la
                echo "========================================"
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
                docker compose -p ${PROJECT_NAME} \
                -f ${COMPOSE_FILE} build --no-cache
                '''
            }
        }

        stage('Stop Previous Containers') {
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

                for i in {1..30}
                do
                    if curl -fs http://localhost:8000/ > /dev/null; then
                        echo "Backend is UP"
                        exit 0
                    fi

                    echo "Waiting..."
                    sleep 5
                done

                echo "Backend failed."

                docker compose -p ${PROJECT_NAME} \
                -f ${COMPOSE_FILE} logs backend

                exit 1
                '''
            }
        }

        stage('Frontend Check') {
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

            echo 'Deployment Successful.'

            sh '''
            echo "===================================="

            echo "Backend:"
            echo "http://$(curl -s ifconfig.me):8000"

            echo ""

            echo "Swagger:"
            echo "http://$(curl -s ifconfig.me):8000/docs"

            echo ""

            echo "Frontend:"
            echo "http://$(curl -s ifconfig.me):3000"

            echo "===================================="
            '''
        }

        failure {

            echo 'Deployment Failed.'

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