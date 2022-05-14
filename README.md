# distributed-face-detection
This repository contains the codes for the AWS implementation of distributed face detection

The files in lambda directory contains the codes for the parent and worker lambdas. All worker lambdas are identical and will have same codes. AWS Policy has to be created for parent lambda which will allow it to invoke the worker lambdas. The ARN of the worker lambdas have to be specified when invoking them and passing parameters to them.
The worker lambdas need to perform image processing and use OpenCV library for the same. A Lambda layer needs to be created for OpenCV. Dockerfile for the same has been included, which contains container rules for installing all necessary dependencies for OpenCV. 
