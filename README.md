Purpose and Implementation

One of the most common uses of “Clouds”, is shared or backup storage.
A number of services provide free (limited) storage, and several provide an
easy to use, comfortable interface, such as a folder (subdirectory) on your desktop
where you may drop file to be automatically backed up (to the cloud service and
retrieved – or even shared between users), or web-based interface.
Several of these services: Dropbox, Sugarsync, Skydrive, Googledrive, and iCloud
offer free storage.
The Project is to provide a utility that runs on your local device that allows
files in your local file system to be dropped into Google cloud storage, for added
safety those files should be encrypted, and after moving the encrypted file to Google
cloud it should be deleted from the local device. Of course, you should be able to
retrieve a file and decrypt it.
You should use a (validated) single key encryption, such as AES, and each file may
have it’s own key (password) so your program should prompt for that key/password.
You should also (in your program) be able to list and remove files from your
cloud storage.
You may use the provided python prototype to start implementation.
You
