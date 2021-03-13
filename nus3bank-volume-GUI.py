import PySimpleGUI as sg
import struct
import sys

# TODO: Create a GUI that asks for a file, entry, and volume
# TODO: Show old volume of nus3bank
# TODO: Make function to change/read volume of nus3bank

# Upon selecting a file, the code should read the file
## If an error occurs, deselect the file and raise an error
# Display the old volume of the given entry
# Ask user for new volume
# Create the new file and save the backup

class ArgumentError(Exception):
    pass
class EntryError(Exception):
    pass
class ExtensionError(Exception):
    pass

def float_to_hex(f):
    return struct.unpack('>I', struct.pack('<f', f))[0]
def hex_to_float(hx):
    if type(hx) == str:
        hx = int(hx)
    return struct.unpack("<f",struct.pack("<I",hx))[0]

'''
regularInput = False
if len(sys.argv) > 4 or len(sys.argv) == 2:
    #More than 3 command-line arguments or 1 command-line argument
    raise ArgumentError
elif len(sys.argv) == 4:
    #3 command-line arguments
    path = sys.argv[1]
    entry = int(sys.argv[2])
    volumeFloat = float(sys.argv[3])
elif len(sys.argv) == 3:
    #2 command-line arguments
    path = sys.argv[1]
    entry = 0
    volumeFloat = float(sys.argv[2])
else:
    path = input("NUS3BANK path: ")
    path = path.replace('"', '') #Remove any quotes in input
    entry = input("Entry (leave blank if music): ")
    if entry == "":
        entry = 0
    else:
        entry = int(entry)
    regularInput = True

key = b'\xe8\x22\x00\x00'
try:
    if path[-9:] != ".nus3bank":
        raise ExtensionError
    with open(path, "rb+") as f:
        occurance = 0
        content = bytearray(f.read())

        backupName = path[:-9] + ".nus3bank.bak"
        with open(backupName, "wb") as backup:
            backup.write(content)

        for i in range(len(content)):
            if key == content[i:i+4]:
                occurance += 1
            if occurance == entry + 2:
                break
        else:
            raise EntryError

        oldVolume = hex_to_float(int.from_bytes(content[i+4:i+8], byteorder='little'))
        print("Old volume: " + str(oldVolume))
        #print("Changing volume of entry " + str(entry) + " from " + str(oldVolume) + " to " + str(volumeFloat) + "...")
        if regularInput:
            volumeFloat = float(input("New volume (decimal and negative values are valid): "))
        volume = float_to_hex(volumeFloat)
        volume = volume.to_bytes(4, 'big')

        #Write to the beginning and erase the end
        content[i+4:i+8] = volume
        f.seek(0)
        f.write(content)
        f.truncate(len(content))

except ArgumentError:
    print("Incorrect number of arguments.")
except EntryError:
    print("Entry number not found.")
except ExtensionError:
    print("File did not end with .nus3bank.")
except:
    print("An unknown error has occurred.")
finally:
    f.close()
    backup.close()
'''

# A list of file extensions for nus3bank files
fileExtensions = (('NUS3BANK files', '*.nus3bank'), ('Backup NUS3BANK files', '*.nus3bank.bak'))

# Create the GUI
sg.theme('DarkAmber')

# Base layout
layout = [ [sg.Text('Entry (put 0 if music):')],
           [sg.Input(key='Entry', enable_events=True)],
           [sg.Text('Select the nus3bank file:')],
           [sg.Input(disabled=True, key='fileInput', disabled_readonly_background_color='#705e52'), sg.FileBrowse(file_types=fileExtensions, key='nus3bankFile')],
           [sg.Button('Get old volume', key='Submit')]]

window = sg.Window('Nus3bank Volume GUI', layout)

print(window['Entry'].BackgroundColor)

# Handle events
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, None):
        break

    # Validate entry to be a whole number
    if event == 'Entry' and values['Entry'] and values['Entry'][-1] not in ('0123456789'):
        window['Entry'].update(values['Entry'][:-1])
    
    if event == 'nus3bankFile':
        window['fileInput'].update(values['nus3bankFile'])

    if event == 'Submit':
        print(f'Entry: {values["Entry"]}')
        print(f'File: {values["nus3bankFile"]}')
        # TODO: Get the volume when the user presses submit

window.close()