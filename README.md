# importEmail
Python Script to import/insert email message into Gmail account.

Useful to try and reproduce issues in test account.

Decided to automate this task as it consisted on a few extra steps:
1) Get the full message (Gmail -> open messages -> click 3 dots menu -> Show original -> copy all
2) Go to [Google's toolbox](https://toolbox.googleapps.com/apps/encode_decode/) and encode in base64_url
3) Copy raw content generated
4) Go to [Gmail API reference](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/import)
5) Paste the raw content in the request body of the API playground
6) Execute call

This script works with a UI where you can browse for the message (.eml or .txt) and it will automatically encode it and execute the call (after authentication), essentially skipping steps 2 through 5.
