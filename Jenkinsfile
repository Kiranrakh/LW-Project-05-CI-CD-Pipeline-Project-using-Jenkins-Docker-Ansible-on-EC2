pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/Kiranrakh/LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                cd app
                docker build -t flask-app .
                docker save flask-app > flask-app.tar
                '''
            }
        }

        stage('Deploy via Ansible') {
            steps {
                sh '''
                cd ansible
                ansible-playbook -i inventory deploy.yml
                '''
            }
        }
    }
}
