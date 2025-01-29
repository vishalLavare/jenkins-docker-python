# Jenkins Pipeline for Python Docker Deployment

This guide provides instructions on setting up a Jenkins pipeline to build a Docker image for a Python project and push it to Docker Hub.

## Prerequisites
1. **Jenkins Setup**: Ensure Jenkins is installed and running.
2. **Docker Installation**:
   - Install Docker on the Jenkins server.
   - Run `sudo usermod -aG docker jenkins` to allow Jenkins to execute Docker commands.
3. **Docker Hub Credentials**:
   - Navigate to **Dashboard** -> **Manage Jenkins** -> **Credentials** -> **Global** -> **Add Credentials**.
   - Choose **Kind** as `Username with password`.
   - Provide your **Docker Hub username** and **password**.

## Setting Up the Project
1. Create a directory for the project:
   ```bash
   mkdir python-docker-project && cd python-docker-project
   ```
2. Add the following files:
   - `Dockerfile`
   - `app.py`
   - `requirements.txt`
3. Push the project to a GitHub repository.

## Creating the Jenkins Pipeline
1. Navigate to **Dashboard** -> **New Item** -> **Pipeline**.
2. Configure the pipeline:
   - Add a name and description.
   - Under **Build Triggers**, enable **GitHub hook triggers**.
   - Generate the pipeline syntax:
     - Go to **Pipeline Syntax** -> **Checkout from Version Control**.
     - Paste the GitHub repository URL and select the branch.
     - Copy the generated script.
3. Use the following pipeline script:

```groovy
pipeline {
    agent any

    stages {
        stage('Git Clone') {
            steps {
                echo 'Clone the GitHub repository'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/vishalLavare/jenkins-docker-python.git']])
            }
        }
        stage('Build') {
            steps {
                echo 'Build Docker image'
                sh '''
                    sudo docker build -t pythonimg .
                    sudo docker images
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Run and test the Docker container'
                sh '''
                    sudo docker ps -a | grep pythoncont && sudo docker stop pythoncont && sudo docker rm pythoncont || echo "No existing container to remove"
                    sudo docker run -d -p 5000:5000 --name pythoncont pythonimg
                    sudo docker ps
                '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Push Docker image to Docker Hub'
                sh '''
                    sudo docker login -u vishallavare -p (provide Docker Personal Access Token)
                    sudo docker tag pythonimg vishallavare/pythonimg
                    sudo docker push vishallavare/pythonimg
                '''
            }
        }
    }
}
```

## Key Notes
- Replace `vishallavare` with your Docker Hub username.
- Ensure the repository `jenkins-docker-python` exists on GitHub.
- Update the credentials in Jenkins for secure authentication.

## Author
[Vishal Lavare](https://github.com/vishalLavare)

