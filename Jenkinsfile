pipeline {
  agent any
  options { timestamps() }
  environment {
    WEBEX_BOT_TOKEN = credentials('webex-bot-token')
    WEBEX_ROOM_ID   = credentials('webex-room-id')
  }
  triggers { githubPush() }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python') {
      steps {
        sh '''
          set -eux
          python3 -m venv .venv || python -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Unit Tests') {
      steps {
        sh '. .venv/bin/activate && python -m pytest -q --maxfail=1 --disable-warnings'
      }
    }
  }

  post {
    success {
      sh '. .venv/bin/activate && python ci/notify_webex.py --status success --build-url "$BUILD_URL" --tests "All tests passed" || true'
    }
    failure {
      sh '. .venv/bin/activate || true; python ci/notify_webex.py --status failure --build-url "$BUILD_URL" --error "Build failed. See Jenkins console for details." || true'
    }
  }
}
