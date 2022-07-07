# Task 2: Off to the RCE-es 😈

## DESCRIPTION

SudoSingles™ is an incredibly modern application built by genius engineers.

And as all genius engineers know, microservices are the best thing you can do for an application. Therefore, the SudoSingles™ platform is made up of several interconnected microservices that all do specific tasks.

One of the main components of SudoSingles™ is a containerized Java microservice that optimizes all images uploaded to the website for display on the web and uploads them all to one big S3 bucket full of profile pictures.

A little birdie has told you that SudoSingles™’s image processing microservice is vulnerable to the log4shell attack. You’ve also found a m Well, you used to moonlight as a "l33t" haxor back in the day, so maybe you can use your skills to verify if that’s true.

## DETAILS

The intel you got also indicated that a hacker spun up an attack machine on your network. Not good. Time to check it out.

Find the “FSSAttackerMachineAccessUrl” entry in the Credentials section below. You should be taken to a login screen. You can log in using the “Player” user and your “PlayerPassword,” also found in the Credentials section.

You’ll know you’ve logged in successfully if you’re taken into a desktop environment in your browser, complete with programs like a Terminal Emulator, a File Browser, and a Web Browser. Feel free to click around to verify everything works.

To complete this task, enter the *hostname* of the attack machine and hit “Submit.”

## NOTES

ONLY ONE USER CAN BE LOGGED IN AT A TIME.

If more than one user tries to log on, the first user will be frozen out. So, select the member of your team that you feel is the most "l33t" and delegate them to control the attack machine for this challenge.

If you run into trouble loading the environment, maybe switch to Chrome? I hate to be that guy, but it might help for this challenge.

## SCORING

attacker-machine

## HINTS

### HINT 1

There are many commands in the terminal that can help you find your hostname... Google is probably your friend here!

### HINT 2

Since this is a Linux system, Google “How to find my hostname on Linux.” There are many ways to do this, but you’ll probably have to run a command in the Terminal Emulator application (found in the bottom bar). Enter the full name (for example “host-name”).

### HINT 3

1. Open the Terminal application. You can find it on the bar at the bottom of the page.

2. Enter “hostname”

3. The output of this command is the string answer.


