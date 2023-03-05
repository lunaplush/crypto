import zipfile
import os

class Zipper():

    def __init__(self) -> None:
        pass


    @staticmethod
    def zipFolder(src_folder, dst_folder, zip_filename, internal_folder = ''):
        try:
            path_to_zipfile = os.path.join(dst_folder, zip_filename)
            zf = zipfile.ZipFile(path_to_zipfile, 'w')

            for folder, subfolders, files in os.walk(src_folder):
                # print(folder, subfolders, files)
                for file in files:
                    zf.write(
                        os.path.join(folder, file),
                        os.path.join(internal_folder, os.path.relpath(os.path.join(folder, file), src_folder)),
                        compress_type=zipfile.ZIP_DEFLATED
                    )
            zf.close()
            print(f'Zip file {zip_filename} has been created')
        except Exception as e:
            print(e)


    @staticmethod
    def addToArchive(path_to_zipfile, src_folder, filelist = [], internal_folder = ''):
        try:
            zf = zipfile.ZipFile(path_to_zipfile, 'a', compression=zipfile.ZIP_DEFLATED)
            if len(filelist) == 0:
                            for folder, subfolders, files in os.walk(src_folder):
                                # print(folder, subfolders, files)
                                for file in files:
                                    zf.write(
                                        os.path.join(folder, file),
                                        os.path.join(internal_folder, os.path.relpath(os.path.join(folder, file), src_folder))
                                    )
            else:
                for filename in filelist:
                    zf.write(
                        os.path.join(src_folder, filename),
                        os.path.join(internal_folder, os.path.relpath(os.path.join(src_folder, filename), src_folder))
                    )

            zf.close()
            print(f'Files have been added to archive')

        except Exception as e:
            print(e)

    
    @staticmethod
    def addFileToArchiveFromVariable(path_to_zipfile, filename, filedata, internal_folder = ''):
        try:
            zf = zipfile.ZipFile(path_to_zipfile, 'a', compression=zipfile.ZIP_DEFLATED)
            zf.writestr(
                 os.path.join(internal_folder, filename),
                 filedata
            )
            zf.close()
            print(f'Data have been adder via file {filename} to the archive')

        except Exception as e:
            print(e)


    @staticmethod
    def unzip(path_to_zipfile, dst_folder):
        try:
            zf = zipfile.ZipFile(path_to_zipfile, 'r')
            zf.extractall(dst_folder)
            zf.close()
            print(f'Archive was unziped')
        except Exception as e:
             print(e)