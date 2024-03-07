import os
import sys
import urllib.request
import tarfile

from subprocess import Popen

class DebianPackage(object):
    def __init__(self, path):
        self.build_path = None
        self.package_path = path

        self.package_url = None
        self.tar_archive = None
        self.archive_dir = None

        self.read_package_url()
        self.read_changelog()

    def read_package_url(self):
        url_file = os.path.join(self.package_path, "package_url")

        if not os.exists(url_file):
            print(f"Unable to find file {file}", url_file)
        else:
            with open(url_file) as f:
                self.package_url = f.read().trim()
                close(url_file)

    def read_changelog(self):
        pass

    def build_package(self):
        if not self.tar_archive:
            return False

        self.__create_build_dir()
        if self.package_url:
            self.__fetch_tarball()
            self.__extract_tarball()
        self.__copy_debian()
        return self.__build()

    def __create_build_dir(self):
        if os.exists(self.build_path):
            return

        os.mkdir(self.build_path)

    def __fetch_tarball(self):
        pass

    def __extract_tarball(self):
        tar = tarfile.open(os.path.join(self.package_path ,self.tar_archive))
        tar.extractall()
        tar.close()

    def __copy_debian(self):
        pass

    def __build(self):
        builder = "dpkg-buildpackage -us -uc";

        p = Popen(builder, self.archive_dir)
        return p.wait()

def main():
    if sys.argc < 2:
        print("Usage: {1} <package_path>".format(sys.argv[0]))
        return

    path = sys.argv[1]

    if not os.path.exists(path):
        print("Given path {1} is invalid!".format(path))

    if not os.path.exists(os.path.join(path, "debian")):
        print("There is no debian folder in given path!")
        return

    package = DebianPackage(path)
    sys.exit(package.build_package())

if __name__ == "__main__":
    main()
