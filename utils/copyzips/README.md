## What is CopyZips

CopyZips is a Custom Resource that copy Zips (or any files, really) between buckets. 

## Why would you use it?

Since AWS doesn't support running creating Lambda Functions using a zipped code from a different region, CopyZips is a workaround that allows you to copy the function zip to the bucket that lives in the region used by the entire stack.

## How to use it?

Check `sample-usage.template.yaml` for a sample.
