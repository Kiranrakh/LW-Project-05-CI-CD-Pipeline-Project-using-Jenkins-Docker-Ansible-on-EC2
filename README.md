🚀 CI/CD Pipeline using Jenkins, Docker, and Ansible on EC2

This project automates the deployment of a Flask application using Jenkins for CI/CD, Docker for containerization, and Ansible for remote deployment to a target EC2 instance.

🔧 Prerequisites

2 EC2 Ubuntu 22.04 Instances:

Jenkins EC2 (with Docker, Jenkins, Ansible)

Target EC2 (Web server with Docker)

A valid .pem key for SSH access

💻 Step-by-Step Setup and Commands

✅ Step 1: Connect to Jenkins EC2

ssh -i ~/Downloads/LW-Project.pem ubuntu@<JENKINS_PUBLIC_IP>

✅ Step 2: Install Jenkins, Docker, Git, and Ansible

sudo apt update
sudo apt install openjdk-17-jdk -y
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update && sudo apt install jenkins -y
sudo apt install docker.io git ansible -y

sudo usermod -aG docker jenkins
sudo systemctl restart docker
sudo systemctl start jenkins

Now access Jenkins UI: http://<JENKINS_PUBLIC_IP>:8080

✅ Step 3: Install Docker on Target EC2

ssh -i ~/Downloads/LW-Project.pem ubuntu@<TARGET_PUBLIC_IP>
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

✅ Step 4: Copy .pem Key from Laptop to Jenkins EC2

scp -i ~/Downloads/LW-Project.pem ~/Downloads/LW-Project.pem ubuntu@<JENKINS_PUBLIC_IP>:~

✅ Step 5: Move and Set Permissions on Jenkins EC2

sudo mkdir -p /var/lib/jenkins/.ssh
sudo cp ~/LW-Project.pem /var/lib/jenkins/.ssh/
sudo chown jenkins:jenkins /var/lib/jenkins/.ssh/LW-Project.pem
sudo chmod 600 /var/lib/jenkins/.ssh/LW-Project.pem

✅ Step 6: Clone the GitHub Repository in Jenkins EC2

git clone https://github.com/Kiranrakh/LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2.git
cd LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2

Make sure Jenkinsfile, app/, and ansible/ directories are present in the repo.

✅ Step 7: Set Up Jenkins Credentials

Go to Jenkins UI

Navigate to: Manage Jenkins > Credentials > Global > Add Credentials

Add type: SSH Username with private key

ID: web-key, Username: ubuntu, Key: LW-Project.pem contents

✅ Step 8: Test Ansible Inventory

cd ansible
ansible -i inventory all -m ping

Accept host key manually if running for first time:

ssh -i ~/.ssh/LW-Project.pem ubuntu@<TARGET_PRIVATE_IP>

✅ Step 9: Trigger Jenkins Pipeline

Create new Pipeline Job in Jenkins UI

Use Git URL: https://github.com/Kiranrakh/LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2.git

Script Path: Jenkinsfile

Build the pipeline

✅ Jenkinsfile (Automated Commands Executed)

cd app
docker build -t flask-cicd-app .
docker save -o flask-app.tar flask-cicd-app
mv flask-app.tar ../ansible/
cd ../ansible
ansible-playbook -i inventory deploy.yml

✅ Step 10: Verify Docker Container on Target EC2

ssh -i ~/Downloads/LW-Project.pem ubuntu@<TARGET_PUBLIC_IP>
sudo docker ps

✅ Final Result

Open the app in your browser:

http://<TARGET_PUBLIC_IP>

✅ Common Fixes

chmod 600 LW-Project.pem                                 # Fix permissions
sudo docker rm -f $(docker ps -q)                        # Free up port 80
ssh ubuntu@<TARGET_PRIVATE_IP>                           # Accept SSH host key

✅ Done! 🎉

Your CI/CD Pipeline using Jenkins + Docker + Ansible is now fully functional!
