pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            args '-u root:root'
        }
    }

    environment {
        PYTHON_CMD = "python"
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
                    sh "${env.PYTHON_CMD} -m pip install --upgrade pip"
                    sh "${env.PYTHON_CMD} -m pip install -r requirements.txt"
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh 'mkdir -p app/reports'
                sh "export PYTHONPATH=$PWD && ${env.PYTHON_CMD} -m pytest -q --junitxml=app/reports/junit.xml"
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
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials-id') {
                        docker.image("devops-app:latest").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d'
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
    }
}
