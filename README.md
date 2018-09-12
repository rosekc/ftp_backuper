# ftp_backuper

A python script that backup files from remote FTP server.

*WARNING!!! THIS SCRIPT DOES NOT PROVIDE ANY GUARANTEE FOR YOUR DATA INTEGRITY*

## Incentive

It is common that sync your photo in your Android phone via some synchronization service, such as Baidu Netdisk,  Onedrive, ect. However, it seems that a lack of solution for sync in local not. I write this script backup some file in my phone. To do this, you must first intall a file explorer, like MiXplorer, and start a FTP server.

## Usage

```python
from ftp_backuper import FtpBackuper

f = ftp_backuper.FtpBackuper(host='localhost', port=2121, remote_path='DCIM/Camera/')
f.process()
```