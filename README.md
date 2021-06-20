# fetch_rewards
Fetch rewards devops challenge

## Assumptions

1. If the instance has to be accessed from the default user: with sudo access pass
the key-pair through server configuration.yaml at line 10 and uncomment line 80 at
infrastructure.py on instance creation else the instance will be accessed just but 
non-root users passed as a part of user configuration
2. Assumed that the instance’s security profile has ports 22 open to the users instance
3. Added region as a part of instance configuration
4. Instance deletion is not a part of the task, so created instances has to be 
manually deleted

## Logic
1. Users are added as part of a group called shared
2. A directory called sharedFolder1 is created at / path in vol1
3. A directory called sharedFolder2 is created at /data path in vol2
4. Both the directories sharedFolder1 and sharedFolder2 is modified to allow
rwx access for the shared linux group
5. Users are allowed to read and write their own filed for enhanced security

## Script Execution steps

### Install dependencies
```bash
$ pip3 install -r requirements.txt
```
### Run script
```bash
$ cd sourcefiles && python3 infrastructure.py  
```
## Steps after execution
1. after sshing as user1 navigate to sharedFolder1  `$ cd /sharedFolder1` 
2. create a txt file and add a line to it `$ touch user1.txt && echo hi from user1 from sh1 > user1.txt`
3. Then read the text using `$ cat user1.txt`
4. repeat the steps 2 and 3 by navigating to sharedFolder 2 `$ cd /data/sharedFolder2`
5. Same applies for other users
6. If all files and folder under the shared folders needs to accessed by every user then add an `-R` flag at lines 15 and 18 of user_data.sh. For eg:  `chmod -R ...`