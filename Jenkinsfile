pipeline {
  agent any
  environment {
    IMAGE_WEB = "devsolutions/web"
    IMAGE_STATUS = "devsolutions/status"
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
        script {
          COMMIT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          echo "Commit: ${COMMIT}"
        }
      }
    }

    stage('Build Images') {
      steps {
        sh "docker build -t ${IMAGE_WEB}:${COMMIT} ./app/web"
        sh "docker build -t ${IMAGE_STATUS}:${COMMIT} ./app/status"
      }
    }

    stage('Tag Latest') {
      steps {
        sh "docker tag ${IMAGE_WEB}:${COMMIT} ${IMAGE_WEB}:latest"
        sh "docker tag ${IMAGE_STATUS}:${COMMIT} ${IMAGE_STATUS}:latest"
      }
    }

    stage('Push (optional)') {
      steps {
        echo "If you have registry credentials, push images here. Skipping push to public registry in this lab."
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        // update deployment images
        sh "kubectl set image deployment/web-deployment web=${IMAGE_WEB}:${COMMIT} --record || kubectl apply -f kubernetes/web-deployment.yaml"
        sh "kubectl set image deployment/status-deployment status=${IMAGE_STATUS}:${COMMIT} --record || kubectl apply -f kubernetes/status-deployment.yaml"
      }
    }

    stage('Verify') {
      steps {
        sh "kubectl rollout status deployment/web-deployment --timeout=60s || true"
        sh "kubectl get pods -o wide"
      }
    }
  }
  post {
    always {
      sh "kubectl get pods -o wide || true"
    }
  }
}
