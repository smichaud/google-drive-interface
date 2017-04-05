# google-drive-interface
(Work in progress) A custom Python interface based on PyDrive / Google Drive API . Additionally, an interactive shell to interact with the drive.

## Notes
I created this project mainly to get use to the Google Drive tools. Therefore, the interface is quite basic and there is no verification (exceptions, file exists...). I still feel like such a terminal interface can be useful and allows to perform certain things that the existing tools do not. There is more complete/stable solutions out there:

- [gdrive command line utility written in Go](https://github.com/prasmussen/gdrive)
- [another one](https://github.com/odeke-em/drive)

Feel free to send pull requests.

## Dependencies
The only Python dependency is PyDrive:

- pip install PyDrive

You also need to put the ```client_secrets.json``` created using the [Google Drive API credential Wizard](https://console.developers.google.com/flows/enableapi?apiid=drive) at the root of this project.
