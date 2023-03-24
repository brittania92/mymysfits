# Mystical Mysfits

This project includes sample code in your desired programming language and front-end framework to build and deploy a well-architected 3-tier modern web application.  This blueprint was inspired [Mythical Mysfits website](https://mythicalmysfits.com/). Mythical Mysfits have been used in several public [AWS workshops](https://workshops.aws/) and [Game Days](https://aws.amazon.com/gameday/).  These workshops and game days seek to educate and demonstrate to our customers what is possible on AWS; through this Blueprint we seek to do the same.  

The project uses [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/) to define and deploy the AWS resources that run this project's application.  

`/cdkStacks` contains the infrastructure as code (IaC) cdk stack files.

`/src` contains the application source code

`/web` contains the frontend source code.  

## Local Development

*Note*
We recommend to use the projct's included CI/CD workflows that are located in the repository's `.codecatalyst/workflows` directory to deploy code changes.  Provided below are sample instructions on how to commit and verify a change.  

### Install Dependencies

```bash
    python3 -m pip install -r requirements-dev.txt
```

Or use the included Makefile

```bash
    make install
```

### Run unit tests

```bash
    pytest -k unit
```

Or use the included Makefile

```bash
    make unit-test
```

### Run integration tests

Integration tests will run against a deployed backend.  Use the project workflow's output variable `apiUrl` for the value of API_ENDPOINT environment variable.

```bash
    export API_ENDPOINT="{apiUrl_value}"
    pytest -k integ
```

Or use the included Makefile

```bash
    export API_ENDPOINT="{apiUrl_value}"
    make integ-test
```

### Build frontend

Building the frontend correctly requires you to set the endpoint for the backend.  This value is obtained from the output variable `apiUrl`

```bash 
    export VITE_API_ENDPOINT="{apiUrl_value}"
    cd web
    npm install
    npm run build-only
    # Needed to persist the build directory after build
    checkout web/build/.gitkeep
```

Or use the included Makefile

```bash
    export VITE_API_ENDPOINT="{apiUrl_value}"
    make build-frontend
```

## Sample Change

For this sample change, we are going to update the data file that gets stored in our DynamoDBTable.  The included data file is upserted into our table when the data changes, which allows us to add new mysfits via our CI/CD pipeline.  

1) From CodeCatalyst Code Menu, create a new Dev enviornment from the main branch in the project's repo.

2) From the IDE, open the file `src/mysfit_data.json`

3) Add the following elements to the existing json structure.  Adjust for formatting and save.  

```javascript
{  
    "Age": 64,
    "Description": "Doctor Doom loves rock & roll and is known to prespire under the bright lights.  His motto is 'Everything fails all the time!",
    "GoodEvil": "Good",
    "LawChaos": "Chaotic",
    "Name": "Dr. Doom",
    "ProfileImageUri": "https://deyn4asqcu6xj.cloudfront.net/3tierapp/img/doctor_doom.png",
    "Species": "CTO",
    "ThumbImageUri": "https://deyn4asqcu6xj.cloudfront.net/3tierapp/img/doctor_doom.png"    
},
{
    "Age": 54,
    "Description": "Nice!",
    "GoodEvil": "Good",
    "LawChaos": "Lawful",
    "Name": "JazzyJassy",
    "ProfileImageUri": "https://deyn4asqcu6xj.cloudfront.net/3tierapp/img/jazzy_jassy.png",
    "Species": "CEO",
    "ThumbImageUri": "https://deyn4asqcu6xj.cloudfront.net/3tierapp/img/jazzy_jassy.png"    
},
{
    "Age": 54,
    "Description": "Work Hard, have fun, make history",
    "GoodEvil": "Neutral",
    "LawChaos": "Lawful",
    "Name": "BlueOrigin",
    "ProfileImageUri": "https://deyn4asqcu6xj.cloudfront.net/3tierapp/img/blue_origin.png",
    "Species": "Chairman",
    "ThumbImageUri": "https://deyn4asqcu6xj.cloudfront.net/3tierapp/img/blue_origin.png"    
},
```
4) Adding additional mysfits will break our unit tests.  In the supplied tests we are expecting only 12 mysfits to be included in our dataset.  Update the value 12 to 15 in both test files in the `tests` directory.

5) After saving the file commit and push your changes
```bash
git commit -am "updating mysfits"
git push
```

6) Navigate to the project's workflows and wait for the deployment pipelines to complete.  Use the View App link in the deploy_frontend action to observe your changes. 

## CDK Deployment
If you still want to deploy without using CI/CD workflows, you can just install the python dependencies:
```bash
    python3 -m pip install -r requirements.txt
```
and run:
```bash
    cdk deploy
```

## Connections and permissions

This blueprint requires a custom development role.  To create one, click "Add an existing IAM role" from the add IAM role options. The IAM role needs to contain the CodeCatalyst trust policy, as well as the following permissions:

```
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "cloudformation:*",
              "ecr:*",
              "ssm:*",
              "s3:*",
              "codeguru-reviewer:*",
              "iam:Get*",
              "iam:PassRole",
              "iam:CreateRole",
              "iam:DeleteRole",
              "iam:TagRole",
              "iam:UpdateRole",
              "iam:AttachRolePolicy",
              "iam:DetachRolePolicy",
              "iam:PutRolePolicy",
              "iam:CreateServiceLinkedRole",
              "iam:CreatePolicy",
              "iam:DeletePolicy",
              "iam:CreatePolicyVersion",
              "iam:DeletePolicyVersion",
              "iam:PutRolePermissionsBoundary",
              "iam:DeleteRolePermissionsBoundary",
              "sts:AssumeRole",
              "sts:GetCallerIdentity"
          ],
          "Resource": "*"
      }
  ]
}
```

The IAM roles also require the Amazon CodeCatalyst service principals `codecatalyst.amazonaws.com` and `codecatalyst-runner.amazonaws.com`.

### Required IAM role trust policy:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "codecatalyst.amazonaws.com",
                    "codecatalyst-runner.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```
