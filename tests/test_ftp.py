import unittest
from mock import patch, mock_open, MagicMock
from myftp.myftp import export_factory

class TestFTP(unittest.TestCase):
    """docstring for TestFTP."""

    @patch('myftp.myftp.FTP', autospec=True)
    def test_ftp(self, mocked_ftp):
        mocked_file = MagicMock()
        ftp = export_factory('ftp')
        ftp(
            local_obj_file=mocked_file,
            file_name='foo',
            host='localhost',
            user='user',
            password='dev',
            destination='/tmp')
        # Why I used this something.return_value way:
        # When you use 'with something as s' you put the return of something
        # on s, so when you are mocking you need to get the return of it
        # and call the method that you want to assert.
        mocked_ftp.return_value.cwd.assert_called_once_with('/tmp')
        mocked_ftp.return_value.storbinary.assert_called_once_with(
            'STOR foo', mocked_file)

    @patch('myftp.myftp.SSHClient', autospec=True)
    def test_sftp(self, mock_ssh):
        mock_client = MagicMock()
        mock_ssh.return_value = mock_client
        sftp = export_factory('sftp')

        mock_file = MagicMock()
        sftp(
            local_file=mock_file,
            file_name='foo',
            host='localhost',
            port='22',
            user='user',
            password='dev',
            destination='/tmp')

        mock_client.connect.assert_called_once_with(
            hostname='localhost',
                password='dev',
                port=22,
                username='user')

        mock_client.open_sftp.return_value.putfo.assert_called_once_with(
            mock_file,
            '/tmp/foo'
        )
