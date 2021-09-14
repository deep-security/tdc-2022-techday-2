## What is MissionControlChecker

This is a stack that creates a Lambda that is callebable by Mission Control, interfacing with it and the challenges in order to execute specific functions.

## Why would you use it?

This allows you, challenge creator, to create challenges that don't have a Static flags (such as a hardcoded string). It can, dynamically, verify for a condition given you write another lambda to do so.

## How to use it?

*NOTE: Still subject to change*

You'll need to create, per task, lambda code that verifies the completetion of the task and provide the function's name to the Mission Control team in order to properly trigger it when a team tries to answer the task. We expect a easy-to-understand name, like XDRTask1.

Details on how to implement you own lambda can be find both in `sample.py` and `sample.js`, depending on your language of choice.