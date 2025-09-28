pipeline {
    agent any

    environment {
        PYTHON_CMD = "python3"
        PROJECT_ROOT = "${WORKSPACE}"
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
                sh 'mkdir -p app/reports'
                // Run pytest from project root, set PYTHONPATH
                sh 'export PYTHONPATH=$PWD && python3 -m pytest -q --junitxml=app/reports/junit.xml'
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
                    // Replace with your Docker registry info
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials-id') {
                        docker.image("devops-app:latest").push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Example: docker-compose deployment
                sh 'docker-compose down'
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
