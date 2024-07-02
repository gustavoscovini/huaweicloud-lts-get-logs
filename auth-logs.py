import requests
from utils import update_values

# Authentication endpoint
AUTH_ENDPOINT = 'https://iam.myhuaweicloud.com/v3/auth/tokens'
START_TIME = '1712322223000'  # This time is in timestamp, use this site as reference https://www.epochconverter.com/
END_TIME = '1712325823000'
REGION_PROJECT_ID = '...'
LOG_GROUP_ID = '...'
LOG_STREAM_ID = '...'

# Change the values according to your account
ACCOUNT_VARIABLES = {
    'AccountName': '...',
    'IAMUser': '...',
    'IAMPasswd': '...',
    'region': 'sa-brazil-1',
    'IAMUserID':  '',
    'MFACode': ''
}

# Request body for token generation with MFA
body_authorization = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "domain": {
                        "name": "{AccountName}"
                    },
                    "name": "{IAMUser}",
                    "password": "{IAMPasswd}"
                }
            }
        },
        "scope": {
            "project": {
                "name": "{region}"
            }
        }
    }
}


#     "auth": {
#         "identity": {
#             "methods": [
#                 "password",
#                 "totp"
#             ],
#             "password": {
#                 "user": {
#                     "name": "{IAMUser}",
#                     "password": "{IAMPasswd}",
#                     "domain": {
#                         "name": "{AccountName}"
#                     }
#                 }
#             },
#             "totp": {
#                 "user": {
#                     "id": "{IAMUserID}",
#                     "passcode": "{MFACode}"
#                 }
#             }
#         },
#         "scope": {
#             "domain": {
#                 "name": "{AccountName}"
#             },
#             "project": {
#                 "name": "{region}"
#             }
#         }
#     }
# }

# Put the values of 'replacements' into 'data'
formatted_data = update_values(body_authorization, ACCOUNT_VARIABLES)
print(formatted_data)
# Make the request to get the token
response = requests.post(AUTH_ENDPOINT, json=formatted_data,
                         headers={'Content-Type': 'application/json; charset=UTF-8'})
token = 'Bearer ' + response.headers['X-Subject-Token']

print(token)
# Update the header for other requests
headers = {
    'Authorization': token,
    'Content-Type': "application/json;charset=UTF-8",
}

# Another request, change the values in format according to you account

url = ('https://lts.sa-brazil-1.myhuaweicloud.com/v2/{region_projectId}/groups/{log_groupId}/streams/{'
       'log_streamId}/content/query').format(region_projectId=REGION_PROJECT_ID, log_groupId=LOG_GROUP_ID,
                                             log_streamId=LOG_STREAM_ID)

body = {
    "start_time": START_TIME,
    "end_time": END_TIME
}

# Make the request for logs, don't forget to pass the header
response = requests.post(url, headers=headers, json=body)

# Print the response
print(response.text)
