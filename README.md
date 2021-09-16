# Nus3bank-volume-GUI

This is meant to be a simple GUI that can edit the volume of a NUS3Bank file. It should help in modding Super Smash Bros. Ultimate.

This was made using PySimpleGUI, and this wouldn't be possible without the help of [zrksyd](https://github.com/zrksyd) or [Genwald](https://github.com/Genwald). zrksyd made the original [volume.py](https://gist.github.com/zrksyd/8e25e9ea5244714c5418d466a424107e) script, which was a CLI tool to adjust the volume of NUS3Bank files. Genwald made [nus3volume.py](https://gist.github.com/Genwald/d4e39d5ccc9e98266914efd1a2e4e813), which fixed a bug in zrksyd's program that affected NUS3Bank files for Voice/SFX files.

To download this program, click [here](https://github.com/Pacil142857/nus3bank-volume-GUI/releases/latest).

## Tutorial

This is a quick tutorial on how to use the program.

When you launch the application, it will ask you for an entry number and a NUS3Bank file, like this:

![The first part of the application](https://i.imgur.com/fkAf8bi.png)

If you're replacing a music file, then leave the entry field blank. If you're replacing a Voice/SFX NUS3Bank file, then you might find this part useful since you can control the volume of a specific voice line (you can find the entry number you need using [this website](https://smashultimatetools.com/audio/nus3audio_idsp)). As for the file, just click on "Browse" and select a NUS3Bank file (You can extract NUS3Bank files with [ArcExplorer](https://github.com/ScanMountGoat/ArcExplorer) or a similar tool). This example shows the NUS3Bank for "Driver Vs." from the Xenoblade Chronicles series. Once you've selected a file (and optionally an entry), click on the "Get original volume" button.

![The second part of the application](https://i.imgur.com/FVYAg64.png)

Following that, you'll see a screen like this. You can see the original volume of the NUS3Bank here. Sometimes it'll look weirdly specific, as shown here. This is because decimals can be a little bit off, so there's nothing wrong if the volume is off by 0.001. In any case, the next step is to input the new volume that you want the NUS3Bank to have. For songs, I recommend somewhere between 4.7 and 5. You can input negative and decimal numbers if you'd like.

Once you've done that, you have two options: quickly save the file with the same filename as before, or make a new filename. A backup of your file will not be saved, but you can always just change the volume back to what it was before. If you click on "Change volume & save", the new file will be stored in the same location with the same name. If you click on "Save As...", you'll get a popup asking you where to save the file. You can choose where to save the file and you can also choose the filename. After you save the file, you'll go back to the first page.

This program can also work if you double click on a NUS3Bank file, but it needs a bit of setting up to do. First, find any NUS3Bank file in File Explorer. Right click the file, and select "Open with". Click on "More apps", scroll down, and click on "Look for another app on this PC". Locate this program (nus3bank-volume-GUI.exe) and select it. After doing that, you should be able to double click on any NUS3Bank file to open it with this program. You can do the same thing for nus3bank.bak files, but it will affect all files ending in ".bak" instead of only files ending in .nus3bank.bak.

You can also edit files in batch, which is fairly straightforward. On the first page of the application, click the "Batch Edit" button. You'll then be taken to a page where you can set the volume for multiple files at once. You can hold CTRL to select multiple files at once.
