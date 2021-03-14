import PySimpleGUI as sg
import struct
import sys

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
    # More than 3 command-line arguments or 1 command-line argument
    raise ArgumentError
elif len(sys.argv) == 4:
    # 3 command-line arguments
    path = sys.argv[1]
    entry = int(sys.argv[2])
    volumeFloat = float(sys.argv[3])
elif len(sys.argv) == 3:
    # 2 command-line arguments
    path = sys.argv[1]
    entry = 0
    volumeFloat = float(sys.argv[2])
else:
    path = input("NUS3BANK path: ")
    path = path.replace('"', '') # Remove any quotes in input
    entry = input("Entry (leave blank if music): ")
    if entry == "":
        entry = 0
    else:
        entry = int(entry)
    regularInput = True
'''

key = b'\xe8\x22\x00\x00'

def getVolume(path, entry):
    ''' Get the original volume of a nus3bank '''
    # If an entry is not provided, assume it's 0
    if entry == '':
        entry = 0
    entry = int(entry)

    try:
        if path[-9:] != ".nus3bank":
            raise ExtensionError
        with open(path, "rb+") as f:
            occurance = 0
            content = bytearray(f.read())

            ''' No need to make a backup if we're just getting the volume
            backupName = path[:-9] + ".nus3bank.bak"
            with open(backupName, "wb") as backup:
                backup.write(content)
            '''

            for i in range(len(content)):
                if key == content[i:i+4]:
                    occurance += 1
                if occurance == entry + 2:
                    break
            else:
                raise EntryError

            oldVolume = hex_to_float(int.from_bytes(content[i+4:i+8], byteorder='little'))
            return oldVolume

            ''' The rest of this writes to the file, so it's commented out for now
            print("Old volume: " + str(oldVolume))
            # print("Changing volume of entry " + str(entry) + " from " + str(oldVolume) + " to " + str(volumeFloat) + "...")
            
            volumeFloat = float(input("New volume (decimal and negative values are valid): "))
            volume = float_to_hex(volumeFloat)
            volume = volume.to_bytes(4, 'big')

            # Write to the beginning and erase the end
            content[i+4:i+8] = volume
            f.seek(0)
            f.write(content)
            f.truncate(len(content))
            '''

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
        # Commented out since we didn't make a backup
        # backup.close()


def changeVolume(path, entry, newVolume):
    ''' Change the volume of a nus3bank and store a backup '''
    # If an entry is not provided, assume it's 0
    if entry == '':
        entry = 0
    entry = int(entry)

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

            # print("Changing volume of entry " + str(entry) + " from " + str(oldVolume) + " to " + str(volumeFloat) + "...")
            
            volume = float_to_hex(newVolume)
            volume = volume.to_bytes(4, 'big')

            # Write to the beginning and erase the end
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


# A list of file extensions for nus3bank files
fileExtensions = (('NUS3BANK files', '*.nus3bank'), ('Backup NUS3BANK files', '*.nus3bank.bak'))
origVol = None

# Create the GUI
sg.theme('DarkAmber')

# First layout used when getting the original volume of a nus3bank
layout1 = [ [sg.Text('The file has been saved. A backup of the file has been saved with the .nus3bank.bak extension.', visible=False, key='savedText')],
            [sg.Text('Entry (leave blank if music):')],
            [sg.Input(key='Entry', enable_events=True)],
            [sg.Text('Select the nus3bank file:')],
            [sg.Input(disabled=True, key='fileInput', disabled_readonly_background_color='#705e52'), sg.FileBrowse(file_types=fileExtensions, key='nus3bankFile')]]

# Second layout used when changing the volume of a nus3bank
layout2 = [ [sg.Text('Original volume:'), sg.Text(str(origVol), key='originalVolume')],
            [sg.Text('New volume:'), sg.Input(key='newVol')]]

# Container layout used to switch between layouts
layout = [[sg.Column(layout1, key='col1'), sg.Column(layout2, visible=False, key='col2')],
          [sg.Button('Get old volume', key='submit')]]

window = sg.Window('Nus3bank Volume GUI', layout)

# Keep track of layouts
layoutCounter = 1
# Handle events
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, None):
        break

    # Validate entry to be a whole number
    if event == 'Entry' and values['Entry'] and values['Entry'][-1] not in ('0123456789'):
        window['Entry'].update(values['Entry'][:-1])
    
    # Show file path when user selects a file
    if event == 'nus3bankFile':
        window['fileInput'].update(values['nus3bankFile'])

    if event == 'submit':
        # Get original volume
        if layoutCounter == 1:
            origVol = getVolume(values['fileInput'], values['Entry'])
            # Change layouts
            window['col1'].update(visible=False)
            window['col2'].update(visible=True)

            # Show original volume and update submit button
            window['originalVolume'].update(str(origVol))
            window['submit'].update('Change volume & save')
            layoutCounter = 2

        else:
            # Change layouts
            changeVolume(values['fileInput'], values['Entry'], float(values['newVol']))
            window['col2'].update(visible=False)
            window['col1'].update(visible=True)

            # Update submit button and tell user that the file's been saved
            window['submit'].update('Get old volume')
            window['savedText'].update(visible=True)

            # Clear values for the file
            window['fileInput'].update('')
            layoutCounter = 1
        

window.close()