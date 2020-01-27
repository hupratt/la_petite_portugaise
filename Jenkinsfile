// labels need to be set on the node label property as well as on the "manage Jenkins" section of the settings

// to test: see if one label triggers a job on all the web servers tagged with the label

// See how it impacts the visual pipline plug in as well

def labels = ['master','slave'] 

def builders = [:]
for (x in labels) {     
    def label = x
    builders[label] = {

        timestamps {

            node () {

                def NAME="la_petite_portugaise"
                def PROJECT="/home/ubuntu/Dev/${NAME}"
                def SETTINGS="${PROJECT}/src/${NAME}/settings.py"
                def SETTINGS_COMMAND="--settings=${NAME}.settings"
                def APACHE_CONF="${PROJECT}/${NAME}.conf"
                def APACHE_CONF_TARGET="/etc/apache2/sites-available/${NAME}.conf"
                def MANAGE="${PROJECT}/src/manage.py"
                def REQUIREMENTS="${PROJECT}/src/REQUIREMENTS.txt"
                def PYTHON_P="${PROJECT}/bin/python3.6"
                def GET_SECRET="/var/lib/jenkins/inject_vars.py"

                stage ('Checkout') {

                    // change permissions, checkout scm and stop the web server

                    sh """ 
                    whoami
                    uname -a
                    sudo chmod -R 770 ${PROJECT}
                    sudo chown -R ubuntu:www-data ${PROJECT}
                    cd ${PROJECT}
                    sudo git fetch --all
                    sudo git reset --hard origin/master
                    sudo service apache2 stop

                    """

                }

                stage ('Dependencies') {

                    // upgrade pip and grab dependencies specified in the requirements file
                    sh """ 
                    cd ${PROJECT}
                    . bin/activate
                    echo 'which python are you running?'
                    which python
                    sudo ${PYTHON_P} -m pip install --upgrade pip # Upgrade pip
                    echo 'pip upgrade done'
                    ${PYTHON_P} -m pip install -r ${REQUIREMENTS} # Install or upgrade dependencies
                    echo 'pip install done'
                    sudo ${PYTHON_P} ${GET_SECRET} -e "~/.bash_profile" -t ${SETTINGS}
                    echo 'var import done'
                    """ 

                }

                stage ('SQL') {

                    // run the sql migrations scripts to replicate our local database settings to the production database

                    sh """ 
                    cd ${PROJECT}
                    . bin/activate
                    echo 'which python are you running?'
                    which python
                    sudo ${PYTHON_P} ${MANAGE} makemigrations                  
                    sudo ${PYTHON_P} ${MANAGE} migrate                  
                    echo 'manage.py migrate done'
                    """ 
                }

                stage ('Translations') {

                    // grab latest translations of our resources
                    sh """ 
                    cd ${PROJECT}
                    . bin/activate
                    echo 'which python are you running?'
                    which python
                    sudo ${PYTHON_P} ${MANAGE} compilemessages ${SETTINGS_COMMAND}
                    echo 'manage.py compilemessages done'
                    """ 

                }

                stage ('Assets') {

                    // store the app static files into the main static root directory that apache manages

                    sh """ 
                    cd ${PROJECT}
                    . bin/activate
                    echo 'which python are you running?'
                    which python
                    sudo ${PYTHON_P} ${MANAGE} collectstatic --noinput
                    echo 'manage.py collectstatic done'
                    """ 

                }

                stage ('Security') {

                    // run the security report

                    sh """ 
                    cd ${PROJECT}
                    . bin/activate
                    echo 'which python are you running?'
                    which python
                    sudo ${PYTHON_P} ${MANAGE} check --deploy
                    """ 

                }

                

                stage ('Test') {

                    // Run test coverage report

                    sh """ 

                    """ 

                }

                stage ('Apache') {
                    // Overwrite conf files, check the new config and restart the web server

                    sh """ 
                    ${APACHE_CONF} > ${APACHE_CONF_TARGET}
                    sudo apachectl configtest
                    sudo service apache2 start
                    """ 
                }

            }

        }      

    }         

}

 

throttle(['loadbalancer']) {
  parallel builders
}


