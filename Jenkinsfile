pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/krrish0508/Compliance-Dashboard-'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Main Script') {
            steps {
                sh 'python3 main.py'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'  // only if you have tests
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: '**/*.csv', fingerprint: true
            }
        }
    }
}
