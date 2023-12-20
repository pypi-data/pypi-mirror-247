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

        with open(destination_dir+"/.env", "x") as File:
            File.write("""# -- Database Environment -- #
SERVER=localhost
DATABASE=example
USER_NAME=root
PASSWORD=


# -- Mail -- #
EMAIL=example@gmail.com
APP_PASSWORD=exampleToken


# -- Hosts & API Keys -- #
DOMAIN=api.example.com

# USER #
USER=user@${DOMAIN}
USER_API_KEY=exampleToken


# -- FTP API -- #
FTP_URL=https://api.example.com
FTP_BASE=/
FTP_HOST=1.1.1.1
FTP_USER=user@api.example.com
FTP_PASSWORD=password
LOCAL_BASE=../


# -- FTP WEB -- #
WEB_FTP_URL=https://example.com
WEB_FTP_BASE=/
WEB_FTP_HOST=1.1.1.1
WEB_FTP_USER=user@example.com
WEB_FTP_PASSWORD=password
WEB_LOCAL_BASE=C://path/to/local/web/""")
        print("SUCCESSFULLY CREATED API!")
    except Exception as e:
        raise Exception("CREATE FAILED:\n", e)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3 and args[1] == "create" and args[2] == "rest-api":
        create_rest_api()
    if len(args) == 4 and args[1] == "create" and args[2] == "rest-api":
        create_rest_api(args[3])
