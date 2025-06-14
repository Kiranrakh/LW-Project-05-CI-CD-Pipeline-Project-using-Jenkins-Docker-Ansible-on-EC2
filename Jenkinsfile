pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-cicd-app"
        TAR_NAME = "flask-app.tar"
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo "📥 Cloning repository..."
                git branch: 'main', url: 'https://github.com/Kiranrakh/LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                sh '''
                cd app
                docker build -t $IMAGE_NAME .
                docker save $IMAGE_NAME > $TAR_NAME
                mv $TAR_NAME ../ansible/
                '''
            }
        }

        stage('Deploy via Ansible') {
            steps {
                echo "🚀 Deploying to target EC2 with Ansible..."
                sh '''
                cd ansible
                ansible-playbook -i inventory deploy.yml
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Deployment completed successfully!"
        }
        failure {
            echo "❌ Deployment failed. Check the console output for details."
        }
    }
}
