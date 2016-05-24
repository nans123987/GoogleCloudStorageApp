

# import statements.
import argparse
import httplib2
import os
import sys
import json
import time
import datetime
import io
import hashlib
import tkFileDialog
# Google apliclient (Google App Engine specific) libraries.
from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaIoBaseUpload
import easygui
# pycry#pto libraries.
from Crypto import Random
from Crypto.Cipher import AES

# from googleapiclient.discovery import MEDIA_BODY_PARAMETER_DEFAULT_VALUE


# Encryption using AES
# You can read more about this in the following link
# http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto


# Initial password to create a key
password = 'googlecloud'
# key to use
key = hashlib.sha256(password).digest()

# this implementation of AES works on blocks of "text", put "0"s at the end if too small.
def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

# Function to encrypt the message
def encrypt(message, key, key_size=256):
    message = pad(message)
    # iv is the initialization vector
    iv = Random.new().read(AES.block_size)
    # encrypt entire message
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

# Function to decrypt the message
def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

# Function to encrypt a given file
def encrypt_file(file_name, key):
    print ("something")
    # Open file to read content in the file, encrypt the file data and
    # create a new file and then write the encrypted data to it, return the encrypted file name.



# Function to decrypt a given file.
def decrypt_file(file_name, key):
    print ("something")
    # open file read the data of the file, decrypt the file data and 
    # create a new file and then write the decrypted data to the file.

_BUCKET_NAME = 'hallowed-tea-132123'  # name of your google bucket.
_API_VERSION = 'v1'

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# client_secret.json is the JSON file that contains the client ID and Secret.
# You can download the json file from your google cloud console.
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. 
# These scopes are used to restrict the user to only specified permissions (in this case only to devstorage) 
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/devstorage.full_control',
      'https://www.googleapis.com/auth/devstorage.read_only',
      'https://www.googleapis.com/auth/devstorage.read_write',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

# Downloads the specified object from the given bucket and deletes it from the bucket.
def get(service):
  # User can be prompted to input file name(using raw_input) that needs to be be downloaded, 
  # as an example file name is hardcoded for this function.
  try:
# Get Metadata
    listobj(service)
    name = raw_input("\nPlease enter the file you want to download:  ")
    req = service.objects().get(
            bucket=_BUCKET_NAME,
            object=name,
            fields='bucket,name,metadata(my-key)',
        
                )                   
    resp = req.execute()
    print json.dumps(resp, indent=2)

# Get Payload Data
    req = service.objects().get_media(
            bucket=_BUCKET_NAME    ,
            object=name,
        )    
# The BytesIO object may be replaced with any io.Base instance.
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, req, chunksize=1024 * 1024)  # show progress at download
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print 'Download %d%%.' % int(status.progress() * 100)
        print 'Download Complete!'
    # decodefile = decrypt(fh.getvalue(),key)
    with open(name, 'wb') as fo:
        fo.write(fh.getvalue())
        print json.dumps(resp, indent=2)
    

  except client.AccessTokenRefreshError:
    print ("Error in the credentials")

    # Puts a object into file after encryption and deletes the object from the local PC.
def put(service):
    
    filePath = tkFileDialog.askopenfilename()
    FileBaseName = os.path.basename(filePath)
    
    Body = {
        'name': FileBaseName,
    }
    
    with open(filePath, 'rb') as fi:
        req = service.objects().insert(
            bucket=_BUCKET_NAME,
            body=Body,
            media_body=MediaIoBaseUpload(fi, 'application/octet-stream'))
        result = req.execute()
    os.remove(filePath)
    easygui.msgbox("File uploaded Successfully and deleted", "Success!", "Done")
   

# Lists all the objects from the given bucket name
def listobj(service):
    '''List all the objects that are present inside the bucket. '''
    
    fields_to_return = \
        'nextPageToken,items(name)'

    req = service.objects().list(bucket=_BUCKET_NAME, fields=fields_to_return)
    all_objects = []
    
    while req:
        resp = req.execute()
        all_objects.extend(resp.get('items', []))
        req = service.objects().list_next(req, resp)
    for item in all_objects:
        print item[u'name']
    


# This deletes the object from the bucket
def deleteobj(service):
    '''Prompt the user to enter the name of the object to be deleted from your bucket.
        Pass the object name to the delete() method to remove the object from your bucket'''
    
    listobj(service)
    f_name = raw_input("\n\nEnter the Filename to delete from cloud storage:  ")
    
    req = service.objects().delete(bucket=_BUCKET_NAME, object=f_name)
    req.execute()
    
    easygui.msgbox("File successfully deleted from cloud storage", "Success", "Close")
    
    

    
def main(argv):
  
  
  print ("1. Upload FIle to google Cloud Storage")
  print ("2. Download file from google cloud storage")
  print ("3. Get List of files in google cloud bucket")
  print ("4. Delete a file in the google cloud storage bucket")
  x = raw_input("\n\nChoose an option : ")
 # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  
  # sample.dat file stores the short lived access tokens, which your application requests user data, attaching the access token to the request.
  # so that user need not validate through the browser everytime. This is optional. If the credentials don't exist 
  # or are invalid run through the native client flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file (sample.dat in this case). 
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Cloud Storage API.
  service = discovery.build('storage', _API_VERSION, http=http)

  # This is kind of switch equivalent in C or Java.
  # Store the option and name of the function as the key value pair in the dictionary.
  options = {1: put, 2: get, 3:listobj, 4:deleteobj}
   # Take the input from the user to perform the required operation.
  # for example if user gives the option 1, then it executes the below line as put(service) which calls the put function defined above.
  
  options[int(x)](service)
 

if __name__ == '__main__':
  main(sys.argv)
# [END all]
