# Nus3bank-volume-GUI
This is meant to be a simple GUI that can edit the volume of a nus3bank file. It should help in modding Super Smash Bros. Ultimate.

This was made using PySimpleGUI, and this wouldn't be possible without the help of [zrksyd](https://github.com/zrksyd) who made the original [volume.py](https://gist.github.com/zrksyd/8e25e9ea5244714c5418d466a424107e) file, which was a CLI tool to adjust the volume of nus3bank files.

To download this program, click [here](https://github.com/Pacil142857/nus3bank-volume-GUI/releases/latest).

## Tutorial
This is a quick tutorial on how to use the program.

When you launch the application, it will ask you for an entry number and a nus3bank file, like this:

![The first part of the application](https://i.imgur.com/fkAf8bi.png)

If you're replacing a music file, then leave the entry field blank. If you're replacing a different nus3bank file (for example, Mario's voice files), then you might find this part useful since you can control the volume of a specific voice line. As for the file, just click on "Browse" and select a file. This example shows the nus3bank for "Driver Vs." from the Xenoblade Chronicles series. Once you've selected a file (and optionally an entry), click on the "Get original volume" button.

![The second part of the application](https://i.imgur.com/FVYAg64.png)

Following that, you'll see a screen like this. You can see the original volume of the nus3bank here. Sometimes it'll look weirdly specific, like shown here (Well, I don't think the developers intentionally made the volume 3.599, but what do I know?) This is because decimals can be a little bit off, so there's nothing wrong if the volume is off by 0.001. In any case, the next step is to input the new volume that you want the nus3bank to have. For songs, I recommend somewhere between 4.3 and 4.5. You can input negative and decimal numbers if you'd like.

Once you've done that, you have two options: quickly save the file with the same filename as before, or make a new filename. In either case, a backup of the original will be stored as "filename".nus3bank.bak (where "filename" is replaced by the filename). Please note that the backup will replace any preexisting backups with the same name. If you click on "Change volume & save", the new file will be stored in the same location with the same name. If you click on "Save As...", you'll get a popup asking you where to save the file. You can choose where to save the file and you can also choose the filename. Once you click either of those buttons, you'll go back to the first page.