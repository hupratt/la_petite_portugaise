## La petite portugaise website application 

https://www.lapetiteportugaise.eu

## Architecture

* [x] La petite portugaise (LPP) is a django web app with standard static templating running on apache as a web server.
* [x] Apache proxies requests to the standard WSGI application which invokes the LPP application itself. 
* [x] There is no decoupling of the front end. 
* [x] The continuous delivery pipeline is triggered by a git push to origin (ie. this repo).
* [x] The git push triggers a webhook where both github and jenkins are listening on in order to build the jenkins pipeline.
* [x] Specifications of the Jenkinsfile can be found above.
* [x] Any push to origin will trigger the webhook however jenkins will only build the source code located in the "master" branch.
