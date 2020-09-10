# -*- coding: utf-8 -*-
from tkinter.filedialog import askopenfilename, asksaveasfilename
from simpletk import *
from inference import main

@SimpleMain()
async def gui_main():
    pass

audio = None
image = None
save = None
running = False

@pack()
@SimpleButton(gui_main, text='Select audio')
def select_audio():
    global audio
    new = askopenfilename(filetypes=[('.wav files', '*.wav')])
    if new and not new.isspace():
        print('setting audio file to {}'.format(new))
        audio = new.strip()

@pack()
@SimpleButton(gui_main, text='Select image')
def select_image():
    global image
    new = askopenfilename(filetypes=[('.png files', '*.png')])
    if new and not new.isspace():
        print('setting image file to {}'.format(new))
        image = new.strip()

@pack()
@SimpleButton(gui_main, text='Select output')
def select_save():
    global save
    new = asksaveasfilename(filetypes=[('.mkv files', '*.mkv')])
    if new and not new.isspace():
        if not new.endswith('.mkv'):
            new = '{}.mkv'.format(new)
        print('setting output file to {}'.format(new))
        save = new.strip()

@pack()
@SimpleButton(gui_main, text='Go')
def go():
    global running
    if not running:
        try:
            running = True
            if audio and image and save:
                main({
                    'face': image,
                    'audio': audio,
                    'outfile': save
                })
        finally:
            running = False


if __name__ == '__main__':
    gui_main()