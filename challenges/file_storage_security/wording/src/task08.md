# C1 - File Storage Security - Task 8: Wire It Up 🔌

## DESCRIPTION

Good job deploying the All-In-One stack. Again, you would normally do this right from the FSS Console, but you can't do that today. So thanks for putting up with the extra steps.

To finish setting up the FSS resources, you'll need to add the stack you created to the FSS console.

## DETAILS

Navigate to your FSS console and register the stack you just created. You'll add both the Scanner and Storage stack by clicking the "+ Deploy" button and using the outputs from the Service Catalog product.

When you've added your Scanner and Storage stacks to the console, enter the name of the Scanner Stack, as it appears in the FSS console, and hit "Submit" below.

## NOTES

You've already deployed the stack, so you won't need to launch any CloudFormation templates in this challenge. You'll just need to add a few ARNs to register the stack you've already created to your account.

## SCORING

<!-- https://simple-regex.com/build/62d1a489e5df9 -->

/^(?:SC)(?:-)[0-9]{12}(?:-pp-)(?:[0-9]|[a-z]){13}(?:-ScannerStack-)(?:[0-9]|[A-Z]){12}/

## HINTS

### HINT 1

Make sure you've deployed the All In One Stack Service catalog product template with "ScanOnGetObject" set to true, the region set to "trend-us-1", and your ExternalID properly set.

### HINT 2

1. Take note of the "ScannerStackManagementRoleARN" and "StorageStackManagementRoleARN" from the outputs of your provisioned Service Catalog product.
2. Navigate to the FSS console, and click the blue "+ Deploy" button.
3. Click the "Scanner Stack and Storage Stack" option.
4. Paste in the value of "ScannerStackManagementRoleARN" for Step 3 and "StorageStackManagementRoleARN" for Step 4.
5. Click submit and wait for the stacks to deploy successfully.
6. When that has completed, copy the Scanner Stack name found under the "Scanner Stack" heading in the left-hand pane. It should look something like: "SC-############-pp-xxxxxxxxxxxxx-ScannerStack-xxxxxxxxxxxx"