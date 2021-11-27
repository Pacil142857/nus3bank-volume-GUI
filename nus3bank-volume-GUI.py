# Some of this code was originally written by zrksyd in his volume.py program and Genwald in his nus3volume.py program
# The original volume.py program can be found here: https://gist.github.com/zrksyd/8e25e9ea5244714c5418d466a424107e
# The original nus3volume.py program can be found here: https://gist.github.com/Genwald/d4e39d5ccc9e98266914efd1a2e4e813
# You can check out zrksyd's Github profile page here: https://github.com/zrksyd
# You can check out Genwald's Github profile page here: https://github.com/Genwald

import nus3volume
import PySimpleGUI as sg
import sys


class ArgumentError(Exception):
    pass
class EntryError(Exception):
    pass
class ExtensionError(Exception):
    pass


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

        # Raise ExtensionError if the file doesn't end in .nus3bank or .nus3bank.bak
        if not (path[-9:] == '.nus3bank' or path[-13:] == '.nus3bank.bak'):
            raise ExtensionError
        
        # Get the volume
        with open(path, 'rb+') as f:
            file = nus3volume.BankReader(f)
            volume = file.get_volume(entry)
        
        return volume

    except EntryError:
        sg.popup_error('Entry number not found. Terminating program.')
        sys.exit()
    except ExtensionError:
        sg.popup_error('File did not end with .nus3bank or .nus3bank.bak. Terminating program.')
        sys.exit()
    except nus3volume.InvalidMagic:
        sg.popup_error('File must be a valid NUS3Bank file. Terminating program.')
        sys.exit()
    except:
        sg.popup_error('An unknown error has occurred. Terminating program.')
        sys.exit()


