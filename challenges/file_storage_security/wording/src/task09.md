# Task 9: Too EZ 😎

## DESCRIPTION

To deploy protection, all you have to do is make the function grab objects from the FSS ScanOnGetObject Object Lambda Access Point (say that five times fast).

Even if you don’t know Python, don’t worry. If you can type, you can deploy protection.

## DETAILS

You can find the ScanOnGetObject Access point for the deployed “File Storage Security All in One Template” product under the “ScanOnGetObjectAccessPointARN” entry in Events ⇒ Outputs.

Find the line that starts with “bucket =” at the top of the Python file, and replace everything inside the quotes with the ScanOnGetObjectAccessPointARN value.

Once you’ve done this, click “Deploy” to deploy your new function version to production.

Click Verify once you’re done deploying protection.

## NOTES

## SCORING

protectionChecker

## HINTS

### HINT 1
If you don't have the “ScanOnGetObjectAccessPointARN” entry in Events ⇒ Outputs for your File Storage Security All In One Service Catalog product, redeploy the product with "ScanOnGetObject" set to "true". The ARN will look like: "arn:aws:s3-object-lambda:xx-xxxx-x:xxxxxxxxxxxx:accesspoint/fss-olap-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

### HINT 2
The code you have to change is on line 11. Make sure you've activated your FSS stack in the FSS console using the ScannerStackManagementRoleARN and StorageStackManagementRoleARN. Finally, ensure that the ARN is entered correctly into the bucket variable. 

### HINT 3

1. Make sure you have the FSS AIO Service Catalog product deployed successfully with "ScanOnGetObject" set to "true," and that you've added the stack to the FSS console.
2. Copy the ARN from “ScanOnGetObjectAccessPointARN” entry in Events ⇒ Outputs.
3. Navigate to the "FSSLambdaToProtect" URL from the "Credentials" section to be taken to the Lambda code page.
4. Replace line 11 with the following, replacing the ARN with the ARN you copied from step 2: bucket = "arn:aws:s3-object-lambda:xx-xxxx-x:xxxxxxxxxxxx:accesspoint/fss-olap-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"