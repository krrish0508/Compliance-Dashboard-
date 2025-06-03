pipeline {
    agent any

    environment {
        // This loads the secret text credential from Jenkins
        NVD_API_KEY = credentials('NVD_API_KEY') // <- ensure this ID exists in Jenkins
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
            // Ensures artifact archiving runs within the node context
            archiveArtifacts artifacts: 'dependency-check-report/**', fingerprint: true
        }
    }
}
