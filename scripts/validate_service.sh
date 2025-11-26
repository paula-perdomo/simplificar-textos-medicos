#!/bin/bash

# Wait for the application to start (max 5 minutes)
for i in {1..30}; do
    # Try to reach the health check endpoint
    # -s: Silent mode
    # -o /dev/null: Discard output
    # -w "%{http_code}": Print only the HTTP status code
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health)

    if [ "$HTTP_CODE" == "200" ]; then
        echo "Application is healthy!"
        exit 0
    fi

    echo "Waiting for application... (Attempt $i/30)"
    sleep 10
done

echo "Application failed to start within timeout."
# Print container logs to help debugging in CodeDeploy console
sudo docker logs biomedical-text-simplification
exit 1