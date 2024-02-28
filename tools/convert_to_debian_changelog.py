import re, sys

def extract_info(s):
    pattern = r"(\w{3} \w{3} \d{2} \d{4}) (.*?) <(.*?)>"
    match = re.search(pattern, s)
    if match:
        return {"date": match.group(1), "name": match.group(2), "email": match.group(3)}
    else:
        return None

def convert_rpm_changelog_to_debian(rpm_changelog, package_name):
    debian_changelog = ""
    isert_at = 0
    lines = rpm_changelog.split('\n')
    for line in lines:
        if line.startswith('* '):
            info = extract_info(line[2:])
            debian_changelog += package_name + ' (' + line[2:].split(' ')[-1] + ') ' + 'unstable; urgency=medium' + '\n'
            insert_at = len(debian_changelog)
            debian_changelog += f'-- {info["name"]} {info["email"]} {info["date"]} \n'
        elif line.startswith('- '):
            debian_changelog = debian_changelog[:insert_at] + '  ' + line[2:] + '\n' + debian_changelog[insert_at:]
            insert_at = len('  ' + line[2:] + '\n')
        elif line.startswith('  '):
            debian_changelog = debian_changelog[:insert_at] + '    ' + line[2:] + '\n' + debian_changelog[insert_at:]
            insert_at = len('    ' + line[2:] + '\n')
        else:
            debian_changelog += line + '\n'
    return debian_changelog


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <package name>")
        sys.exit(1)

    package_name = sys.argv[2]

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            rpm_changelog = file.read()
    except IOError:
        print("Error: File does not appear to exist.")
        sys.exit(1)

    print(convert_rpm_changelog_to_debian(rpm_changelog, package_name))
