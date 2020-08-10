# aws-automation-boto3-examples
AWS Automation boto3 Examples

Documentation Link: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

Boto3 is the Amazon Web Services (AWS) SDK for Python. It enables Python developers to create, configure, and manage AWS services, such as EC2 and S3. Boto3 provides an easy to use, object-oriented API, as well as low-level access to AWS services.

Prerequisites: 
  Anaconda ( https://www.anaconda.com/products/individual ). Anaconda is a free and open-source distribution of the Python and R programming languages for scientific computing, that aims to simplify package management and deployment. It will contain all the packages required to test the automation scripts.

Boto3 looks at various configuration locations until it finds configuration values. Boto3 adheres to the following lookup order when searching through sources for configuration values:

    A Config object that's created and passed as the config parameter when creating a client
    Environment variables
    The ~/.aws/config file

We will use environment variables to set AWS Access key ID & Secret access key as below.

On Windows: ( Updated below key and secret with your AWS key and secret )

  set AWS_ACCESS_KEY_ID=XXXXXXXXXX <br />
  set AWS_SECRET_ACCESS_KEY=XXXXXXXXXX

On Linux:

  export AWS_ACCESS_KEY_ID=XXXXXXXXXX <br />
  export AWS_SECRET_ACCESS_KEY=XXXXXXXXXX
