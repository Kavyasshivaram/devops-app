pipeline {
  agent any

  environment {
    IMAGE_NAME = "localhost:5000/devops-app"
    APP_DIR = "app"
  }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Unit Tests') {
      steps {
        dir("${APP_DIR}") {
          sh 'python -m pytest -q --junitxml=reports/junit.xml || true'
        }
      }
      post { always { junit 'app/reports/junit.xml' } }
    }

    stage('Build Docker Image') {
      steps { sh "docker build -t ${IMAGE_NAME}:latest ${APP_DIR}" }
    }

    stage('SonarQube Scan') {
      steps {
        withSonarQubeEnv('sonarqube') {
          sh "sonar-scanner -Dsonar.projectBaseDir=. -Dsonar.login=${env.SONAR_TOKEN}"
        }
      }
    }

    stage('Push to Registry') {
      steps { sh "docker push ${IMAGE_NAME}:latest" }
    }

    stage('Deploy') {
      steps {
        sh """
        docker rm -f devops-app || true
        docker run -d --name devops-app -p 5000:5000 ${IMAGE_NAME}:latest
        """
      }
    }
  }
}
