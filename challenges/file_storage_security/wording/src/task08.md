# Task 8: Import What? 😕

## DESCRIPTION

Since you can’t fix the application to stop having vulnerabilities right now, you need to stop the application from returning malware to the user.

To that end, you need to protect the microservice that serves the optimized images from the image bucket. That way, whenever the webpage asks for a file, if it would return malware, it instead … doesn't do that.

## DETAILS

In order to protect the microservice, you must find the microservice.

In the "Credentials" section, you can find a link to the Lambda with the microservice’s code under “FSSLambdaToProtect.” Go ahead and navigate to that link.

You’ll see it’s a Python function that fetches images from the Image bucket and returns them to the rest of the application.

To complete this challenge, enter the first line of code of this Lambda function.

## NOTES

This is just to make sure you’re on the right page.

Deleting or messing up this code is like breaking a mirror—if you do it, you'll have seven years of bad luck. So be careful to not delete or change anything you shouldn't.

## SCORING

import base64

## HINTS

### HINT 1
You can find the Code on the page if you scroll down a little. Make sure you have the "Code" tab selected. Also, make sure to enter the first line of code, exactly as it appears.

### HINT 2
1. Navigate to the URL found in the "Credentials" section under "FSSLambdaToProtect."
2. Find the "Code" section of the Lambda page.
3. Copy the first line (import base64) into Mission Control, and hit "Submit."