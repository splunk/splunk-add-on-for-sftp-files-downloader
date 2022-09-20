import os

import paramiko


class SFTP_Client:
    def __init__(self, logger, **kwargs):
        self._logger = logger
        self._ssh_server = kwargs["ssh_server"]
        self._username = kwargs["username"]
        self._password = kwargs["password"]
        self._port = kwargs["port"]
        self._key_file_path = kwargs["key_file_path"]
        self._ssh_server_known_hosts_path = kwargs["ssh_server_known_hosts_path"]
        self._server_file_path = kwargs["server_file_path"]
        self._burn_after_download = kwargs["burn_after_download"]
        self._destination_file_path = kwargs["destination_file_path"]

        if self._key_file_path:
            keyfileclass = SFTP_Client.keyfile_class_for_type(kwargs["key_file_type"])
            self._private_key = keyfileclass.from_private_key_file(self._key_file_path)
        else:
            self._private_key = None

    @staticmethod
    def keyfile_class_for_type(key_file_type):
        if key_file_type == "RSA":
            return paramiko.RSAKey
        elif key_file_type == "DSA":
            return paramiko.DSSKey

        raise TypeError(f"Unknown key_file_type: {key_file_type}")

    def get_remote_filenames(self, sftp):
        dirlist = sftp.listdir(self._server_file_path)
        for row in dirlist:
            yield row

    def download_files(self, sftp):
        for filename in self.get_remote_filenames(sftp):
            remote_file = os.path.join(self._server_file_path, filename)
            local_file = os.path.join(self._destination_file_path, filename)
            self._logger.log_info(f"Copying {remote_file} from sftp server!")
            # copy remote file to local
            sftp.get(remote_file, local_file)

            if self._burn_after_download:
                self._logger.log_info(f"Deleting {remote_file} from sftp server!")
                sftp.remove(remote_file)

    def process(self):
        # Connect to the SSH server
        with paramiko.client.SSHClient() as ssh:
            if self._ssh_server_known_hosts_path:
                ssh.load_host_keys(self._ssh_server_known_hosts_path)
            else:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(self._ssh_server, port=self._port, username=self._username,
                        password=self._password, pkey=self._private_key)

            # Connect to the SFTP server
            with ssh.open_sftp() as sftp:
                self._logger.log_debug(f"Connected to sftp server!")
                self.download_files(sftp)
