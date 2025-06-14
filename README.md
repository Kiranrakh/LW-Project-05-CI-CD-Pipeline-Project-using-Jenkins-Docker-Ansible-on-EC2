# 🚀 CI/CD Pipeline using Jenkins, Docker, and Ansible on EC2

This project automates the deployment of a Flask application using Jenkins for CI/CD, Docker for containerization, and Ansible for deployment to a target EC2 instance.

---

## 🔧 Prerequisites

* Two EC2 Ubuntu 22.04 Instances:

  * **Jenkins EC2** (with Jenkins, Docker, Git, Ansible)
  * **Target EC2** (only Docker installed)
* Valid `.pem` key for SSH access
* GitHub Repository with:

  * `Jenkinsfile`
  * `app/` folder (Flask app with Dockerfile)
  * `ansible/` folder (inventory + deploy.yml)

---

## 📁 Project Structure

```
LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2/
├── ansible/
│   ├── deploy.yml               # Ansible playbook to deploy Docker container on target EC2
│   └── inventory                # Inventory file with target EC2 private IP
│
├── app/
│   ├── static/
│   │   └── style.css            # CSS styling for the Flask app
│   ├── templates/
│   │   └── index.html           # HTML template for rendering the Flask app
│   ├── Dockerfile               # Dockerfile to build Flask app container
│   ├── app.py                   # Main Flask application
│   └── requirements.txt         # Python dependencies for the Flask app
│
├── Jenkinsfile                 # Jenkins pipeline-as-code to automate CI/CD
├── README.md                   # Complete project documentation

```

---

## 🧩 Step-by-Step Setup & Commands

### ✅ Step 1: Connect to Jenkins EC2

```bash
ssh -i ~/Downloads/LW-Project.pem ubuntu@<JENKINS_PUBLIC_IP>
```

---

### ✅ Step 2: Install Jenkins, Docker, Git, Ansible

```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc

echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | \
sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install jenkins docker.io git ansible -y

sudo usermod -aG docker jenkins
sudo systemctl restart docker
sudo systemctl start jenkins
```

➡️ Access Jenkins UI: `http://<JENKINS_PUBLIC_IP>:8080`

---

### ✅ Step 3: Install Docker on Target EC2

```bash
ssh -i ~/Downloads/LW-Project.pem ubuntu@<TARGET_PUBLIC_IP>
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

---

### ✅ Step 4: Copy `.pem` from Laptop to Jenkins EC2

```bash
scp -i ~/Downloads/LW-Project.pem ~/Downloads/LW-Project.pem ubuntu@<JENKINS_PUBLIC_IP>:~
```

---

### ✅ Step 5: Move Key to Jenkins and Set Permissions

```bash
sudo mkdir -p /var/lib/jenkins/.ssh
sudo cp ~/LW-Project.pem /var/lib/jenkins/.ssh/
sudo chown jenkins:jenkins /var/lib/jenkins/.ssh/LW-Project.pem
sudo chmod 600 /var/lib/jenkins/.ssh/LW-Project.pem
```

---

### ✅ Step 6: Clone GitHub Repo Inside Jenkins EC2

```bash
git clone https://github.com/Kiranrakh/LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2.git
cd LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2
```

---

### ✅ Step 7: Add SSH Credential in Jenkins

1. Go to `Jenkins > Manage Jenkins > Credentials > Global > Add Credentials`
2. Type: **SSH Username with private key**
3. ID: `web-key`
4. Username: `ubuntu`
5. Paste the private key (`LW-Project.pem`) content

---

### ✅ Step 8: Test Ansible Ping from Jenkins EC2

```bash
cd ansible
ansible -i inventory all -m ping
```

✅ If first-time prompt appears:

```bash
ssh -i ~/.ssh/LW-Project.pem ubuntu@<TARGET_PRIVATE_IP>
```

Type `yes` to accept host key.

---

### ✅ Step 9: Create Pipeline Job in Jenkins

1. Go to Jenkins → `New Item`
2. Enter name: `LW-Project-05-Test`
3. Type: `Pipeline`
4. Scroll down to “Pipeline” section:

   * Definition: `Pipeline script from SCM`
   * SCM: `Git`
   * URL: `https://github.com/Kiranrakh/LW-Project-05-CI-CD-Pipeline-Project-using-Jenkins-Docker-Ansible-on-EC2.git`
   * Branch: `*/main`
   * Script Path: `Jenkinsfile`
5. Click `Save` and then `Build Now`

---

## 🛠️ Jenkinsfile Pipeline Actions (What It Does)

```bash
cd app
docker build -t flask-cicd-app .
docker save -o flask-app.tar flask-cicd-app
mv flask-app.tar ../ansible/
cd ../ansible
ansible-playbook -i inventory deploy.yml
```

---

## 📦 Ansible Playbook (`deploy.yml`) Tasks

```yaml
- Copy Docker image to remote
- Load Docker image
- Run container on port 80
```

---

## 🔍 Verify on Target EC2

```bash
ssh -i ~/Downloads/LW-Project.pem ubuntu@<TARGET_PUBLIC_IP>
sudo docker ps
```

If container is running:

```bash
curl http://localhost
```

Or open in browser:

```
http://<TARGET_PUBLIC_IP>
```

---

## 🧹 Common Fixes & Commands

```bash
chmod 600 LW-Project.pem                             # Fix SSH key permission
sudo docker rm -f $(docker ps -q)                   # Remove old container
sudo netstat -tulpn | grep :80                      # Check port 80 usage
```

---

## 🎉 Project Complete

Your Flask App is now deployed via:

* CI using **Jenkins**
* Containerization with **Docker**
* Deployment via **Ansible**
* Running on **EC2**

