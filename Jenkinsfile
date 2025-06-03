pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Setting up Python virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Security Scan - OWASP Dependency Check') {
         steps {
               sh '''
                 chmod +x /home/kali/Desktop/tools/jenkins/dependency-check/bin/dependency-check.sh
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
            archiveArtifacts artifacts: 'dependency-check-report/**/*', fingerprint: true
        }
    }
}
