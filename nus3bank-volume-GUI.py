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
    '''Get the volume of a nus3bank file.

    Parameters:
    path (str): The path to the nus3bank file that will be changed
    entry (int): The entry of the nus3bank. Leave blank (or use 0) for music. This can also be a string, but it must be able to convert to an int.
    
    Returns:
    float: The volume of the nus3bank

    '''
    # If an entry is not provided, assume it's 0
    if entry == '':
        entry = 0

    try:
        entry = int(entry)
        if path[-9:] != ".nus3bank":
            raise ExtensionError
        with open(path, "rb+") as f:
            occurance = 0
            content = bytearray(f.read())

            for i in range(len(content)):
                if key == content[i:i+4]:
                    occurance += 1
                if occurance == entry + 2:
                    break
            else:
                raise EntryError

            oldVolume = hex_to_float(int.from_bytes(content[i+4:i+8], byteorder='little'))
            return oldVolume

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


def changeVolume(path, entry, newVolume, newFileName=None):
    '''Change the volume of a nus3bank and store a backup of the file.
    
    The new file will end in ".nus3bank" while the backup will end in ".nus3bank.bak".

    Parameters:
    path (str): The path to the nus3bank file that will be changed
    entry (int): The entry of the nus3bank. Leave blank (or use 0) for music. This can also be a string, but it must be able to convert to an int.
    newVolume (float): The new volume for the nus3bank
    newFileName (str): The name of the file that it should be saved as. If this exists, then the new file will be saved with this name. Note that this should be the full path to the file.

    '''
    # If an entry is not provided, assume it's 0
    if entry == '':
        entry = 0
    
    # If a new file name is not provided, set it to the name of the old nus3bank
    if not newFileName:
        newFileName = path

    try:
        entry = int(entry)
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
            
            volume = float_to_hex(newVolume)
            volume = volume.to_bytes(4, 'big')

        # Write the new file
        with open(newFileName, 'wb+') as f:
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


def isLastDigitNumber(num, negativeFloat=False):
    '''Check if the last character of an input is a number.

    If negativeFloat is true, also check for negative signs and decimals.

    Parameters:
    num (str): The input that gets checked

    Keyword arguments:
    negativeFloat (bool): Allow negative numbers and decimals (default False)

    Returns:
    bool: If the input is a number or not

    '''
    if not negativeFloat:
        return num[-1] in '0123456789'
    
    # This is the first character, so hyphens, decimals, and numbers are allowed
    if len(num) == 1:
        return num[0] in '-.0123456789'
    # There's more than 1 character, so hyphens can't be allowed now
    if '.' not in num[:-1]:
        return num[-1] in '.0123456789'
    # A decimal was found, so there can't be decimals either.
    return num[-1] in '0123456789'


# A list of file extensions for nus3bank files
fileExtensions = (('NUS3BANK files', '*.nus3bank'), ('Backup NUS3BANK files', '*.nus3bank.bak'), ('All files', '*.*'))
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
            [sg.Text('New volume:'), sg.Input(key='newVol', enable_events=True)]]

# A SaveAs button. It needs to be in a frame so it can turn invisible.
saveAs = sg.Frame(title='', border_width=0, visible=False, key='saveAsFrame',
                  layout=[[sg.SaveAs(file_types=fileExtensions, enable_events=True, key='saveAsButton')]])
# Container layout used to switch between layouts
layout = [[sg.Column(layout1, key='col1'), sg.Column(layout2, visible=False, key='col2')],
          [sg.Button('Get old volume', key='submit'), saveAs]]

window = sg.Window('Nus3bank Volume GUI', layout)

# Keep track of layouts
layoutCounter = 1
# Handle events
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, None):
        break

    # Validate entry to be a whole number
    elif event == 'Entry' and values['Entry'] and not isLastDigitNumber(values['Entry']):
        window['Entry'].update(values['Entry'][:-1])
    
    # Validate volume to be a float
    elif event == 'newVol' and values['newVol'] and not isLastDigitNumber(values['newVol'], True):
        window['newVol'].update(values['newVol'][:-1])
        pass
    
    # Show file path when user selects a file
    elif event == 'nus3bankFile':
        window['fileInput'].update(values['nus3bankFile'])


    elif event == 'submit':
        # Get original volume
        if layoutCounter == 1:
            origVol = getVolume(values['fileInput'], values['Entry'])
            # Change layouts
            window['col1'].update(visible=False)
            window['col2'].update(visible=True)

            # Show original volume & saveAs button and update submit button
            window['originalVolume'].update(str(origVol))
            window['saveAsFrame'].update(visible=True)
            window['submit'].update('Change volume & save')
            layoutCounter = 2

        else:
            # Change the volume and save
            changeVolume(values['fileInput'], values['Entry'], float(values['newVol']))
            # Change layouts
            window['col2'].update(visible=False)
            window['col1'].update(visible=True)

            # Update submit button and tell user that the file's been saved
            window['submit'].update('Get old volume')
            window['savedText'].update(visible=True)

            # Make the Save As button invisible
            window['saveAsFrame'].update(visible=False)

            # Clear values for the file
            window['fileInput'].update('')
            layoutCounter = 1
        
    elif event == 'saveAsButton':
        fileName = values['saveAsButton']
        
        # Change the volume and save
        changeVolume(values['fileInput'], values['Entry'], float(values['newVol']), fileName)

        # Change layouts
        window['col2'].update(visible=False)
        window['col1'].update(visible=True)

        # Update submit button and tell user that the file's been saved
        window['submit'].update('Get old volume')
        window['savedText'].update(visible=True)

        # Make the Save As button invisible
        window['saveAsFrame'].update(visible=False)

        # Clear values for the file
        window['fileInput'].update('')
        layoutCounter = 1
        

window.close()