pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Build step here'
            }
        }

        stage('Security Scan - OWASP Dependency Check') {
            steps {
                sh '''
                    /home/kali/Desktop/tools/jenkins/dependency-check/bin/dependency-check.sh \
                        --project ComplianceDashboard \
                        --format HTML \
                        --out dependency-check-report \
                        --scan .
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'dependency-check-report/*', fingerprint: true
        }
    }
}
