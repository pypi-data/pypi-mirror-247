import os
import sys


def create_rest_api(name: str = False):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        destination_dir = os.getcwd()
        if name:
            destination_dir += "/" + name
            if not os.path.exists(destination_dir):
                try:
                    os.mkdir(destination_dir)
                except FileExistsError:
                    print("FOLDER ALREADY EXISTS")

        def copy_file(file):
            print("CREATING", destination_dir + "/" + file[len(current_dir + "/rest_api/test/sample/"):])
            with open(file, 'rb') as File:
                with open(destination_dir + "/" + file[len(current_dir + "/rest_api/test/sample/"):], 'x'):
                    pass
                with open(destination_dir + "/" + file[len(current_dir + "/rest_api/test/sample/"):], 'wb') as newFile:
                    newFile.write(File.read())

        def copy_folders(folder):
            files = os.listdir(folder)
            for file in files:
                if "." in file:
                    copy_file(folder + "/" + file)
                else:
                    try:
                        print("CREATING FOLDER", destination_dir + "/" + (
                            folder + "/" + file)[len(current_dir + "/rest_api/test/sample/"):]
                        )
                        os.mkdir(destination_dir + "/" + (folder + "/" + file)[
                                                         len(current_dir + "/rest_api/test/sample/"):
                        ])
                    except FileExistsError:
                        pass
                    copy_folders(folder + "/" + file)
            return None

        cdir = current_dir + "/rest_api/test/sample"
        print("WORKING DIRECTORY", cdir)
        copy_folders(cdir)
        print("SUCCESSFULLY CREATED API!")
    except Exception as e:
        raise Exception("CREATE FAILED:\n", e)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3 and args[1] == "create" and args[2] == "rest-api":
        create_rest_api()
    if len(args) == 4 and args[1] == "create" and args[2] == "rest-api":
        create_rest_api(args[3])
