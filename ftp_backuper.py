import ftplib
import os
from pathlib import Path, PurePosixPath

def chdir(path):
    """change the cwd. If path does not exists, create it.
    
    :param path: path like object
    """

    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

class FtpBackuper:
    def __init__(self, host, port=0, remote_path='/',
                 user='', password='', local_path=''):
        """Create a Backuper.
        
        :param host: ftp host
        :param port: ftp port, defaults to 0
        :param remote_path:remote path that would backup, defaults to '/'
        :param user: ftp username, defaults to ''
        :param password: ftp password, defaults to ''
        :param local_path: local path that save the remote backup file, defaults to ''
        """

        self._ftp = ftplib.FTP()
        self._ftp.connect(host, port)
        self._ftp.login(user, password)
        self._ftp.cwd(remote_path)
        self.local_path = Path(local_path)
        self.remote_path = PurePosixPath(remote_path)

    def process(self):
        self._walk(PurePosixPath())

    def _walk(self, cur_path):
        self._ftp.cwd(str('/' / cur_path))
        p = self.local_path / cur_path
        chdir(p)
        items = []
        self._ftp.retrlines('LIST {}'.format(str(self.remote_path / cur_path)), items.append) 
        items = [str.split(_) for _ in items]
        for i in items:
            filename = i[-1]
            print('processing: {}'.format(self.remote_path / filename))
            is_dir = i[0][0] == 'd'
            if is_dir:
                self._walk(cur_path / filename)
                #self._ftp.cwd(str('/' / cur_path))
                p = self.local_path / cur_path
                chdir(p)
            elif not os.path.exists(filename):
                self.retrieve_file(filename, self.remote_path / filename)

    def retrieve_file(self, filename, path, blocksize=8192, rest=None):
        cmd = 'RETR {}'.format(path)
        with open(filename, 'wb') as f:
            return self._ftp.retrbinary(cmd, f.write, blocksize, rest)
