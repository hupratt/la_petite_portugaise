// labels need to be set on the node label property as well as on the "manage Jenkins" section of the settings
// to test: see if one label triggers a job on all the web servers tagged with the label
// See how it impacts the visual pipline plug in as well

def labels = ['master', 'slave', 'loadbalancer'] 
def builders = [:]
    
for (x in labels) {
        
    def label = x
    
    builders[label] = {
            
		timestamps {
                
			node () {
				
				def NAME="la_petite_portugaise"
				def PROJECT="/home/ubuntu/Dev/${NAME}"
				def SETTINGS="${PROJECT}/src/${NAME}/settings.py"
				def MEDIA_ROOT="${PROJECT}/media"
				def STATIC_ROOT="${PROJECT}/static"
				def SETTINGS_COMMAND="--settings=${NAME}.settings"
				def APACHE_CONF="${PROJECT}/${NAME}.conf"
				def APACHE_CONF_LB="${PROJECT}/${NAME}.loadbalancer.conf"
				def APACHE_CONF_TARGET="/etc/apache2/sites-available/${NAME}.conf"
				def MANAGE="${PROJECT}/src/manage.py"
				def REQUIREMENTS="${PROJECT}/src/REQUIREMENTS.txt"
				
				stage ('Checkout') {

					// change permissions, checkout scm and stop the web server
					// files should only be read and write to the owner, and the group can only read the files
					// directories have read, write and execute permissions to the owner, and the group can read + execute
					// static files have read, write and execute permissions to the owner, and the group can read + write
					// make sure permissions are set correctly before cd ing and fetching the origin
					sh """ 
					whoami
					uname -a
					sudo find ${PROJECT} -type f -exec chmod 640 {} +
					sudo find ${PROJECT} -type d -exec chmod 750 {} +
					sudo chmod 760 ${MEDIA_ROOT}
					sudo chmod 760 ${STATIC_ROOT}
					cd ${PROJECT}
					sudo git fetch --all
					sudo git reset --hard origin/master
					sudo service apache2 stop
					"""

				}
                
				stage ('Dependencies') {

					// upgrade pip and grab dependencies specified in the requirements file

					if (label != 'loadbalancer') {
					sh """ 
					cd ${PROJECT}
					source bin/activate
					echo 'which python are you running?'
					which python
					python -m pip install --upgrade pip
					echo 'pip upgrade done'
					python -m pip install -r ${REQUIREMENTS}
					echo 'pip install done'
					""" 
					} else {
					}
				}
                
				stage ('SQL') {

					// run the sql migrations scripts to replicate our local database settings to the production one

					if (label != 'loadbalancer') {
					sh """ 
					cd ${PROJECT}
					. bin/activate
					echo 'which python are you running?'
					which python
					python ${MANAGE} makemigrations                  
					python ${MANAGE} migrate                  
					echo 'manage.py migrate done'
					""" 
					} else {
					}
				}
                
				stage ('Translations') {

					// grab latest translations of our resources

					if (label != 'loadbalancer') {
					sh """ 
					cd ${PROJECT}
					. bin/activate
					echo 'which python are you running?'
					which python
					python ${MANAGE} compilemessages ${SETTINGS_COMMAND}
					echo 'manage.py compilemessages done'
					""" 
					} else {
					}
				}
                
				stage ('Assets') {

					// store the app static files into the main static root directory that apache manages

					if (label != 'loadbalancer') {
					sh """ 
					cd ${PROJECT}
					. bin/activate
					echo 'which python are you running?'
					which python
					python ${MANAGE} collectstatic --noinput
					echo 'manage.py collectstatic done'
					""" 
					} else {
					}
				}
                
				stage ('Security') {

					// run the security report

					if (label != 'loadbalancer') {
					sh """ 
					cd ${PROJECT}
					. bin/activate
					echo 'which python are you running?'
					which python
					python ${MANAGE} check --deploy
					""" 
					} else {
					}
				}
                
				stage ('Test') {

					// Run test coverage report

					if (label != 'loadbalancer') {
					sh """ 
					cd ${PROJECT}
					. bin/activate
					python ${MANAGE} test
					""" 
					} else {
					}
				}
                
				stage ('Apache') {

					// Overwrite conf files, check the new config and restart the web server

					if (label != 'loadbalancer') {
					sh """ 
					sudo mv ${APACHE_CONF} ${APACHE_CONF_TARGET}
					sudo apachectl configtest
					sudo service apache2 start
					""" 
					} else {
					sh """ 
					sudo mv ${APACHE_CONF_LB} ${APACHE_CONF_TARGET}
					sudo apachectl configtest
					sudo service apache2 start
					""" 
					}
					
				}
                
			}
                
		}
                
	}

} 

throttle(['loadbalancer']) {
  parallel builders
}


