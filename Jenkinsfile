

def labels = ['master','slave'] 
def builders = [:]
for (x in labels) {
    def label = x // Need to bind the label variable before the closure 

    // Create a map to pass in to the 'parallel' step so we can fire all the builds at once
    builders[label] = {
		timestamps {
			node () {
				
				def PROJECT="/home/ubuntu/Dev/la_petite_portugaise"
				def PYTHON_P="$PROJECT/bin/python3.6"
				def GET_SECRET="/var/lib/jenkins/run_vars.py"
				
				
				stage ('Checkout') {
					// checkout scm
					sh """ 
					whoami
					uname -a
					cd $PROJECT
					sudo git fetch --all
					sudo git reset --hard origin/master
					sudo chmod -R 770 $PROJECT
					sudo chown -R ubuntu:www-data $PROJECT
					"""
				}

				stage ('Build') {
					
					sh """ 
					cd $PROJECT
					sudo service apache2 stop
					. bin/activate
					echo 'which python are you running?'
					which python
					cd src

					sudo $PYTHON_P -m pip install --upgrade pip
					echo 'pip upgrade done'
					$PYTHON_P -m pip install -r REQUIREMENTS.txt
					echo 'pip install done'
					whoami
					cd /var/lib/
					cd jenkins
					ls
					$PYTHON_P $GET_SECRET
					echo 'var import done'

					#$PYTHON_P manage.py makemigrations                  

					#$PYTHON_P manage.py migrate                  
					echo 'manage.py migrate done'

					sudo $PYTHON_P manage.py compilemessages --settings=la_petite_portugaise.settings 
					echo 'manage.py compilemessages done'

					sudo $PYTHON_P manage.py collectstatic --noinput
					echo 'manage.py collectstatic done'

					sudo $PYTHON_P manage.py check --deploy
					deactivate # quit the virtual environment

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




