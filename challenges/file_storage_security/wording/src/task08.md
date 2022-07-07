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

## SCORING

import base64

## HINTS

### HINT 1

### HINT 2

### HINT 3

Hint 3
