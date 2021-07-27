pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
    }

  }
  stages {
    stage('tool version') {
      steps {
        sh 'docker --version'
      }
    }

  }
}