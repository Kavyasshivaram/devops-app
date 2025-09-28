pipeline {
    agent any

    environment {
        PYTHON_CMD = "python3"  // Python inside Docker image
        DOCKER_IMAGE_NAME = "devops-app:latest"
        DOCKER_REGISTRY = "https://index.docker.io/v1/"
        DOCKER_CREDENTIALS = "dockerhub-credentials-id" // Jenkins Docker Hub credentials ID
    }

    options {
        skipDefaultCheckout()
        ansiColor('xterm')
    }

    stages {

        // --------------------------
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
                git url: 'https://github.com/Kavyasshivaram/devops-app.git', branch: 'main'
            }
        }

        // --------------------------
        stage('Install Dependencies in Docker') {
            steps {
                dir('app') {
                    echo "Installing Python dependencies inside Docker..."
                    sh """
                    docker run --rm -v \$PWD:/app -w /app python:3.11 bash -c '
                        python -m pip install --upgrade pip &&
                        python -m pip install -r requirements.txt
                    '
                    """
                }
            }
        }

        // --------------------------
        stage('Run Unit Tests in Docker') {
            steps {
                dir('app') {
                    echo "Running unit tests inside Docker..."
                    sh 'mkdir -p reports'
                    sh """
                    docker run --rm -v \$PWD:/app -w /app python:3.11 bash -c '
                        python -m pytest -v --capture=no --junitxml=reports/junit.xml
                    '
                    """
                }
            }
            post {
                always {
                    echo "Archiving test results..."
                    junit 'app/reports/junit.xml'
                }
            }
        }

        // --------------------------
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                script {
                    docker.build("${env.DOCKER_IMAGE_NAME}", ".")
                }
            }
        }

        // --------------------------
        stage('Push Docker Image') {
            steps {
                echo "Pushing Docker image to Docker Hub..."
                script {
                    docker.withRegistry("${env.DOCKER_REGISTRY}", "${env.DOCKER_CREDENTIALS}") {
                        docker.image("${env.DOCKER_IMAGE_NAME}").push()
                    }
                }
            }
        }

        // --------------------------
        stage('Deploy') {
            steps {
                echo "Deploying application using Docker Compose..."
                dir('app') {
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! 🎉'
        }
        failure {
            echo 'Pipeline failed! ❌ Check logs for details.'
        }
        always {
            echo 'Pipeline finished. Cleaning up...'
        }
    }
}
