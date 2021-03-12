## The deployed project can be found on:
> [![Deploy without ssh](https://github.com/dpendjol/FoodTracker/actions/workflows/deploy.yml/badge.svg)](https://github.com/dpendjol/FoodTracker/actions/workflows/deploy.yml)  
> [Deployment without use of appleboy/ssh and scp actions and self-hosted Action Runner](http://188.166.100.51/)

> [![Deploy through ssh](https://github.com/dpendjol/FoodTracker/actions/workflows/deploy_ssh.yml/badge.svg)](https://github.com/dpendjol/FoodTracker/actions/workflows/deploy_ssh.yml)  
> [Deployment with use of appleboy/ssh and scp action and Github Action Runner](http://178.128.248.135/)
---

# CD Assignment

For this assignment I made use of a project that I made when watching a Youtube tutorial. I made some changes and did some things different from the tutorial. For example I extracted a base template and I used Peewee ORM in stead of SQLAlchemy. The report is alot longer then 300 words, hope thats not a problem.

## Goal of assignment

- *Automatically deploy a project (in my case the Flask project mentioned above) using Github actions and/or bash scripting*

The goal, can be accomplished in many different ways. I did two of them, one with the use of 'external action scripts' and one without them.

## With external scripts

### **Three components**
- Getting the SSH-keys to work
  - I wanted to make the connection as secure as possible and didn't like to use a password authentication in the script. An important thing to remember is not to forget to add the public key to the `authorized_keys` file.
- Connect to VPS with the use of secrets and appleboy/scp-action to copy the files to the VPS when the tests passes. 
  - This can be done with the `success()` function. After each step we can check if it was succesfull or not. If it was succesfull the script continous, or else it stops and starts cleaning up.
- When the files are copied, we have to restart the service. 
  - To do this I've added a line to the `sudoers` file, telling it that the user I use to run the service can execute the `sudo systemctl restart ....service` without the need for a password. This had to be done, otherwise the new source-code doesn't seem to get loaded.

### **Three problems**
- Getting the SSH-keys to work
  - It didn't work at first, but then I realised that we were connecting from Github to the VPS. So the Github repo had to be in possession of the key (private key) so it can identify itself to the server which has the lock (public key). But after reading a lot online I got the concept of the lock and the key.Afterwards I found a lesson on Winc from Luc that explained it nicely.
- Getting access to the database
  - After copying the files I frequenly got a '502 Bad Gateway' reponse from the Nginx server. After manually restarting, it didn't grant access to the server. It took me a while to figure this out, but it was a permission problem. First I tried the give full access to the SQLite3 database file, but that didn't seem to fix the problem.
  The solution was to run the service as the same user who had access to the database file. Luckily I created a user and after adding a `User=` to the `project.service` file it still didn't work. 
  Problem, forgot to remove the `DynamicUser=yes` declaration.
- The routes did not work in Flask
  - Problem here was the configuration of the Nginx site config file.   In this file the following line `try_files $uri $uri/ =404;` caused the issue because some of the routes are not real files, therefore a 404 was returnd. After commenting out this file, everthing worked.

## Without external scripts

The basic configuration of the server is the same as the version with external scripts.

### **Components**
- Setting up runner on VPS
  - I wanted to do the same as above, but without the use of the appleboy action scripts. For that purpose I setup a runner, because now Github Actions is performing the commands on the VPS. When giving commands through the Action script, it is executed on the VPS instead of on a Github server.
- The restart of the service is the same as above.

### **Problems**
- The above mentioned problems didn't occur here, because I had solved them already.
- There was a permission problem when copying the files. I solved it, but I could not find the exact cause, all the permissions were right. I added a `-f` flag to the `cp` command to force a copy.
- The database file was overwritten with every new deployment due to overwriting with the testing database. Worked around this problem by  removing the testing database file before copying all of the source files.


## Extra stuff
When solving this assignment the most challenging part was to name the problems and finding the correct terminology. Most problems I had were with setting up the server. When following the instructions it didn't work. So I did some extra stuff.

- Made a seperate user to run login with and run the app through `gunicorn`. Added this user to the `sudo` group and as mentioned above, added this user rights to perform certain tasks without asking for a password. This is usefull when wanting to automate the `systemctl restart`.
- I edited the `sshd_config` to prevent a remote login for the root account and limited the login to only ssh for safety.
- I configured the UFW to only accept incoming requests on ports 22 and 80.
- I used symbolic links to get maintain a single-source-of-truth between `sites-availible` and `sites-enabled` in de Nginx configuration
- Tried to write tests for each route in the app.

The report turned out bigger then expected. Hope that's no problem.

## Future learning
By deploying a complexer project I learned a lot. My testing skills need to be better. Testing works for now, but as mentioned in the problems section I didn't get the hang of initializing a testing database just yet. So I used a work-a-round for now. But this is a project that I want to continue developing.