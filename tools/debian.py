import re
import os
import sys
import urllib.request
import tarfile
import logging
import subprocess

from shutil import copytree

class DebianPackage(object):
    def __init__(self, path):
        self.build_path = os.path.join(path, "build")
        self.package_path = path

        self.package_url = None
        self.tar_archive = None

        self.read_package_url()
        self.read_changelog()

    def read_package_url(self):
        url_file = os.path.join(self.package_path, "package_url")

        if not os.path.exists(url_file):
            print("Unable to find file {}".format(url_file))
        else:
            with open(url_file) as f:
                self.package_url = f.read().strip()
                print('Got package_url {}'.format(self.package_url))

    def read_changelog(self):
        line = ''
        with open(os.path.join(self.package_path, 'debian', 'changelog'), 'r', encoding='utf-8') as file:
            line = file.readline()
        matches = re.match(r"(.+) \((.+)\)", line)

        name = matches.group(1)
        version = matches.group(2)

        archive_suffix = 'bz2'
        if self.package_url.endswith('gz'):
            archive_suffix = 'gz'
        self.tar_archive = os.path.join(self.package_path, '{}-{}.orig.tar.{}'.format(name, version, archive_suffix))
        print('Got archive path {}'.format(self.tar_archive))

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
        if os.path.exists(self.build_path):
            return

        os.mkdir(self.build_path)

    def __fetch_tarball(self):
        urllib.request.urlretrieve(self.package_url, self.tar_archive)

    def __extract_tarball(self):
        retcode = subprocess.call(['tar', '-xvf', self.tar_archive, '-C', self.build_path, '--strip-components=1'])
        if retcode == 0:
            print("Extracted successfully")
        else:
            raise IOError('tar exited with code %d' % retcode)

    def __copy_debian(self):
        source_dir = os.path.join(self.package_path, "debian")
        target_dir = os.path.join(self.build_path, "debian")
        copytree(source_dir ,target_dir)

    def __build(self):
        retcode = subprocess.call(['dpkg-buildpackage', '-us', '-uc'], cwd=self.build_path)
        if retcode == 0:
            print("Build successful")
        else:
            raise IOError('dpkg-buildpackage exited with code %d' % retcode)

def main():
    if len(sys.argv) != 2:
        print("Usage: {} <package_path>".format(sys.argv[0]))
        return

    path = sys.argv[1]

    if not os.path.exists(path):
        print("Given path {} is invalid!".format(path))

    if not os.path.exists(os.path.join(path, "debian")):
        print("There is no debian folder in given path!")
        return

    package = DebianPackage(path)
    sys.exit(package.build_package())

if __name__ == "__main__":
    main()
