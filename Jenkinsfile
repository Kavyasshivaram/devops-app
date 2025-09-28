pipeline {
    agent {
        docker {
            image 'python:3.11'   // Official Python image
            args '-v /var/jenkins_home:/var/jenkins_home' // Optional: persist workspace
        }
    }

    environment {
        PYTHON_CMD = "python"
        DOCKER_IMAGE_NAME = "devops-app:latest"
        DOCKER_REGISTRY = "https://index.docker.io/v1/"
        DOCKER_CREDENTIALS = "dockerhub-credentials-id" // Replace with your Jenkins credentials ID
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
        stage('Install Dependencies') {
            steps {
                dir('app') {
                    echo "Upgrading pip and installing requirements..."
                    sh "${env.PYTHON_CMD} -m pip install --upgrade pip"
                    sh "${env.PYTHON_CMD} -m pip install -r requirements.txt"
                }
            }
        }

        // --------------------------
        stage('Run Unit Tests') {
            steps {
                dir('app') {
                    echo "Running unit tests..."
                    sh 'mkdir -p reports'
                    sh "${env.PYTHON_CMD} -m pytest -v --capture=no --junitxml=reports/junit.xml"
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
        stage('Push to Docker Registry') {
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
