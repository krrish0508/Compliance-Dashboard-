pipeline {
    agent any

    environment {
        NVD_API_KEY = credentials('NVD_API_KEY') // This ID must match your Jenkins credentials
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Security Scan - OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: """
                    --nvdApiKey ${NVD_API_KEY}
                    --format HTML
                    --out dependency-check-report
                    --scan .
                """, odcInstallation: 'Default'
            }
        }
    }

    post {
        always {
            script {
                // Ensure this runs inside the workspace context
                node {
                    archiveArtifacts artifacts: 'dependency-check-report/**', fingerprint: true
                }
            }
        }
    }
}
