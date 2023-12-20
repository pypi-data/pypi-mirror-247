from datetime import datetime
from ftplib import FTP
from dotenv import load_dotenv
from os import environ

load_dotenv("../.env")

# FTP server credentials and file information
FTP_URL = environ.get("FTP_URL")
FTP_BASE = environ.get("FTP_BASE")
FTP_HOST = environ.get("FTP_HOST")
FTP_USER = environ.get("FTP_USER")
FTP_PASSWORD = environ.get("FTP_PASSWORD")
LOCAL_BASE = environ.get("LOCAL_BASE")
FILES = ['tmp/restart.txt']

if __name__ == "__main__":
    try:

        print("CONNECTING")

        # Create an FTP connection
        ftp = FTP(FTP_HOST)

        # Login to the FTP server
        ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)

        print("CONNECTED TO THE SERVER")


        def upload(path):
            try:
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_content = f"Uploaded at {current_time}"

                temp_file_path = f"{LOCAL_BASE}{path}"
                with open(temp_file_path, "w") as temp_file:
                    temp_file.write(file_content)

                ftp.storbinary("STOR " + FTP_BASE + path, open(temp_file_path, "rb"))

            except Exception as err:
                print(f"Upload failed for {path} due to:\n{err}")


        print("RESTARTING")
        for FILE in FILES:
            upload(FILE)

        print("RESTART COMPLETED")
        # Close the FTP connection
        ftp.quit()

    except Exception as e:
        print("RESTART FAILED\nDUE TO\n", e)
