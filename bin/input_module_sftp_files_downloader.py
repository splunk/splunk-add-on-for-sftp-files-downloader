
# encoding = utf-8

from sftp_client import SFTP_Client

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''


def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # username = definition.parameters.get('username', None)
    # password = definition.parameters.get('password', None)
    # burn_after_download = definition.parameters.get('burn_after_download', None)
    # ssh_server = definition.parameters.get('ssh_server', None)
    # port = definition.parameters.get('port', None)
    # key_file_path = definition.parameters.get('key_file_path', None)
    # key_file_type = definition.parameters.get('key_file_type', None)
    # server_file_path = definition.parameters.get('server_file_path', None)
    # ssh_server_known_hosts_path = definition.parameters.get('ssh_server_known_hosts_path', None)
    # destination_file_path = definition.parameters.get('destination_file_path', None)
    pass


def collect_events(helper, ew):
    configs = {
        "username": helper.get_arg("username"),
        "password": helper.get_arg("password"),
        "port": helper.get_arg("port"),
        "ssh_server": helper.get_arg("ssh_server"),
        "key_file_path": helper.get_arg("key_file_path"),
        "key_file_type": helper.get_arg("key_file_type"),
        "server_file_path": helper.get_arg("server_file_path"),
        "burn_after_download":  helper.get_arg("burn_after_download"),
        "destination_file_path": helper.get_arg("destination_file_path"),
        "ssh_server_known_hosts_path": helper.get_arg("ssh_server_known_hosts_path")
    }

    helper.log_debug("SFTP Files Downloader : Start processing...")

    sftpclient = SFTP_Client(helper, **configs)

    sftpclient.process()

    helper.log_debug("SFTP Files Downloader : Finished.")
