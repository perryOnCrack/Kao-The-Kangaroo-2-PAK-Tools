import sys
import os
import math

def NewFolder(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print('Directory ' + path + ' exists.')

chunk_size = 128

open_path = sys.argv[1].replace('\\', '/')
open_dir = open_path.rsplit('/', 1)[0]
if open_dir == open_path:
    open_dir = ''
else:
    open_dir += '/'

with open(open_path, 'rb') as f:
    # Pak file header chunk.
    chunk = f.read(chunk_size)
    folder_path = chunk[16:64].decode('ascii').rstrip('\0')
    print(folder_path)

    # Each files and its table.
    end_of_file_reached = False
    while not end_of_file_reached:
        # Info of the file.
        # Get size and path/file name here.
        while True:
            chunk = f.read(chunk_size)
            # Reach end of file.
            if chunk == bytes(b''):
                print('EOF reached')
                end_of_file_reached = True
                break

            # Find one item.
            if chunk[0:4].decode('ascii') == 'item':
                # Get file size.
                size = int.from_bytes(chunk[4:8], 'little')
                # Get file path + name.
                file_path = chunk[16:].decode('ascii').rstrip('\0')
                file_path = file_path.replace('\\', '/') # Replace '\' with '/'
                
                print(file_path)
                print(str(size) + ' bytes')
                
                # Get the string used in open().
                full_path = open_dir + folder_path + '/' + file_path

                # Create a folder for the file.
                NewFolder(full_path.rsplit('/', 1)[0])

                # Calculate number of chunks to read.
                num_of_chunk = math.ceil(size / chunk_size)
                with open(full_path, 'wb') as w:
                    for c in range(num_of_chunk-1):
                        w.write(f.read(chunk_size))
                    # Last chunk of the file might not be full of data.
                    bytes_remain = size - chunk_size * (num_of_chunk-1)
                    print(bytes_remain)
                    w.write(f.read(chunk_size)[:bytes_remain])
                print()
