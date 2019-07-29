import os
import sys

from easycli import Root, SubCommand, Argument
from .linuxcp import recursive_copy, copyfile


class CP(Root):
    __help__ = 'easycli example'
    __command__ = 'cp'
    __completion__ = False
    __arguments__ = [
        Argument(
            'files',
            nargs='*',
            metavar='N',
            type=str,
            help='source path'
        ),
        Argument(
            '-r', '--recursive',
            action='store_true',
            help='copy directories recursively'
        ),
        Argument(
            '-v', '--verbose',
            help='explain what is being done',
            action='store_true',
        ),
    ]

    def _split_source_destination(self, args):
        if len(args.files) < 2:
            print('Source or destination is not entered')
            sys.exit()
        sources = args.files[:-1]
        destination = args.files[-1]
        return sources, destination

    def __call__(self, args):
        sources, destination = self._split_source_destination(args)
        current_dir = os.getcwd()
        for source_file in sources:

            if '/' in source_file[:-1]:
                source_path = source_file
                os.chdir(source_file[:source_file.rindex('/')])
                file_name = source_file[source_file.rindex('/')+1:]

            else:
                source_path = current_dir + '/' + source_file
                file_name = source_file

            if not (
                os.path.exists(source_path) or os.path.isfile(source_path)
            ):
                print(
                    f"cp: cannot stat '{source_path}':"\
                    "No such file or directory"
                )

            if os.path.isdir(source_path):

                if not args.recursive:
                    destination = os.path.abspath(destination)
                    destination = destination.split('/')[-1]
                    print(
                        f"cp: -r not specified;"\
                        "omitting directory {destination!r}"
                    )
                    sys.exit()

                else:
                    source = os.path.abspath(source_path)
                    destination = os.path.abspath(destination)

                    if '/' not in source[-1] or '/' not in source:
                        top = destination + '/' + source[source.rindex('/')+1:]

                    else:
                        top = destination + '/' + source

                    if not os.path.isdir(destination):
                        os.mkdir(destination)

                    if source == top:

                        if '/' in destination:
                            print(
                                f"cp: '{source_path}' and ./'{destination}'"
                                "are the same file"
                            )

                        else:
                            print(
                                f"cp: '{source_path}' and '{destination}'"
                                "are the same file"
                            )
                        sys.exit()
                    if os.path.exists(top):

                        for root, dirs, files in os.walk(top, topdown=False):

                            for name in files:
                                os.remove(os.path.join(root, name))

                            for name in dirs:
                                os.rmdir(os.path.join(root, name))
                        os.rmdir(top)

                    recursive_copy(source, destination, args.verbose)

            elif os.path.isfile(source_path):
                source = source_path
                destination = destination

                if not(os.path.exists(source)):
                    print(
                        f"cp: cannot stat '{source_path}':"
                        "No such file or directory"
                    )

                if not os.path.isdir(destination):
                    os.mkdir(destination)

                if destination == "":
                    print(
                        f"cp: missing destination file operand after "
                        "'{destination}'"
                    )

                if os.path.isdir(source):
                    print(
                        f"cp: -r not specified;"\
                        "omitting directory '{source_path}'"
                    )
                copyfile(source, destination, args.verbose)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        CP().main(['-h'])

    else:
        CP().main()

