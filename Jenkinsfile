stage('Health Check') {
    steps {
        sh '''
            echo "========================================"
            echo "Health Check"
            echo "========================================"

            echo ""
            echo "Waiting for Backend..."

            BACKEND_OK=false

            for i in $(seq 1 30); do
                if curl -fs http://localhost:8000/ >/dev/null 2>&1; then
                    echo ""
                    echo "✅ Backend Started Successfully."
                    BACKEND_OK=true
                    break
                fi

                echo "Attempt $i/30 - Backend not ready..."
                sleep 5
            done

            if [ "$BACKEND_OK" != "true" ]; then
                echo ""
                echo "❌ Backend Failed to Start!"
                docker compose -p ai-media-assistant -f docker-compose.prod.yml logs backend
                exit 1
            fi

            echo ""
            echo "Waiting for Frontend..."

            FRONTEND_OK=false

            for i in $(seq 1 30); do
                if curl -fs http://localhost:3000 >/dev/null 2>&1; then
                    echo ""
                    echo "✅ Frontend Started Successfully."
                    FRONTEND_OK=true
                    break
                fi

                echo "Attempt $i/30 - Frontend not ready..."
                sleep 5
            done

            if [ "$FRONTEND_OK" != "true" ]; then
                echo ""
                echo "❌ Frontend Failed to Start!"
                docker compose -p ai-media-assistant -f docker-compose.prod.yml logs frontend
                exit 1
            fi

            echo ""
            echo "========================================"
            echo "🎉 Deployment Successful!"
            echo "========================================"
            echo ""
            echo "Backend  : http://localhost:8000"
            echo "Frontend : http://localhost:3000"
        '''
    }
}