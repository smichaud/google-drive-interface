from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class DriveInterface():
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self._drive = GoogleDrive(gauth)


    def print_files(self, dir_id):
        for f in self.get_files_list(dir_id):
            filetype = '[F] '
            if f['mimeType'] == "application/vnd.google-apps.folder":
                filetype = "[D] "
            print(filetype + f['title'])


    def get_files_list(self, dir_id):
        request = {'q': "'{}' in parents and trashed=false".format(dir_id)}
        return self._drive.ListFile(request).GetList()


    def get_file_by_id(self, id):
        return self._drive.CreateFile({'id': id})


    # TODO: Adapt: for now, it gets the first file that starts with the filename
    def get_file_by_name(self, filename, dir_id='root'):
        files_list = self.get_files_list(dir_id)
        for f in files_list:
            if f['title'].startswith(filename):
                return f['id']

        return dir_id


    def create_dir(self, filename, parent_id='root'):
        new_dir = self._drive.CreateFile({
            'title': filename,
            'parents':  [{"id": parent_id}],
            'mimeType': "application/vnd.google-apps.folder"
        })
        new_dir.Upload()

        return new_dir['id']


    def recursive_dir_copy(self, src_id, dst_id):
        files = self.get_files_list(src_id)
        for f in files:
            if f['mimeType'] == "application/vnd.google-apps.folder":
                current_dir = self.create_dir(f['title'], dst_id)
                self.recursive_dir_copy(f['id'], current_dir)


    def get_file_path(self, id):
        path = ""
        current_file = self.get_file_by_id(id)
        while current_file['parents']:
            path = current_file['title'] + "/" + path
            current_file = self.get_file_by_id(current_file['parents'][0]['id'])

        return "/" + path


    def download_file(self, drive_file):
        drive_file = self._drive.CreateFile({'id': drive_file['id']})
        drive_file.GetContentFile(drive_file['title'])


    def upload_file(self, filename, parent_id='root'):
        file_to_upload = self._drive.CreateFile({'parent': parent_id})
        file_to_upload.SetContentFile(filename)
        file_to_upload.Upload()


    def print_permissions(self, file_id):
        f = self.get_file_by_id(file_id)
        permissions = f.GetPermissions()
        for p in permissions:
            print("======================")
            print(p)


    def add_permission(self, file_id, value, ptype='user', role='writer'):
        f = self.get_file_by_id(file_id)
        f.InsertPermission({
            'type': ptype, # user, group, domain, anyone
            'value': value, # email address or domain name for the entity
            'role': role # organizer, owner, reader, writer
        })


    def remove_permission(self, file_id, user_id):
        f = self.get_file_by_id(file_id)
        f.DeletePermission(user_id)
