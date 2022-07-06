# Task 7: HELP 🙃

## DESCRIPTION

Ok, looks like you’ve totally screwed yourself over and released code in the environment that causes a cryptominer to be dropped on all visitors to SudoSingles’ website... Not good.

You need to A) clean this mess up, and B) fix the underlying vulnerability. There’s no way to know how much more malware might be hiding in the S3 environment!

However, all the Java developers at SudoSingles™ Inc. are competing in a week-long Super Smash Brothers tournament in a gigantic Faraday cage on a remote island. Some kind of teambuilding activity, they said… Sorry, I have no idea. But you’re on your own -- the devs are totally unreachable

You need to make sure that even if the backend is exploited, SudoSingles™ will serve no malware to its users. Luckily you are a Trend Micro Cloud One customer and have FSS at your disposal.

The only issue is that the malware is already in that bucket, and the bucket has millions of profile pictures already in it! There’s no way to scan all those existing files with FSS in the normal configuration – trust me, I’ve tried. And you need to stop this now.

Luckily, there is a better way. You’ve heard about the new ScanOnGetObject feature of FSS that should help here.

## DETAILS

In this challenge, you need to deploy a FSS All-In-One Stack with the ScanOnGetObject feature enabled to protect the bucket that contains all the profile pictures of the SudoSingles™ users.

We would normally do this using the simple CloudFormation template generated in the FSS console, but we can’t do that on Tech Day. So we’re going to use the AWS Service Catalog.

Navigate to the Service Catalog and launch the “File Storage Security All in One Template” product. This is an exact copy of the CloudFormation template from the FSS console.

Configure the stack to protect the bucket found under “FSSBucketToProtect” in the Credentials field below. Also, make sure to enable the ScanOnObject get feature, and to set your region to trend-us-1.

Finally, you’ll need to acquire your FSS external ID to finish launching the AIO stack. I’ll leave this one up to you.

Once the FSS All-In-One Stack is finished deploying, enter “I did it” in the box below, and hit “Submit.”

## NOTES

This answer is on the honor system. Don’t let it get to your head.

## SCORING

String answer:

I did it

## HINTS

### HINT 1

You can get your external ID by trying to launch an FSS template from the FSS console, and copying the value from there. Or you can use the FSS api. Your choice.

### HINT 2

If the template isn’t deploying, delete the service catalog and try again, making sure that your region and ExternalID are correct.

### HINT 3

    Find your external ID by launching a stack from the FSS console and copying the External ID value

    Fill in the service catalog template, making sure to set ScanOnGetObject to true, region to trend-us-1, bucket to the value of FSSBucketToProtect from the Credentials field of mission control, and the external ID to the external ID from step 1

    You’re done when the FSS stack is in CREATE_COMPLETE status.
