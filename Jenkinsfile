pipeline {
    agent any

    environment {
        DEPENDENCY_CHECK = tool name: 'Default', type: 'org.jenkinsci.plugins.DependencyCheck.tools.DependencyCheckInstallation'
        PYTHON = 'python3'
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
                    ${PYTHON} -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Security Scan - OWASP Dependency Check') {
            steps {
                withCredentials([string(credentialsId: 'c1760fd3-490f-43a0-ae8d-825ff412a81d', variable: 'NVD_API_KEY')]) {
                    dependencyCheck additionalArguments: """
                        --nvdApiKey ${NVD_API_KEY}
                        --format HTML
                        --out dependency-check-report
                        --scan .
                    """, odcInstallation: 'Default'
                }
            }
        }
    }

    post {
        always {
            script {
                node {
                    echo 'Archiving Dependency-Check report...'
                    archiveArtifacts artifacts: 'dependency-check-report/**', fingerprint: true
                }
            }
        }
    }
}
