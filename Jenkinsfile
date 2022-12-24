pipeline {
    agent any

    stages {
        stage('Git Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: '14cea341-f8a8-47ef-bdef-4f1a820ee9d1', url: 'https://github.com/cmu-seai/group-project-f22-mavericks.git']]])
            }
        }
        stage('Build') {
            steps {
                echo 'Build and Setup Environment'
                git credentialsId: '14cea341-f8a8-47ef-bdef-4f1a820ee9d1', url: 'https://github.com/cmu-seai/group-project-f22-mavericks.git'
                sh '''#!/bin/bash
                python -m venv env 
                source env/bin/activate
                pip install -r requirements.txt'''
                
            }
        }
         stage('Unit Tests & Coverage') {
            steps {
                echo 'Run Unit Tests to Evaluate Infrastructure'
                sh '''#!/bin/bash
                python -m venv env 
                source env/bin/activate
                pip install -r requirements.txt
                cd recommendation-service/data_clean
                coverage run -m pytest test_data_clean.py > ../reports/unittest_report.txt
                coverage report -m  test_data_clean.py > ../reports/coverage_report.txt
                cd ..
                coverage run -m pytest online_eval/test_main.py >> reports/unittest_report.txt
                coverage report -m  online_eval/test_main.py >>  reports/coverage_report.txt
                cd offline_eval
                coverage run -m pytest main.py >> ../reports/unittest_report.txt
                coverage report -m  main.py >> ../reports/coverage_report.txt 
                '''
            }
         }
            
        stage('Offline Evaluation') {
            steps {
                echo 'Running Offline Evaluation'
                sh '''#!/bin/bash
                python -m venv env 
                source env/bin/activate
                pip install -r requirements.txt
                cd recommendation-service
                cd offline_eval
                python offline_eval.py > ../reports/offline_evaluation_report.txt
                '''
            }
        }
            
        stage('Online Evaluation') {
            steps {
                echo 'Collecting Telemetry of Latency'
                sh '''#!/bin/bash
                python -m venv env 
                source env/bin/activate
                pip install -r requirements.txt
                cd recommendation-service
                python online_eval/main.py
                '''
            }
        }
    }
}
