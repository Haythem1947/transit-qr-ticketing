pipeline {
  agent any

  triggers {
    pollSCM('H/2 * * * *')      // checks GitHub every 2 minutes: a push to main starts a build
  }

  environment {
    DOCKERHUB_USER = 'CHANGE_ME'                  // M4: put the real Docker Hub username here
    IMAGE_TAG      = "1.0.${BUILD_NUMBER}"        // every build gets a new version number
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