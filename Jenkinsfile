pipeline {
    agent any

    environment {
        PYTHON_CMD = "python3"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Kavyasshivaram/devops-app.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                dir('app') {
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'python3 -m pip install -r requirements.txt'
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                dir('app') {
                    sh 'mkdir -p reports'
                    sh 'python3 -m pytest -q --junitxml=reports/junit.xml'
                }
            }
            post {
                always {
                    junit 'app/reports/junit.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("devops-app:latest", ".")
                }
            }
        }

        stage('Push to Registry') {
            steps {
                echo "Docker push step here (configure your registry)"
            }
        }

        stage('Deploy') {
            steps {
                echo "Deployment step here (docker-compose or Kubernetes)"
            }
        }
    }
}
