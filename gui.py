# -*- coding: utf-8 -*-
from tkinter.filedialog import askopenfilename, asksaveasfilename
from simpletk import *
from inference import main, load_model
import tkinter
import torch

@SimpleMain()
async def gui_main():
    pass

audio = None
image = None
save = None
running = False


@grid(padx=15, pady=3, row=0, rowspan=5, column=1)
@SimpleText(gui_main)
def text():
    return '\n'.join([
        'GUI written by dunnousername#8672 (https://github.com/dunnousername/Wav2Lip)',
        'Wav2Lip originally by Rudrabha (https://github.com/Rudrabha/Wav2Lip)',
        'GUI Version 0.1.1'
    ]) + '\n'

@grid(padx=15, pady=3, row=0)
@SimpleButton(gui_main, text='Select audio')
def select_audio():
    global audio
    new = askopenfilename(filetypes=[('.wav files', '*.wav')])
    if new and not new.isspace():
        text('setting audio file to {}\n'.format(new))
        audio = new.strip()

@grid(padx=15, pady=3, row=1)
@SimpleButton(gui_main, text='Select image or video')
def select_image():
    global image
    new = askopenfilename(filetypes=[('image or video files', '*.png;*.jpg;*.jpeg;*.mp4;*.mkv;*.mov')])
    if new and not new.isspace():
        text('setting input file to {}\n'.format(new))
        image = new.strip()

@grid(padx=15, pady=3, row=2)
@SimpleButton(gui_main, text='Select output')
def select_save():
    global save
    new = asksaveasfilename(filetypes=[('.mp4 files', '*.mp4')])
    if new and not new.isspace():
        if not new.endswith('.mp4'):
            new = '{}.mp4'.format(new)
        text('setting output file to {}\n'.format(new))
        save = new.strip()

@grid(padx=15, pady=3, row=4)
@SimpleCheckbox(gui_main, text='Use GPU (disable if it causes issues)')
def use_cuda():
    return True

@grid(padx=15, pady=3, row=3)
@SimpleButton(gui_main, text='Go')
def go():
    global running
    if not running:
        device = 'cpu'
        if use_cuda:
            if torch.cuda.is_available():
                device = 'cuda'
            else:
                text('GPU not available! Using cpu instead.\n')
                use_cuda.set_checked(False)
        try:
            running = True
            text('Starting...\n')
            gui_main.update()
            if audio and image and save:
                main({
                    'face': image,
                    'audio': audio,
                    'outfile': save
                }, load_model('model/wav2lip.pth', device), device)
        except Exception as e:
            text('Got an error ({}); process failed!\n'.format(e))
            text('See full error log for details.\n')
            raise e
        else:
            text('Finished successfully!\n')
        finally:
            running = False

if __name__ == '__main__':
    gui_main()