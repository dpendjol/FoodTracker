## The deployed project can be found on:
> http://188.166.100.51/ --> Deployment without use of appleboy/ssh and scp actions
> http://178.128.248.135/ --> Deployment with use of appleboy/ssh and scp action
---

# CD Assignment

For this assignment I made use of a project that I made when watching a Youtube tutorial. I made some changes and did some things diverent from the tutorial. For example I extracted a base template and I used Peewee ORM in stead of SQLAlchemy.

## Goal of assignment

- *Automaticly deploy a project (in my case the Flask project mentioned above) using Github actions and or bash scripting*

The goal, like everthing in life, can be accomplished on many diverent way's. I did two of them, one with the use of 'external action scripts' and one without.

## With external scripts

### **Three components**
- Getting the SSH-keys to work
  - I wanted to make the connection as secure as possible and didn't like to use a password authentication in the script. It didn't work at first, but then I realised that we where connecting from Github to the VPS. So the Github repo had to be in possesion of the key (private key) so it can identify itself to server which has the lock (public key). Important thing to remember is we shouldn't forget to add the public key to the `authorized_keys` file.
- Connect to VPS with the use of secrets and appleboy/scp-action to copy the files to the VPS when the tests passes. 
  -This can be done with the `success()` function. After each step we can check if it was succesfull (exit code 0) or not. If it was successfull the script continous, or else it stops and starts cleaning up.
- When the files are copied, we have to restart the service. 
  - To do this I've added a line to the `sudoers` file, telling it that the user I use to run the service can execute the `sudo systemctl restart ....service` without the need for a password. This had to be done, otherwise the new source-code doesn't seem to get loaded.

### **Three problems**
- Getting the SSH-keys to work
  - As mentiond above I had some trouble getting the SSH key's to work. But after reading alot online I got the concept of the lock and the key. Then everthing fell into place. Afterwards I found a lesson on Winc form Luc that explained it nicely.
- Getting access to the database
  - After copying the files I frequenly got a '502 Bad Gateway' reponse from the Nginx server. After manually restarting, it didn't granted access to the server. It took me a while to figure this out, but it was a permission problem. First I tried the give full acces to the SQLite3 database file, but that didn't seem to fix the problem.
  The solution was to run the service as the same user who had access to the database file. Lucky I created a user and after adding a `User=` to the `project.service` file it still didn't work. 
  Problem, forgot to remove the `DynamicUser=yes` declaration.
- The routes did not work in Flask
  - Problem here was the configuration of the Nginx site config file.   In this file the following line `try_files $uri $uri/ =404;` caused the issue because some of the routes are not real files, therefor a 404 was returnd. After commenting out this file, everthing worked.

## With external scripts

### **Three components**
- Getting the SSH-keys to work
  - I wanted to make the connection as secure as possible and didn't like to use a password authentication in the script. It didn't work at first, but then I realised that we where connecting from Github to the VPS. So the Github repo had to be in possesion of the key (private key) so it can identify itself to server which has the lock (public key). Important thing to remember is we shouldn't forget to add the public key to the `authorized_keys` file.
- Connect to VPS with the use of secrets and appleboy/scp-action to copy the files to the VPS when the tests passes. 
  -This can be done with the `success()` function. After each step we can check if it was succesfull (exit code 0) or not. If it was successfull the script continous, or else it stops and starts cleaning up.
- When the files are copied, we have to restart the service. 
  - To do this I've added a line to the `sudoers` file, telling it that the user I use to run the service can execute the `sudo systemctl restart ....service` without the need for a password. This had to be done, otherwise the new source-code doesn't seem to get loaded.

### **Three problems**
- Getting the SSH-keys to work
  - As mentiond above I had some trouble getting the SSH key's to work. But after reading alot online I got the concept of the lock and the key. Then everthing fell into place. Afterwards I found a lesson from Luc that explained it nicely.
- Getting access to the database
  - After copying the files I frequenly got a '502 Bad Gateway' reponse from the Nginx server. After manually restarting, it didn't granted access to the server. It took me a while to figure this out, but it was a permission problem. First I tried the give full acces to the SQLite3 database file, but that didn't seem to fix the problem.
  The solution was to run the service as the same user who had access to the database file. Lucky I created a user and after adding a `User=` to the `project.service` file it still didn't work. 
  Problem, forgot to remove the `DynamicUser=yes` declaration.
- The routes did not work in Flask
  - Problem here was the configuration of the Nginx site config file.   In this file the following line `try_files $uri $uri/ =404;` caused the issue because some of the routes are not real files, therefor a 404 was returnd. After commenting out this file, everthing worked.

## Without external scripts

The basic configuration of the server is the 

### **Components**
- Setting up runner on VPS
  - I wanted to do the same as above, but without the use of the appleboy action scripts. For that purpose I setup a runner, because now Github Actions is preforming the commands on the VPS. When giving commands through the Action script, it is executed on the VPS instead of on a Github server.
- The restart of the service is the same as above.

### **Problems**
- The above mentioned problems didn't occur here, because I had solved them already.
- There was a permission problem when copying the files. Solved could not find the exact cause, al the permissions where right. Made a work-a-round bij first removing the directory before copying the new information to it
- The database file was overwritten with every new deployment due to overwriting with the testing database. Worked around this problem by before copying removing the testing database file.


## Extra stuff
When solving this assignment the most challenging part was to name the problems and finding the correct terminology. Most problems I had where with setting up the server. When following the instructions it didn't work. So I did some extra stuff.

- Made a seperate user to run login with and run the app through `gunicorn`. Added this user to the `sudo` group and as mentioned above, added this user rights to preform certain tasks without asking for a password. This is usefull when wanting to automate the `systemctl restart`.
- I edited the `sshd_config` to prevent a remote login for the root account and limited the login to only ssh for safety
- I configured the UFW to only accept incoming requests on ports 22 and 80.
- I used symbolic links to get maintain a single-source-of-truth between `sites-availible` and `sites-enabled` in de Nginx configuration
- Tried to write tests for each route in the app.

The report turned out bigger then expected. Hope that's no problem.

## Future learning
By deploying a complexer project learned alot. My testing skills needs to be better. Testing works for now, but as mentioned in de problems section I don't got the hang of initializing a testing database yet.

https://testdriven.io/blog/flask-pytest/