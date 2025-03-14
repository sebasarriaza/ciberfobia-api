#!/bin/bash

# 🛑 Stop all running Docker containers
echo "Stopping all running Docker containers..."
docker stop $(docker ps -aq)

# 🏗️ Build the Docker image
echo "Building Docker image..."
docker build -t ciberfobia-api:testing .

# 📥 Read variables from .env_variables.json file
echo "Reading environment variables..."
VARS=$(cat .env_variables.json)

# 🔧 Function to escape JSON strings for bash
escape_json() {
    echo "$1" | sed 's/"/\\"/g'
}

# 🚀 Build the docker run command with environment variables
CMD="docker run -p 8080:8080"

# 🔄 Add environment variables from JSON
for key in $(echo "$VARS" | jq -r 'keys[]'); do
    value=$(echo "$VARS" | jq -r --arg k "$key" '.[$k]')
    
    # 🔍 Handle nested JSON (specifically for GCP_SA_CREDENTIALS)
    if [[ "$key" == "GCP_SA_CREDENTIALS" ]]; then
        value=$(echo "$VARS" | jq -r --arg k "$key" '.[$k]')
        value=$(escape_json "$value")
    fi
    
    CMD="$CMD -e $key=\"$value\""
done

# 🎯 Complete the command with the image name
CMD="$CMD ciberfobia-api:testing"

# 🚀 Run the Docker container
echo "Running Docker container..."
eval "$CMD"
