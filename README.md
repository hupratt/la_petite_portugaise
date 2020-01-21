# La petite portugaise web application 

https://www.lapetiteportugaise.eu

## Architecture

- La petite portugaise (LPP) is a django web app with standard static templating running on apache as a web server.
- Apache proxies requests to the standard WSGI application which invokes the LPP application itself. 
- There is no decoupling of the front end. 
- A load balancer sitting in front of the servers distributes tasks using a round robin scheduler. This setup mitigates timeouts and ensures failover as there is always a server that can handle incoming requests without having to upgrade to a more expensive tier with our cloud provider. Further improvements to the set up will include: delegating caching to the load balancer and request compression
- The continuous delivery pipeline is triggered by a git push to origin by any member that has write access to this repo.
- The git push triggers a webhook where both github and jenkins are listening on in order to build the jenkins pipeline.
- Specifications of the Jenkinsfile can be found above.
- Any push to origin will trigger both webhooks however jenkins will only build the source code located in the "master" branch.

## Features

* [x] Feature 1
* [x] Feature 2
* [x] Feature 3
