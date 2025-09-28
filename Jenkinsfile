environment {
    PYTHON_CMD = "python"
}
...
stage('Install Dependencies') {
    steps {
        dir('app') {
            sh "${env.PYTHON_CMD} -m pip install --upgrade pip"
            sh "${env.PYTHON_CMD} -m pip install -r requirements.txt"
        }
    }
}
...
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
