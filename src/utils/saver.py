import PyPDF2
from io import BytesIO

import pdf2image


# using /tmp directory storage 512 MB to store assets

def decrypt_pdfblob_save(file_blob, password, output_file):
    print("Initiating file decryption")
    try:
        reader = PyPDF2.PdfFileReader(BytesIO(file_blob))

        if reader.isEncrypted and password is not None:
            reader.decrypt(password)
            print('File Decrypted (PyPDF2)')

            writer = PyPDF2.PdfFileWriter()
            for i in range(reader.getNumPages()):
                writer.addPage(reader.getPage(i))

            writer.write(output_file)

            print("File Saved")

        else:
            print('File already Decrypted')
            output_file.write(file_blob)
            print("File Saved")

    except Exception as err:
        print(err, '\n decrypt library problem \n')
        return None


def pdf_to_img_save(pdf_file, img_file):
    print("Initiating pdf to image conversion")
    pages = pdf2image.convert_from_bytes(pdf_file.read(), poppler_path='/opt/bin/poppler')
    # pages = pdf2image.convert_from_bytes(pdf_file.read())
    for page in pages:
        page.save(img_file, 'JPEG')
        print("File Saved")

    # page.save image file m convert nhi kr pa ra isse dekh
