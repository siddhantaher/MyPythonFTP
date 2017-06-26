import os
from ftplib import FTP
from paramiko.client import SSHClient, AutoAddPolicy
from contextlib import closing
from config import config


def export_via_ftp(local_file, file_name):
    with closing(FTP(
            host=config['host'],
            user=config['user'],
            passwd=config['password'])) as ftp:
        ftp.cwd(config['destination'])
        with open(local_file, 'rb') as f:
            if os.path.isfile(local_file):
                ftp.storbinary(('STOR {}').format(package_name), f)
            else:
                raise IOError('File {} not found!'.format(local_file))


def export_via_sftp(local_file, file_name):
    with closing(SSHClient()) as client:
        client.set_missing_host_key_policy(AutoAddPolicy)
        client.connect(
            hostname=config['host'],
            port=int(config['port']),
            username=config['user'],
            password=config['password']
        )
        with closing(client.open_sftp()) as sftp:
            if os.path.isfile(local_file):
                sftp.put(local_file, ('{}/{}').format(
                            config['destination'],
                            file_name))
            else:
                raise IOError('File {} not found!'.format(local_file))


def export_factory(arg):
        return EXPORT_TYPE[arg]


EXPORT_TYPE = {
    'ftp': export_via_ftp,
    'sftp': export_via_sftp
}
