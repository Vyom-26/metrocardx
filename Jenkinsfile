pipeline {
  agent any
  environment { BUILD_TS = "" }
  stages {
    stage('Env check') {
      steps {
        script {
          def pyPath = sh(script: 'which python3 || true', returnStdout: true).trim()
          if (!pyPath) { error "python3 not found in PATH on agent. Install python3 or use an agent with python3." }
          echo "python3 found: ${pyPath}"
        }
      }
    }
    stage('Checkout') { steps { checkout scm } }
    stage('Prepare') {
      steps { script {
        BUILD_TS = sh(script: "date +%Y%m%d%H%M%S", returnStdout: true).trim()
        env.BUILD_TS = BUILD_TS
        echo "Using timestamp: ${BUILD_TS}"
      } }
    }
    stage('Build') {
      steps { sh '''
        python3 -m venv venv || true
        . venv/bin/activate
        pip install --upgrade pip || true
        pip install -r requirements.txt || true
      ''' }
    }
    stage('Test') {
      steps { sh '''
        . venv/bin/activate
        mkdir -p reports
        python3 -m unittest discover -v 2>&1 | tee reports/test-${BUILD_TS}.log
      ''' }
      post {
        always {
          sh '''
            mkdir -p /tmp/metrocardx-builds
            cp -r reports/test-${BUILD_TS}.log /tmp/metrocardx-builds/test-${BUILD_TS}.log
            ls -l /tmp/metrocardx-builds || true
          '''
          archiveArtifacts artifacts: "reports/test-${BUILD_TS}.log", fingerprint: true
        }
      }
    }
    stage('Validate') {
      steps { sh 'python3 -c "from metrocard import calculate_recharge; print(calculate_recharge(5,10,0.1))"' }
    }
    stage('Archive') {
      steps { sh '''
        mkdir -p /tmp/metrocardx-builds/${BUILD_TS}
        cp -r . /tmp/metrocardx-builds/${BUILD_TS}/ || true
        echo "Artifacts copied to /tmp/metrocardx-builds/${BUILD_TS}"
      ''' }
    }
  }
  post {
    failure { echo "Build failed. See archived logs in /tmp/metrocardx-builds" }
    success { echo "Pipeline finished successfully. Logs in /tmp/metrocardx-builds" }
  }
}
