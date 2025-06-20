pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    python -m venv ${VENV_NAME}
                    . ${VENV_NAME}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . ${VENV_NAME}/bin/activate
                    pytest --alluredir=reports/allure-results
                '''
            }
        }
        
        stage('Generate Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        
        success {
            echo 'Test execution completed successfully!'
        }
        
        failure {
            echo 'Test execution failed!'
        }
    }
} 