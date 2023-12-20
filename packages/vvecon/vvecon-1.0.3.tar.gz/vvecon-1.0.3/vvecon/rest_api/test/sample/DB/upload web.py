import os
from ftplib import FTP
from dotenv import load_dotenv
from os import environ

load_dotenv("../.env")

# FTP server credentials and file information
FTP_URL = environ.get("WEB_FTP_URL")
FTP_BASE = environ.get("WEB_FTP_BASE")
FTP_HOST = environ.get("WEB_FTP_HOST")
FTP_USER = environ.get("WEB_FTP_USER")
FTP_PASSWORD = environ.get("WEB_FTP_PASSWORD")
LOCAL_BASE = environ.get("WEB_LOCAL_BASE")
FILES = ['.env', 'index.php']
FOLDERS = ['config', 'controller', 'core', 'model', 'paths', 'view', 'statics']

if __name__ == "__main__":
    try:

        print("CONNECTING")

        # Create an FTP connection
        ftp = FTP(FTP_HOST)

        # Login to the FTP server
        ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)

        print("CONNECTED TO THE SERVER")

        # Change the working directory (if needed)
        # ftp.cwd("/remote_directory")

        def create_remote_directory(remote_dir):
            try:
                ftp.cwd(remote_dir)
            except Exception:
                try:
                    print("MAKE NEW DIR", remote_dir)
                    ftp.mkd(remote_dir)
                except Exception:
                    print("FOLDER ALREADY EXISTS")


        def upload(path):
            # Open the local file in binary mode for uploading
            with open(LOCAL_BASE + path, "rb") as File:
                # Use the STOR command to upload the file
                ftp.storbinary("STOR " + FTP_BASE + path, File)


        print("UPLOADING FILES")
        for FILE in FILES:
            upload(FILE)


        def upload_folders(FOLDER):
            files = os.listdir(LOCAL_BASE + FOLDER)
            print("UPLOADING FILES ON " + FOLDER)
            for file in files:
                if "." in file:
                    print("UPLOADING", FOLDER + "/" + file)
                    upload(FOLDER + "/" + file)
                else:
                    create_remote_directory(FOLDER + "/" + file)
                    upload_folders(FOLDER + "/" + file)
            return None


        for FOLDER in FOLDERS:
            upload_folders(FOLDER)

        print("UPLOAD COMPLETED")
        # Close the FTP connection
        ftp.quit()

    except Exception as e:
        print("CONNECTION FAILED\nDUE TO\n", e)
