pipeline {
    agent any

    environment {
        PATH = "${tool name: 'Default', type: 'org.jenkinsci.plugins.DependencyCheck.tools.DependencyCheckInstallation'}/bin:${env.PATH}"
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
                dependencyCheck odcInstallation: 'Default', additionalArguments: '''
                    --project ComplianceDashboard
                    --format HTML
                    --out dependency-check-report
                    --scan .
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dependency-check-report/**', allowEmptyArchive: true
        }
    }
}
