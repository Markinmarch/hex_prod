# import requests module
import requests

# Making a get request
response = requests.get('https://www.youtube.com/')

# print response
print(response)

# print check if an error has occurred
print(response.raise_for_status())

# ping an incorrect url
response = requests.get('https://www.youtube.com/')

# print check if an error has occurred
print(response.raise_for_status())