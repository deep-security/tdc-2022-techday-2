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

### HINT 2

### HINT 3

Hint 3
