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

key = b'\xe8\x22\x00\x00'

def getVolume(path, entry):
    '''Get the volume of a nus3bank file.

    Parameters:
    path (str): The path to the nus3bank file that will be changed
    entry (int): The entry of the nus3bank. Leave blank (or use 0) for music. This can also be a string, but it must be able to convert to an int.
    
    Returns:
    float: The volume of the nus3bank
    bytearray: The content of the nus3bank
    # int: The occurrence of where the new volume should go in the nus3bank

    '''
    # If an entry is not provided, assume it's 0
    if entry == '':
        entry = 0

    try:
        entry = int(entry)

        # Raise ExtensionError if the file doesn't end in .nus3bank or .nus3bank.bak
        if not (path[-9:] == '.nus3bank' or path[-13:] == '.nus3bank.bak'):
            raise ExtensionError

        with open(path, 'rb+') as f:
            occurence = 0
            content = bytearray(f.read())

            for i in range(len(content)):
                if key == content[i:i+4]:
                    occurence += 1
                if occurence == entry + 2:
                    break
            else:
                raise EntryError

            oldVolume = hex_to_float(int.from_bytes(content[i+4:i+8], byteorder='little'))
            return oldVolume, content, i

    except EntryError:
        sg.popup_error('Entry number not found. Terminating program.')
    except ExtensionError:
        sg.popup_error('File did not end with .nus3bank or .nus3bank.bak. Terminating program.')
    except:
        sg.popup_error('An unknown error has occurred. Terminating program.')


def changeVolume(content, index, path, entry, newVolume, newFileName=None):
    '''Change the volume of a nus3bank and store a backup of the file.
    
    The new file will end in ".nus3bank" while the backup will end in ".nus3bank.bak".

    Parameters:
    content (bytearray): The content of the original nus3bank
    index (int): The place where the new volume goes in the file
    path (str): The path to the nus3bank file that will be changed
    entry (int): The entry of the nus3bank. Leave blank (or use 0) for music. This can also be a string, but it must be able to convert to an int.
    newVolume (float): The new volume for the nus3bank
    newFileName (str): The name of the file that it should be saved as. If this exists, then the new file will be saved with this name. Note that this should be the full path to the file.

    Returns:
    bool: True if the file being edited was a backup. False otherwise.

    '''
    # If an entry is not provided, assume it's 0
    if entry == '':
        entry = 0
    
    # If a new file name is not provided, set it to the name of the old nus3bank
    if not newFileName:
        newFileName = path

    try:
        entry = int(entry)

        # Raise ExtensionError if the file doesn't end in .nus3bank or .nus3bank.bak
        if not (path[-9:] == '.nus3bank' or path[-13:] == '.nus3bank.bak'):
            raise ExtensionError

        # Determine if the file is a backup
        isBackup = False
        if path[-13:] == '.nus3bank.bak':
            isBackup = True

        # Create backup if not editing a backup
        if not isBackup:
            backupName = path + '.bak'
            with open(backupName, 'wb') as backup:
                backup.write(content)
        
        # Get new volume
        volume = float_to_hex(newVolume)
        volume = volume.to_bytes(4, 'big')

        # Write the new file
        with open(newFileName, 'wb+') as f:
            # Write to the beginning and erase the end
            content[index + 4:index + 8] = volume
            f.seek(0)
            f.write(content)
            f.truncate(len(content))
        
        return isBackup

    except EntryError:
        sg.popup_error('Entry number not found. Terminating program.')
    except ExtensionError:
        sg.popup_error('File did not end with .nus3bank or .nus3bank.bak. Terminating program.')
    except:
        sg.popup_error('An unknown error has occurred. Terminating program.')


def isLastDigitNumber(num):
    '''Check if the last character of an input is a number.

    This also checks for negative signs and decimals, and won't allow 2 decimals or a negative sign in the wrong place.

    Parameters:
    num (str): The input that gets checked

    Returns:
    bool: If the input is a number or not

    '''
    # This is the first character, so hyphens, decimals, and numbers are allowed
    if len(num) == 1:
        return num[0] in '-.0123456789'
    # There's more than 1 character, so hyphens can't be allowed now
    if '.' not in num[:-1]:
        return num[-1] in '.0123456789'
    # A decimal was found, so there can't be decimals either.
    return num[-1].isdigit()


def toFirstPage(window, backupSaved):
    '''Move from the second page to the first page'''
    # Change layouts
    window['col2'].update(visible=False)
    window['col1'].update(visible=True)

    # Update text so that it says a backup was saved if and only if a backup was saved
    if backupSaved:
        window['savedText'].update('The file has been saved. A backup has not been saved.')
    else:
        window['savedText'].update('The file has been saved. A backup of the file has been saved with the .nus3bank.bak extension.')

    # Update submit button, disable it, and tell user that the file's been saved
    window['submit'].update('Get original volume')
    window['submit'].update(disabled=True)
    window['savedText'].update(visible=True)

    # Make the Save As button invisible
    window['saveAsFrame'].update(visible=False)

    # Clear values for the file
    window['fileInput'].update('')


