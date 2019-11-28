# La petite portugaise website application 

https://www.lapetiteportugaise.eu

## Architecture

- La petite portugaise (LPP) is a django web app with standard static templating running on apache as a web server.
- Apache proxies requests to the standard WSGI application which invokes the LPP application itself. 
- There is no decoupling of the front end. 
- The continuous delivery pipeline is triggered by a git push to origin (ie. this repo).
- The git push triggers a webhook where both github and jenkins are listening on in order to build the jenkins pipeline.
- Specifications of the Jenkinsfile can be found above.
- Any push to origin will trigger the webhook however jenkins will only build the source code located in the "master" branch.


## Features

* [x] Feature 1
* [x] Feature 2
* [x] Feature 3
