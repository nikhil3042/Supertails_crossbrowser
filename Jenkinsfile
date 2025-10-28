pipeline {
    agent any

    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'edge', 'both'],
            description: 'Select which browser(s) to run the tests on'
        )
    }

    environment {
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
        PROJECT_DIR = 'D:\\supertails_automation'
        ALLURE_RESULTS_DIR = 'D:\\supertails_automation\\reports\\allure-results'
        WORKSPACE_RESULTS = 'reports\\allure-results'
    }

    stages {
        stage('Setup') {
            steps {
                bat '''
                    echo ===== Setup: create venv & install requirements =====
                    cd /d %PROJECT_DIR%
                    python -m venv %VENV_NAME%
                    call %VENV_NAME%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (params.BROWSER == 'both') {
                        parallel (
                            "Chrome Tests": {
                                echo "Running tests on CHROME..."
                                bat """
                                    echo ===== Chrome run =====
                                    cd /d %PROJECT_DIR%
                                    call %VENV_NAME%\\Scripts\\activate
                                    if not exist "%ALLURE_RESULTS_DIR%\\chrome" mkdir "%ALLURE_RESULTS_DIR%\\chrome"
                                    pytest -m integration --browser=chrome --alluredir="%ALLURE_RESULTS_DIR%\\chrome" -q
                                """
                            },
                            "Edge Tests": {
                                echo "Running tests on EDGE..."
                                bat """
                                    echo ===== Edge run =====
                                    cd /d %PROJECT_DIR%
                                    call %VENV_NAME%\\Scripts\\activate
                                    if not exist "%ALLURE_RESULTS_DIR%\\edge" mkdir "%ALLURE_RESULTS_DIR%\\edge"
                                    pytest -m integration --browser=edge --alluredir="%ALLURE_RESULTS_DIR%\\edge" -q
                                """
                            }
                        )
                    } else {
                        echo "Running tests on ${params.BROWSER.toUpperCase()}..."
                        bat """
                            echo ===== Single-browser run: ${params.BROWSER} =====
                            cd /d %PROJECT_DIR%
                            call %VENV_NAME%\\Scripts\\activate
                            if not exist "%ALLURE_RESULTS_DIR%\\${params.BROWSER}" mkdir "%ALLURE_RESULTS_DIR%\\${params.BROWSER}"
                            pytest -m integration --browser=${params.BROWSER} --alluredir="%ALLURE_RESULTS_DIR%\\${params.BROWSER}" -q
                        """
                    }
                }
            }
        }

        stage('Generate Report') {
            steps {
                bat '''
                    echo ===== Generating merged Allure results =====
                    cd /d "%PROJECT_DIR%"

                    rem --- Remove old merged folder if exists ---
                    if exist "%ALLURE_RESULTS_DIR%\\merged" (
                        echo Removing old merged folder...
                        rmdir /s /q "%ALLURE_RESULTS_DIR%\\merged"
                    )
                    mkdir "%ALLURE_RESULTS_DIR%\\merged"

                    rem --- Copy all subfolders except merged itself ---
                    for /D %%d in ("%ALLURE_RESULTS_DIR%\\*") do (
                        if /I not "%%~nxd"=="merged" (
                            echo Copying from %%d ...
                            xcopy "%%d\\*" "%ALLURE_RESULTS_DIR%\\merged\\" /E /I /Y >nul
                        )
                    )

                    echo ===== Checking merged results folder =====
                    dir "%ALLURE_RESULTS_DIR%\\merged"

                    rem --- Copy merged folder into Jenkins workspace ---
                    echo ===== Copying merged results into Jenkins workspace =====
                    if not exist "%WORKSPACE%\\reports" mkdir "%WORKSPACE%\\reports"
                    if exist "%WORKSPACE%\\reports\\allure-results" rmdir /s /q "%WORKSPACE%\\reports\\allure-results"
                    mkdir "%WORKSPACE%\\reports\\allure-results"

                    xcopy "%ALLURE_RESULTS_DIR%\\merged\\*" "%WORKSPACE%\\reports\\allure-results\\" /E /I /Y
                    echo ===== Files copied to Jenkins workspace =====
                    dir "%WORKSPACE%\\reports\\allure-results"
                '''

                allure([
                    includeProperties: false,
                    jdk: '',
                    commandline: 'allure_2.35.0',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }

    }

    post {
        always {
            cleanWs()
        }

        success {
            echo '✅ Test execution completed successfully on selected browser(s)!'
        }

        failure {
            echo '❌ Test execution failed!'
        }
    }
}
