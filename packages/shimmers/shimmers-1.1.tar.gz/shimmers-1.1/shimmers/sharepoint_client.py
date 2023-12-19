import csv
import posixpath
from collections import OrderedDict
from io import BytesIO, TextIOWrapper
import logging
from .version_info import version


log = logging.getLogger(__name__)


class Sharepoint:
    def __init__(self, conf=None, site_name=None, tenant_name=None,
                 tenant_id=None, client_id=None, key=None, thumbprint=None):
        self.tenant_name = tenant_name
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.key = key
        self.thumbprint = thumbprint
        self.site_name = site_name
        if conf:
            self.tenant_name = self.tenant_name or conf.tenant_name
            self.tenant_id = self.tenant_id or conf.tenant_id
            self.client_id = self.client_id or conf.client_id
            self.key = self.key or conf.key
            self.thumbprint = self.thumbprint or conf.thumbprint
            self.site_name = self.site_name or conf.site_name
        self.session = None

    def connect(self, force=False):
        """
        connects to office 365 and sets up the session.  If a session
        already exists, we reuse that session.  To force the creation
        of a new session, set force=True.

        Args:

            force (bool): set this flag to True if you want to force
                          return a fresh session.
        """
        from msal import ConfidentialClientApplication
        from office365.runtime.auth.token_response import TokenResponse
        from office365.sharepoint.client_context import ClientContext
        if self.session and not force:
            return self.session
        sharepoint_base_url = f'https://{self.tenant_name}.sharepoint.com'
        site_url = f'{sharepoint_base_url}/sites/{self.site_name}'
        authority = f'https://login.microsoftonline.com/{self.tenant_id}'
        app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential={
                'private_key': self.key,
                'thumbprint': self.thumbprint,
            },
            authority=authority,
            app_name='shimmers',
            app_version=version,

        )
        token_json = app.acquire_token_for_client(
            scopes=[ f'{sharepoint_base_url}/.default' ],
        )
        self.session = ClientContext(site_url).with_access_token(
            lambda: TokenResponse.from_json(token_json)
        )
        return self.session

    def ensure(self, d):
        """
        ensures that d exists
        """
        from office365.sharepoint.folders.folder import Folder
        session = self.connect()
        pieces = d.split(posixpath.sep)[3:]
        s: Folder = session.web.root_folder
        s = s.expand(['Folders'])
        for x in pieces:
            found = False
            s = s.get().execute_query()
            for y in s.folders:
                if y.name == x:
                    found = True
                    s = y
                    break
            if not found:
                log.info('creating folder %s in %s', x, s.serverRelativeUrl)
                s = s.folders.ensure_path(x).execute_query()
        return s

    def upload(self, buff, destination, retry_401=True):
        """
        uploads a BytesIO to the destination path
        Args:
            buff (BytesIO): the data to upload
            destination (str): the location in sharepoint where the file will
                               be stored
            retry_401 (bool): defaults to true.  If specified as true,
                              and we receive a 401 error from the download
                              operation, we will retry exactly once
                              to see if refreshing the token overcomes the 401
                              error
        """
        from office365.sharepoint.folders.folder import Folder
        from office365.runtime.client_request_exception import ClientRequestException
        destination = self.make_relative(destination)
        base = posixpath.basename(destination)
        destination = posixpath.dirname(destination)
        folder: Folder = self.ensure(destination)
        buff.seek(0)
        log.info(f'uploading %s => %s', base, destination)
        try:
            folder.upload_file(base, buff.getvalue()).execute_query()
        except ClientRequestException as ex:  # pragma: no cover
            if ex.response.status_code == 401 and retry_401:
                # we can get a 401 when our token expires, set
                # session to None here so that we reconnect on the
                # retry
                self.session = None
                return self.upload(buff, destination, False)
            raise

    def make_relative(self, path):
        pieces = []
        for x in path.split(posixpath.sep):
            if x == 'Documents':
                pieces.append('Shared Documents')
            else:
                pieces.append(x)
        return posixpath.join('/sites', self.site_name, *pieces)

    def get_folder(self, name, load_folders=False, load_files=False):
        """
        loads a folder from the sharepoint site.  Name should be relative
        to the site, e.g., Documents/folder1/folder2
        """
        from office365.sharepoint.folders.folder import Folder
        session = self.connect()
        path = self.make_relative(name)
        folder: Folder = session.web.get_folder_by_server_relative_url(path)
        expansions = []
        if load_folders:
            expansions.append('Folders')
        if load_files:
            expansions.append('Files/ListItemAllFields/FieldValuesAsText')
        if expansions:
            folder.expand(expansions)
        folder.get()
        folder.execute_query()
        return folder

    @classmethod
    def expand_folder(cls, f):
        expansions = ['Folders', 'Files/ListItemAllFields/FieldValuesAsText']
        f.expand(expansions)
        f.get()
        f.execute_query()
        return f

    def yield_files(self, name_or_folder):
        """
        yields all files from a folder and all of its subfolders
        """
        if isinstance(name_or_folder, str):
            f = self.get_folder(name_or_folder, True, True)
        else:
            f = self.expand_folder(name_or_folder)
        for x in f.files:
            yield x
        for folder in f.folders:
            yield from self.yield_files(folder)

    def download(self, filename, retry_401=True):
        """
        Downloads the specified path into a BytesIO buffer

        Args:
            filename (str): the name of the file to download
            retry_401 (bool): defaults to true.  If specified as true,
                              and we receive a 401 error from the download
                              operation, we will retry exactly once
                              to see if refreshing the token overcomes the 401
                              error
        """
        from office365.runtime.client_request_exception import ClientRequestException
        source = self.make_relative(filename)
        session = self.connect()
        f = session.web.get_file_by_server_relative_path(source)
        log.info('downloading %s from %s', filename, self.site_name)
        buff = BytesIO()
        try:
            f.download(buff).execute_query()
        except ClientRequestException as ex:  # pragma: no cover
            if ex.response.status_code == 401 and retry_401:
                # we can get a 401 when our token expires, set
                # session to None here so that we reconnect on the
                # retry
                self.session = None
                return self.download(filename, False)
            raise
        buff.seek(0)
        return buff

    def upload_dataframes(self, filename, *args, index=False, **kwargs):
        """
        provide arguments as filename, df1, sheet_name1, df2, sheet_name2, ...
        """
        import pandas as pd
        n = len(args)
        buff = BytesIO()
        with pd.ExcelWriter(buff) as f:
            for x in range(0, n, 2):
                df = args[x]
                sheet_name = args[x + 1]
                df.to_excel(f, sheet_name=sheet_name, index=index)
        self.upload(buff, filename)

    def upload_dataframe_csv(self, filename, df, **kwargs):
        """
        provide arguments as filename, df.  kwargs will be passed through
        to the dataframe `to_csv` function.
        """
        buff = BytesIO()
        df.to_csv(buff, **kwargs)
        self.upload(buff, filename)

    def download_dataframe(self, filename, engine='openpyxl', **kwargs):
        """
        downloads the file from sharepoint and provides it to the caller
        as a dataframe
        """
        import pandas as pd
        buff = self.download(filename)
        df = pd.read_excel(io=buff, **kwargs)
        return df

    def download_csv_raw(self, filename, strip=True, encodings=None, **kwargs):
        """
        parses the csv and tries to parse the csv using the specified encodings
        if no encodings are provided, we try the encodings in the following order:

        * utf-8-sig
        * cp1252
        * utf-8
        * cp437

        use the strip flag to specify whether column headings and row values
        should be stripped of any leading or trailing spaces
        """
        buff = self.download(filename)
        encodings = encodings or [ 'utf-8-sig', 'cp1252', 'utf-8', 'cp437', ]
        for encoding in encodings:
            buff.seek(0)
            f = TextIOWrapper(buff, encoding=encoding)
            try:
                reader = csv.reader(f, **kwargs)
                header = [ x.lower() for x in next(reader) ]
                if strip:
                    header = [ x.strip() for x in header ]
                rows = []
                for row in reader:
                    if strip:
                        row = [ x.strip() for x in row ]
                    rows.append(OrderedDict(zip(header, row)))
                return header, rows
            except Exception as ex:  # noqa, pylint: disable=bare-except
                f.detach()
        raise IOError(f'Could not parse the csv with any '
                      f'of the following encodings: {", ".join(encodings)}')

    def download_csv(self, filename, strip=True, encodings=None, **kwargs):
        """
        downloads the csv from sharepoint as a dataframe
        """
        from pandas import DataFrame
        _, rows = self.download_csv_raw(filename, strip, encodings, **kwargs)
        return DataFrame(rows)
