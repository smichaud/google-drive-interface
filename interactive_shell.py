import sys
from driveinterface import DriveInterface


# TODO: If no arg, terminal, else apply command directly
# TODO: Make it modal like vim, for instance if command tt==terminal and on gd==GoogleDrive ?
def main(argv):
    drive = DriveInterface()

    current_dir_id = 'root'
    while True:
        command = input(drive.get_file_path(current_dir_id) + " >>> ")

        if command == 'exit':
            break

        elif command == 'ls':
            drive.print_files(current_dir_id)

        elif command.startswith('cd '):
            new_dir = command.replace('cd ', '', 1)
            if new_dir == "..":
                parents = drive.get_file_by_id(current_dir_id)['parents']
                if parents:
                    current_dir_id = parents[0]['id']
            else:
                current_dir_id = drive.get_file_by_name(
                    new_dir, current_dir_id)

        elif command.startswith('rm '):
            rm_name = command.replace('rm ', '', 1)
            file_id = drive.get_file_by_name(rm_name, dir_id=current_dir_id)
            if file_id != current_dir_id:
                drive.get_file_by_id(file_id).Trash()

        elif command.startswith('mkdir '):
            dir_name = command.replace('mkdir ', '', 1)
            drive.create_dir(dir_name, current_dir_id)

        elif command.startswith('push '):
            filename = command.replace('push ', '', 1)
            drive.upload_file(filename)

        # TODO: This is a test, it dowloads as pdf
        elif command.startswith('pull '):
            filename = command.replace('pull ', '', 1)
            file_id = drive.get_file_by_name(filename, dir_id=current_dir_id)
            drive_file = drive.get_file_by_id(file_id)
            drive_file.GetContentFile(drive_file['title'] + '.pdf',
                                        mimetype='application/pdf')

        elif command.startswith('perm '):
            if command.startswith('perm print '):
                filename = command.replace('perm print ', '', 1)
                file_id = drive.get_file_by_name(filename,
                                                 dir_id=current_dir_id)
                drive.print_permissions(file_id)
            elif command.startswith('perm add '):
                # TODO: Implement the command management
                params = command.replace('perm add ', '', 1).split()
                file_id = drive.get_file_by_name(params[0],
                                                 dir_id=current_dir_id)
                email = params[1]
                drive.add_permission(file_id, value=email,
                                     ptype='user', role='writer')
            elif command.startswith('perm rm '):
                # TODO: Dont ask for user id, could be email for instance
                filename = command.replace('perm rm ', '', 1)
                params = command.replace('perm rm ', '', 1).split()
                file_id = drive.get_file_by_name(params[0],
                                                 dir_id=current_dir_id)
                user_id = params[1]
                drive.remove_permission(file_id, user_id)

        else:
            print("Command not recognized...")


if __name__ == '__main__':
    main(sys.argv[1:])
