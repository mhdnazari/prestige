import os
import sys
import stat


def copyfile(file_path, target_dir, verbose=False):
    if '/' == file_path[-1] or '/' in file_path:

        source_path = file_path
        os.chdir(file_path[:file_path.rindex('/')])
        file_name = file_path[file_path.rindex('/')+1:]

    else:
        source_path = os.getcwd() + '/' + file_path
        file_name = file_path

    target_path = target_dir + file_name

    if not os.access(file_name, os.R_OK):
        if sys.argv[1] !='-f':
            print ("permission denied")
            sys.exit()
        else:
            acc_mode = os.stat(file_name)
            os.chmod(file_name, acc_mode.st_mode | stat.S_IREAD)

    file_pointer = open(file_name, 'rb')
    temp_file = file_pointer.read()
    file_pointer.close()
    os.chdir(target_dir)
    file_pointer = open(file_name, 'wb')
    file_pointer.write(temp_file)
    file_pointer.close()

    source_abs = os.path.abspath(source_path)
    source_abs = source_abs.split('/')[-1]
    destination_abs = os.path.abspath(target_path)


    if verbose:
        print(f'{source_abs!r} -> {target_path!r}')

def recursive_copy(source_dir, target_dir, verbose=False):
    if not (os.access(source_dir, os.X_OK) and os.access(source_dir, os.R_OK)):
        if 'f' not in sys.argv[1]:
            print ("permission denied")
            sys.exit()
        else:
            acc_mode = os.stat(source_dir)
            os.chmod(source_dir, acc_mode.st_mode | stat.S_IXUSR)
            os.chmod(source_dir, acc_mode.st_mode | stat.S_IREAD)
    os.chdir(target_dir)
    os.makedirs(source_dir[source_dir.rindex('/')+1:])
    target_dir2 = target_dir +'/'+ source_dir[source_dir.rindex('/')+1:]
    wlk = os.walk(source_dir)
    root, dirnames, filenames = next(wlk)
    for new_file in filenames:

        os.chdir(source_dir)
        if not os.access(new_file, os.R_OK):
            if 'f' not in sys.argv[1]:
                print ("permission denied")
                sys.exit()
            else:
                acc_mode = os.stat(new_file)
                os.chmod(new_file, acc_mode.st_mode | stat.S_IREAD)

        file_pointer = open(root+'/'+new_file, 'rb')
        temp_file = file_pointer.read()
        file_pointer.close()
        os.chdir(target_dir2)
        file_pointer =open(new_file, 'wb')
        file_pointer.write(temp_file)
        file_pointer.close()

        if verbose:
            source_path = source_dir + '/' + new_file
            target_path = target_dir2 + '/' + new_file
            print(f'{source_path!r} -> {target_path!r}')

    for new_dir in dirnames:
        recursive_copy(root + '/' + new_dir, target_dir2, verbose)

if __name__ == "__main__":
    CP.main()

