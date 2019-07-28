import os
import sys

from easycli import Root, SubCommand, Argument
from .linuxcp import recursive_copy, copyfile


class CP(Root):
    __help__ = 'easycli example'
    __command__ = 'cp'
    __completion__ = True
    __arguments__ = [
#        Argument(
#            '-V', '--version',
#            action='version',
#            version='CP 1.0',
#        ),
        Argument(
            '-r', '--recursive',
            action='store_true',
            help='copy directories recursively'
        ),
        Argument(
            '-v', '--verbose',
            help='asdf',
            action='store_true',
        ),
        Argument(
            'source',
            help='source path'
        ),
        Argument(
            'destination',
            help='destination path'
        ),
    ]

    def __call__(self, args):
        if not (os.path.exists(args.source) or os.path.isfile(args.source)):
            print(
                f"cp: cannot stat '{args.source}': No such file or directory"
            )

        if os.path.isdir(args.source):
            if not args.recursive:
                destination = os.path.abspath(args.destination)
                destination = destination.split('/')[-1]
                print(
                    f"cp: -r not specified; omitting directory {destination!r}"
                )
                sys.exit()
            else:
                source = os.path.abspath(args.source)
                destination = os.path.abspath(args.destination)
                if '/' not in source[-1] or '/' not in source:
                    top = destination + '/' + source[source.rindex('/')+1:]

                else:
                    top = destination + '/' + source

                if not os.path.isdir(args.destination):
                    os.mkdir(args.destination)

                if source == top:
                    if '/' in destination:
                        print(
                            f"cp: '{args.source}' and ./'{destination}'"
                            "are the same file"
                        )
                    else:
                        print(
                            f"cp: '{args.source}' and '{args.destination}'"
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

        elif os.path.isfile(args.source):
            source = args.source
            destination = args.destination
            if not(os.path.exists(source)):
                print(
                    f"cp: cannot stat '{args.source}':"
                    "No such file or directory"
                )
            if not os.path.isdir(args.destination):
                os.mkdir(args.destination)
            if destination == "":
                print(
                    f"cp: missing destination file operand after "
                    "'{args.destination}'"
                )
            if os.path.isdir(source):
                print(
                    f"cp: -r not specified; omitting directory '{args.source}'"
                )

            copyfile(source, destination, args.verbose)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        CP().main(['-h'])

    else:
        CP().main()

