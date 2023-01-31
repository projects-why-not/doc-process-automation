import easywebdav
from requests.exceptions import ConnectionError

easywebdav.basestring = str
easywebdav.client.basestring = str


class YandexDiskProvider:
    def __init__(self):
        self._server = None

    def login(self, username, password):
        try:
            webdav = easywebdav.connect('webdav.yandex.ru',
                                        username=username,
                                        password=password,
                                        protocol='https',
                                        port=443)
            webdav.ls("/")
            self._server = webdav
        except ConnectionError:
            raise Exception("Failed to establish connection! Check your network")
        except easywebdav.OperationFailed:
            raise Exception("Wrong username or password!")
        except Exception as e:
            raise e

        return self

    def download(self, remote_fpath, local_fpath):
        self._server.download(remote_fpath,
                              local_fpath)

    def upload(self, local_fpath, remote_fpath):
        self._server.upload(local_fpath,
                            remote_fpath)

    def mkdir(self, remote_path):
        self._server.mkdir(remote_path)

    def list(self, path):
        if type(path) is tuple:
            path = path[0]
        return [f.name for f in self._server.ls(path)]
