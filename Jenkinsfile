pipeline {
  agent {
      docker { image 'docker:dind' }
  }
  stages {
    stage('build image') {
      steps {
        sh 'docker --version'
      }
    }
  }
}