pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('OWASP Dependency Check') {
            steps {
                sh '''
                /opt/dependency-check/bin/dependency-check.sh \
                    --project ComplianceDashboard \
                    --scan . \
                    --format HTML \
                    --out dependency-check-report
                '''
            }
        }

        stage('Build') {
            steps {
                sh 'python3 main.py'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dependency-check-report/*', fingerprint: true
        }
    }
}
