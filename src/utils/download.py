import requests


def download_from_url(file_url):
    print("Initiating file download")
    try:
        response = requests.get(file_url)
        print("Download complete")
        return response.content, response.headers['Content-Type']
    except Exception as err:
        print(err, '\n Encrypted file download problem \n')
        return None, None
