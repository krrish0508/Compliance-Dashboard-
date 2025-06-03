pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Ingestion') {
            steps {
                sh 'python ingestion/ingest.py'
            }
        }

        stage('Run Scoring') {
            steps {
                sh 'python scoring/score.py'
            }
        }

        stage('Generate Dashboard') {
            steps {
                sh 'python dashboard/render.py'
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: '**/dashboard/output.html', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
