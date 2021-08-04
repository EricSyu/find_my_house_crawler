pipeline {
  agent any
  stages {
    stage('shell') {
      steps {
        sh 'pwd && ls'
      }
    }

    stage('docker version') {
      steps {
        sh 'docker --version'
      }
    }

  }
}