Flask-Session-Pynamodb
=============
Clone from: https://github.com/pallets-eco/flask-session
Flask-Session is an extension for Flask that adds support DynamoDB for server-side sessions to
your application.

# Installation
````
pip install flask-session-custom
````

# Configuration
Read here: https://flask-session.readthedocs.io/en/latest/

Configure for dynamodb:

| Name        | Description          |
|-----------|----------------------|
| `SESSION_TYPE`    | Set up is `dynamodb` |
| `SESSION_DYNAMODB_TABLE` | The name of the table in DyanmoDB to store session data. Default is "sessions".|
| `SESSION_DYNAMODB_REGION` | 	The region where the dynamodb table is located. Uses environment variable or the local config if not set.|
| `SESSION_DYNAMODB_KEY_ID` | The AWS key id for connecting to Dynamo. Uses environment variable or local config if not set.|
| `SESSION_DYNAMODB_SECRET` | The AWS secret access key for connecting to Dynamo. Uses environment variable or local config if not set.|
| `SESSION_DYNAMODB_ENDPOINT_URL` | The AWS DynamoDB endpoint_url. Default is none, primarily used for local DynamoDB config.|

