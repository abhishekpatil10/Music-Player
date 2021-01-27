import os
import threading
import time
import tkinter
import pygame
from tkinter import *
from pygame import mixer
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
root=tkinter.Tk()
bg = PhotoImage(file = "images/bg.png")
bg1 = Label( root, image = bg) 
bg1.place(x = 0, y = 0,width = 300,height = 500)

#initializing the mixer from pygame module

pygame.mixer.init() 
# Adding File Menu and commands
menubar = Menu(root)  
#for opening of a music file... 
def open_file():
	global filename
	filename = filedialog.askopenfilename()  # file will store inside a filename variable
file = Menu(menubar, tearoff = 0) 
menubar.add_cascade(label ='File', menu = file) 
file.add_command(label ='Open...', command = open_file) 
file.add_separator() 
file.add_command(label ='Exit', command = root.destroy) 
file = Menu(menubar, tearoff = 0) 
def about_us():
	tkinter.messagebox.showinfo('MUSICPLAYER','This is a music player designed by Abhishek.')
#second menu in menubar i.e Help
menubar.add_cascade(label ='Help', menu = file) 
file.add_command(label ='About Us', command = about_us)


#window size of app
root.config(menu = menubar) 
root.geometry("330x400+300+300")
root.resizable(0,0)
root.title('MUSICPLAYER')
root.iconbitmap(r'images/music.ico')

#heading
filelabel=Label(root,text="MUSICPLAYER ",bg='black',fg='white',width=50,height=2)
filelabel.pack(pady=5)

#length of  a song....

def show_details():
    file_data = os.path.splitext(filename)

    if file_data[1] == '.mp3':
        audio = MP3(filename)
        total_length = audio.info.length
    else:
        a = mixer.Sound(filename)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat
    #starts as the song start counting the time
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

#starting the count of music
def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

#for playing music
def play_music():
	global paused
	if paused:   #--- if paused if condition is checked
		mixer.music.unpause()
		statusbar['text']="Music resumed.."+ ' - ' + os.path.basename(filename)
		playBtn.configure(image=pausePhoto)
		paused=FALSE
	else:   #---- if not else will terminate & while starting a new song..
		try:
			mixer.music.load(filename)
			mixer.music.play()
			playBtn.configure(image=pausePhoto)
			statusbar['text']='Music is playing..'+ ' - ' + os.path.basename(filename)
			show_details()
			
		except:    # ----- if music is not selected this will terminate...
			tkinter.messagebox.showerror('MUSICPLAYER','No Music Selected')

#stop music while terminating the window 
def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

#for pausing music
paused=FALSE
def pause_music():
	global paused
	paused = TRUE
	mixer.music.pause()
	playBtn.configure(image=playPhoto)
	statusbar['text']='Music is paused..'


#for adjusting volume	
def set_vol(val):
	volume=int(val)/100
	mixer.music.set_volume(volume)

#for muting the music
muted=FALSE
def mute_music():
	global muted
	if muted:    #if muted ---
		mixer.music.set_volume(0.5)
		volumeBtn.configure(image=volumePhoto)
		scale.set(50)
		muted=FALSE
	else:   #if not muted --
		mixer.music.set_volume(0)
		volumeBtn.configure(image=mutePhoto)
		scale.set(0)
		muted=TRUE

#frame for buttons 
rightframe=Frame(root)
rightframe.pack(pady=30)
#midframe = buttons i.e play pause
midframe = Frame(rightframe)
midframe.pack(padx=20)
#play music
pausePhoto = PhotoImage(file = 'images/pause.png')
playPhoto = PhotoImage(file = 'images/play-button.png')
playBtn = ttk.Button(midframe,image = playPhoto,command = play_music)
playBtn.grid(row=0,column=0,padx=10)

#next music
nextPhoto = PhotoImage(file = 'images/stop.png')
nextBtn = ttk.Button(midframe,image = nextPhoto,command = pause_music)
nextBtn.grid(row=0,column=1,padx=10)

#text info for buttons i.e play & pause 

playlabel =Label(midframe, text='Play',bg='black',fg='white')
playlabel.grid(row=1,column=0,padx=5,pady=5)
pauselabel =Label(midframe, text='Pause',bg='black',fg='white')
pauselabel.grid(row=1,column=1,padx=5,pady=5)

#song lenth label
lengthlabel = ttk.Label(root, text='Total Length : --:--')
lengthlabel.pack()
#current duration i.e. time of song
currenttimelabel = ttk.Label(root, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()

#frame for mute button 
bottomframe=Frame(root)
bottomframe.pack(pady=10,padx=10)
#mute button
mutePhoto = PhotoImage(file = 'images/mute.png')
volumePhoto = PhotoImage(file = 'images/high-volume.png')
volumeBtn = ttk.Button(bottomframe,image = volumePhoto,command = mute_music)
volumeBtn.grid(row=0,column=1)
#volume bar
scale = Scale(root, from_ = 0,to = 100 ,orient = HORIZONTAL,fg='red',command=set_vol)
scale.set(50)
mixer.music.set_volume(0.5)
scale.pack()

#volume text.....
text=Label(root,text="Volume",fg='white',bg='black')
text.pack()

#statusbar i.e bottom navigation.....
statusbar = Label(root,text="Welcome to Music Player",bg='black',fg='white',relief = SUNKEN)
statusbar.pack(side=BOTTOM,fill = X)

#On closing the window .
def on_closing():
    stop_music()
    #root.destroy will terminate the window..
    root.destroy()
#for closing the tkinter window
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
