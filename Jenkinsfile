pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
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
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Security Scan - OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '--scan . --format HTML --project ComplianceDashboard --noupdate', odcInstallation: 'Default'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/dependency-check-report.html', fingerprint: true
        }
    }
}
