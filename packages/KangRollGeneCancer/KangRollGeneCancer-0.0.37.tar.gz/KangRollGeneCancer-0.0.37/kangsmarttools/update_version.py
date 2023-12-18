# -*- coding: utf-8 -*-
# update_version.py
#!/usr/bin/env python3



def update_version(filename='setup.py'):
    new_version = None
    with open(filename, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith('    version='):
            version_parts = line.split('"')
            version = version_parts[1]
            major, minor, patch = map(int, version.split('.'))
            new_version = f'{major}.{minor}.{patch + 1}'
            lines[i] = f'    version="{new_version}",\n'
            break

    with open(filename, 'w') as file:
        file.writelines(lines)

    return new_version # for github commit
 
if __name__ == '__main__':
    updated_version = update_version()
    if updated_version:
        print(f'Updated version to {updated_version}')
    else:
        print('Version update failed.')



# def update_version(filename='setup.py'):
#     with open(filename, 'r') as file:
#         lines = file.readlines()

#     for i, line in enumerate(lines):
#         if line.startswith('    version='):
#             version_parts = line.split('"')
#             version = version_parts[1]
#             major, minor, patch = map(int, version.split('.'))
#             new_version = f'{major}.{minor}.{patch + 1}'  # 注意这里的空格
#             lines[i] = f'    version="{new_version}",\n'
#             # lines[i] = f'    version="{new_version}",\n'
#             break

#             break

#     with open(filename, 'w') as file:
#         file.writelines(lines)
#     print(f'Updated version to {new_version}')

# if __name__ == '__main__':
#     update_version()