# A list of file extensions for nus3bank files
fileExtensions = (('NUS3BANK files', '*.nus3bank'), ('Backup NUS3BANK files', '*.nus3bank.bak'), ('All files', '*.*'))
origVol = None

# If a file has been passed as a command-line argument, fill the file field in automatically
inputtedFile = ''
submitDisabled = True
if len(sys.argv) >= 2:
    inputtedFile = sys.argv[1]
    submitDisabled = False

# Create the GUI
sg.theme('DarkAmber')

# First layout used when getting the original volume of a nus3bank
# For some reason, I need to put text on the first element (savedText) or else it won't update with all of the text.
layout1 = [ [sg.Text('The file has been saved. A backup of the file has been saved with the .nus3bank.bak extension.', visible=False, key='savedText')],
            [sg.Text('Entry (leave blank if music):')],
            [sg.Input(key='Entry', enable_events=True)],
            [sg.Text('Select the nus3bank file:')],
            [sg.Input(disabled=True, key='fileInput', disabled_readonly_background_color='#705e52', enable_events=True, default_text=inputtedFile),
            sg.FileBrowse(file_types=fileExtensions, key='nus3bankFile')]] # This isn't an extra row, the line just got too long

# Second layout used when changing the volume of a nus3bank
layout2 = [ [sg.Text('Original volume:'), sg.Text(str(origVol), key='originalVolume')],
            [sg.Text('New volume (negatives and decimals allowed):'), sg.Input(key='newVol', enable_events=True)]]

# A SaveAs button. It needs to be in a frame so it can turn invisible.
saveAs = sg.Frame(title='', border_width=0, visible=False, key='saveAsFrame',
                  layout=[[sg.SaveAs(file_types=fileExtensions, enable_events=True, key='saveAsButton')]])
# Container layout used to switch between layouts
layout = [[sg.Column(layout1, key='col1'), sg.Column(layout2, visible=False, key='col2')],
          [sg.Button('Get original volume', key='submit', disabled=submitDisabled), saveAs]]

window = sg.Window('Nus3bank Volume GUI', layout)

# Keep track of layouts
layoutCounter = 1

# Handle events
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, None):
        break

    # Validate entry to be a whole number
    elif event == 'Entry' and values['Entry'] and not values['Entry'][-1].isdigit():
        window['Entry'].update(values['Entry'][:-1])
    

    # Validate volume & disable save buttons until a volume is entered
    elif event == 'newVol':
        # Validate volume to be a float
        if values['newVol'] and not isLastDigitNumber(values['newVol']):
            window['newVol'].update(values['newVol'][:-1])
    
        # Don't allow user to save if a new volume has not been entered
        if not any(c.isdigit() for c in values['newVol']):
            window['submit'].update(disabled=True)
            window['saveAsButton'].update(disabled=True)
        else:
            window['submit'].update(disabled=False)
            window['saveAsButton'].update(disabled=False)
    
    # Show file path when user selects a file
    elif event == 'nus3bankFile':
        window['fileInput'].update(values['nus3bankFile'])

    # Enable the "Get original volume" button if the user inputs a file
    elif event == 'fileInput':
        if values['fileInput']:
            window['submit'].update(disabled=False)
        else:
            window['submit'].update(disabled=True)


    elif event == 'submit':
        # Get original volume
        if layoutCounter == 1:
            origVol, content, occurence = getVolume(values['fileInput'], values['Entry'])
            # Change layouts
            window['col1'].update(visible=False)
            window['col2'].update(visible=True)

            # Disable save buttons
            window['submit'].update(disabled=True)
            window['saveAsButton'].update(disabled=True)

            # Clear the new volume field
            window['newVol'].update('')

            # Show original volume & saveAs button and update submit button
            window['originalVolume'].update(str(origVol))
            window['saveAsFrame'].update(visible=True)
            window['submit'].update('Change volume & save')
            layoutCounter = 2

        else:
            # Change the volume and save
            backupSaved = changeVolume(content, occurence, values['fileInput'], values['Entry'], float(values['newVol']))

            # Go to the first page
            toFirstPage(window, backupSaved)

            layoutCounter = 1


    elif event == 'saveAsButton':
        fileName = values['saveAsButton']
        
        # Change the volume and save
        backupSaved = changeVolume(content, occurence, values['fileInput'], values['Entry'], float(values['newVol']), fileName)

        # Go to the first page
        toFirstPage(window, backupSaved)

        layoutCounter = 1
        

window.close()