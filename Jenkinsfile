pipeline {
    agent any

    environment {
        NVD_API_KEY = credentials('c1760fd3-490f-43a0-ae8d-825ff412a81d')
    }

    tools {
        // Matches the name of the tool installation you configured in Jenkins under "Dependency-Check"
        'org.jenkinsci.plugins.DependencyCheck.tools.DependencyCheckInstallation' 'Default'
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
                node {
                    archiveArtifacts artifacts: '**/dependency-check-report/**', fingerprint: true
                }
            }
        }
    }
}
