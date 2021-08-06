pipeline {
  agent any
  stages {
    stage('verify docker') {
      steps {
        sh 'docker --version'
      }
    }

    stage('build image') {
      steps {
        sh 'docker build -t house-crawlers .'
      }
    }

    stage('save image to tar') {
      steps {
        sh 'docker save house-crawlers:latest | gzip > /var/jenkins_home/publish/house_crawlers_$(date \'+%Y%m%d%H%M\').tar.gz '
      }
    }

    stage('remove image') {
      steps {
        sh 'docker rmi $(docker images -q house-crawlers)'
      }
    }

  }
}