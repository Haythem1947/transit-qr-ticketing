pipeline {
  agent any

  triggers {
    pollSCM('H/2 * * * *')
  }

  environment {
    DOCKERHUB_USER = 'boodaci'
    IMAGE_TAG      = "1.0.${BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Test') {
      steps {
        sh '''
          for svc in ticket-service validation-service; do
            python3 -m venv /tmp/venv-$svc
            /tmp/venv-$svc/bin/pip install -q -r services/$svc/requirements.txt -r services/$svc/requirements-dev.txt
            cd services/$svc
            /tmp/venv-$svc/bin/python -m pytest -v || exit 1
            cd ../..
          done
        '''
      }
    }
  }
}