def changeVolume(path, entry, newVolume, newFileName=None):
    '''Change the volume of a nus3bank.
    
    The new file will end in ".nus3bank".

    Parameters:
    # content (bytearray): The content of the original nus3bank
    path (str): The path to the nus3bank file that will be changed
    entry (int): The entry of the nus3bank. Leave blank (or use 0) for music. This can also be a string, but it must be able to convert to an int.
    newVolume (float): The new volume for the nus3bank
    newFileName (str): The name of the file that it should be saved as. If this exists, then the new file will be saved with this name. Note that this should be the full path to the file.

    Returns:
    None

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
        
        # Get new volume
        with open(path, 'rb+') as f:
            file = nus3volume.BankReader(f)
            file.set_volume(entry, newVolume)

    except EntryError:
        sg.popup_error('Entry number not found. Terminating program.')
        sys.exit()
    except ExtensionError:
        sg.popup_error('File did not end with .nus3bank or .nus3bank.bak. Terminating program.')
        sys.exit()
    except nus3volume.InvalidMagic:
        sg.popup_error('File must be a valid NUS3Bank file. Terminating program.')
        sys.exit()
    except:
        sg.popup_error('An unknown error has occurred. Terminating program.')
        sys.exit()


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


def toFirstPage(window):
    '''Move from the second page to the first page'''
    # Change layouts
    window['col2'].update(visible=False)
    window['col1'].update(visible=True)
    
    window['savedText'].update('The file has been saved.')
    
    # Update submit button, disable it, and tell user that the file's been saved
    window['submit'].update('Get original volume')
    window['submit'].update(disabled=True)
    window['savedText'].update(visible=True)

    # Make the Save As button invisible
    window['saveAsFrame'].update(visible=False)
    window['saveAsButton'].update(disabled=True)
    
    # Make Batch Editing button visible
    window['batch'].update(visible=True, disabled=False)

    # Clear values for the file and entry
    window['fileInput'].update('')
    window['Entry'].update('')


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
layout1 = [ [sg.Text('The file has been saved.', visible=False, key='savedText')],
            [sg.Text('Entry (leave blank if music):')],
            [sg.Input(key='Entry', enable_events=True)],
            [sg.Text('Select the nus3bank file:')],
            [sg.Input(disabled=True, key='fileInput', disabled_readonly_background_color='#705e52', enable_events=True, default_text=inputtedFile),
            sg.FileBrowse(file_types=fileExtensions, key='nus3bankFile')]] # This isn't an extra row, the line just got too long

# Second layout used when changing the volume of a nus3bank
layout2 = [ [sg.Text('Original volume:'), sg.Text(str(origVol), key='originalVolume')],
            [sg.Text('New volume (negatives and decimals allowed):'), sg.Input(key='newVol', enable_events=True)]]

# Layout for batch editing
layout3 = [ [sg.Text('The files were saved.', visible=False, key='savedBatchText')],
            [sg.Text('Select all the files you want to edit. Hold CTRL to select multiple files.')],
            [sg.Input(disabled=True, key='batchFiles', disabled_readonly_background_color='#705e52', enable_events=True),
             sg.FilesBrowse(file_types=fileExtensions, key='nus3bankBatchFiles', files_delimiter='<::>', enable_events=True)], # This isn't an extra row, the line just got too long
            [sg.Text('New volume (negatives and decimals allowed):'), sg.Input(key='newBatchVol', enable_events=True, size=(10, 1))]]

# A SaveAs button. It needs to be in a frame so it can turn invisible.
saveAs = sg.Frame(title='', border_width=0, visible=False, key='saveAsFrame',
                  layout=[[sg.SaveAs(file_types=fileExtensions, enable_events=True, key='saveAsButton')]])
# Container layout used to switch between layouts
layout = [[sg.Column(layout1, key='col1'), sg.Column(layout2, visible=False, key='col2'), sg.Column(layout3, visible=False, key='col3')],
          [sg.Button('Get original volume', key='submit', disabled=submitDisabled), saveAs, sg.Button('Batch Edit', key='batch')]]

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
    
    # Validate volume & disable save buttons until a volume is entered
    elif event == 'newBatchVol':
        # Validate volume to be a float
        if values['newBatchVol'] and not isLastDigitNumber(values['newBatchVol']):
            window['newBatchVol'].update(values['newBatchVol'][:-1])
    
        # Disable save buttons if there is no file or volume
        if not (values['nus3bankBatchFiles'] and any(c.isdigit() for c in values['newBatchVol'])):
            window['submit'].update(disabled=True)
            window['batch'].update(disabled=True)
        else:
            window['submit'].update(disabled=False)
            window['batch'].update(disabled=False)

    # Show file path when user selects a file
    elif event == 'batchFiles':
        window['batchFiles'].update(' | '.join(values['nus3bankBatchFiles'].split('<::>')))
        
        # Disable save buttons if there is no file or volume
        if not (values['nus3bankBatchFiles'] and any(c.isdigit() for c in values['newBatchVol'])):
            window['submit'].update(disabled=True)
            window['batch'].update(disabled=True)
        else:
            window['submit'].update(disabled=False)
            window['batch'].update(disabled=False)

    # Enable the "Get original volume" button if the user inputs a file
    elif event == 'fileInput':
        if values['fileInput']:
            window['submit'].update(disabled=False)
        else:
            window['submit'].update(disabled=True)

    # Go to batch editing if the user selects Batch Edit
    elif event == 'batch':
        
        # Switch to batch editing page
        if layoutCounter == 1:
            # Switch layouts
            window['col1'].update(visible=False)
            window['col3'].update(visible=True)
            
            # Change text on buttons
            window['batch'].update('Save and continue batch editing', disabled=True)
            window['submit'].update('Save and go back', disabled=True)
            
            layoutCounter = 3
        
        else:
            # Change volume of all the files
            for file in values['nus3bankBatchFiles'].split('<::>'):
                changeVolume(file, 0, float(values['newBatchVol']))
                
            # Tell user the files were saved
            window['savedBatchText'].update(visible=True)
            
            # Reset form fields
            window['batchFiles'].update('')
            window['newBatchVol'].update('')


    elif event == 'submit':
        # Get original volume
        if layoutCounter == 1:
            origVol = getVolume(values['fileInput'], values['Entry'])
            # Change layouts
            window['col1'].update(visible=False)
            window['col2'].update(visible=True)

            # Hide Batch Editing button
            window['batch'].update(visible=False, disabled=True)

            # Disable save buttons
            window['submit'].update(disabled=True)
            window['saveAsButton'].update(disabled=True)

            # Clear the new volume field
            window['newVol'].update('')

            # Show original volume & saveAs button and update submit button
            window['originalVolume'].update(str(origVol))
            window['saveAsFrame'].update(visible=True)
            window['saveAsButton'].update(disabled=False)
            window['submit'].update('Change volume & save')
            layoutCounter = 2
        elif layoutCounter == 2:
            # Change the volume and save
            changeVolume(values['fileInput'], values['Entry'], float(values['newVol']))

            # Go to the first page
            toFirstPage(window)

            layoutCounter = 1

        elif layoutCounter == 3:
            # Change volume of all the files
            for file in values['nus3bankBatchFiles'].split('<::>'):
                changeVolume(file, 0, float(values['newBatchVol']))
        
            # Change layouts
            window['col3'].update(visible=False)
            window['col1'].update(visible=True)

            # Update submit button, disable it, and tell user that the file's been saved
            window['savedText'].update('The files were saved.', visible=True)
            window['submit'].update('Get original volume')
            window['submit'].update(disabled=True, visible=True)

            # Make the Save As button invisible
            window['saveAsFrame'].update(visible=False)

            # Clear values for the file
            window['fileInput'].update('')

            # Update text on Batch Editing button
            window['batch'].update('Batch Edit')
            
            # Reset form fields
            window['batchFiles'].update('')
            window['newBatchVol'].update('')
            
            layoutCounter = 1


    elif event == 'saveAsButton':
        fileName = values['saveAsButton']
        
        # If the user doesn't provide a file, just go back
        if fileName == '':
            continue
        
        # Change the volume and save
        changeVolume(values['fileInput'], values['Entry'], float(values['newVol']), fileName)

        # Go to the first page
        toFirstPage(window)

        layoutCounter = 1
        

window.close()