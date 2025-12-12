pipeline {
    agent any

    environment {
        LOG_DIR = "/tmp/metrocardx-builds"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Env check') {
            steps {
                sh '''
                    echo "Checking for python3..."
                    which python3 || { echo "python3 not found"; exit 1; }
                    python3 --version
                '''
            }
        }

        stage('Prepare') {
            steps {
                sh '''
                    echo "Preparing workspace..."
                    mkdir -p reports
                    mkdir -p ${LOG_DIR}
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    TS=$(date +%Y%m%d%H%M%S)
                    echo "Build TS=$TS"

                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

                    echo "Build completed at ${TS}" | tee reports/build-${TS}.log
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    TS=$(date +%Y%m%d%H%M%S)
                    echo "Running tests (TS=${TS})"

                    . venv/bin/activate

                    # run tests and save output to a log file (POSIX friendly, avoids bash-only PIPESTATUS)
                    python3 -m unittest discover -v tests -p "test_*.py" > reports/test-${TS}.log 2>&1
                    rc=$?
                    # print the log so Jenkins console shows it
                    cat reports/test-${TS}.log || true

                    # copy to persistent host path
                    cp reports/test-${TS}.log ${LOG_DIR}/test-${TS}.log || true

                    if [ $rc -ne 0 ]; then
                        echo "Tests failed (rc=$rc)"
                        exit $rc
                    fi
                '''
            }
        }

        stage('Validate') {
            steps {
                sh '''
                    TS=$(date +%Y%m%d%H%M%S)
                    echo "Validating metrocard module..."

                    . venv/bin/activate

                    python3 -c "import metrocard; print('metrocard OK')" > reports/validate-${TS}.log 2>&1
                    cat reports/validate-${TS}.log || true

                    cp reports/validate-${TS}.log ${LOG_DIR}/validate-${TS}.log || true
                '''
            }
        }

        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: "reports/*-*.log", fingerprint: true
            }
        }
    }

    post {
        always {
            sh '''
                echo "=== Reports Directory ==="
                ls -la reports || true

                echo "=== /tmp/metrocardx-builds Directory ==="
                ls -la ${LOG_DIR} || true
            '''
            echo "Pipeline finished — check archived artifacts."
        }
    }
}
