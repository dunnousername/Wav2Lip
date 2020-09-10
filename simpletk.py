# coding: utf-8
# this file (simpletk.py) was written by github user dunnousername, and is in the public domain.
# attribution is not required, however it would be nice.

import asyncio
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as tkst

class _AsyncTaskWrapper:
    def __init__(self, func):
        self.func = func
        self.task = None

    def __call__(self, *args, **kwargs):
        if not self.task or self.task.done():
            self.task = None
            return False
        self.task = asyncio.create_task(self.func(*args, **kwargs))
        return True

async_task_wrapper = _AsyncTaskWrapper

class AsyncTk(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.tasks = []
        self.tasks.append(self.loop.create_task(self.updater(1/120)))

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)

    def close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

    def start(self):
        self.loop.run_forever()

def pack(*args, **kwargs):
    def wrapper(element):
        element.tk.pack(*args, **kwargs)
        return element
    return wrapper

def grid(*args, **kwargs):
    def wrapper(element):
        element.tk.grid(*args, **kwargs)
        return element
    return wrapper

class SimpleTk:
    def __init__(self, master, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.tk = None
        self.master = master.tk if master else None

    def call(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        if not self.tk:
            self.tk = self.wrap(*args, *self.args, **kwargs, **self.kwargs)
            return self
        else:
            return self.call(*args, **kwargs)

class SimpleMain(SimpleTk):
    def __init__(self):
        super().__init__(None)

    def wrap(self, func):
        tk = AsyncTk()
        tk.tasks.append(tk.loop.create_task(func()))
        return tk

    def call(self):
        self.tk.start()

    def update(self):
        self.tk.update()

class SimpleButton(SimpleTk):
    def wrap(self, func, text='Button', stop_text=None):
        stop_text = stop_text or text
        element = ttk.Button(master=self.master, text=text)
        def wrapper():
            running = func()
            if running:
                element.config(text=stop_text)
            else:
                element.config(text=text)
        element.config(command=wrapper)
        return element

class SimpleText(SimpleTk):
    def wrap(self, func):
        text = func()
        _tk = tkst.ScrolledText(master=self.master)
        _tk.insert(tk.END, text)
        _tk.config(state=tk.DISABLED)
        return _tk

    def puts(self, text):
        self.tk.config(state=tk.NORMAL)
        self.tk.insert(tk.END, text)
        self.tk.config(state=tk.DISABLED)

    def clear(self):
        self.tk.config(state=tk.NORMAL)
        self.tk.delete(1.0, tk.END)
        self.tk.config(state=tk.DISABLED)

    def call(self, text):
        self.puts(text)

class SimpleCheckbox(SimpleTk):
    def wrap(self, func, text='Checkbox'):
        value = func()
        self.var = tk.IntVar()
        self.var.set(1 if bool(value) else 0)
        _tk = ttk.Checkbutton(master=self.master, text=text, variable=self.var)
        return _tk

    def get(self):
        return bool(self.var.get())

    def __bool__(self):
        return self.get()

    def call(self):
        return self.get()

    def set_checked(self, value):
        self.var.set(1 if bool(value) else 0)

# tests

#@SimpleMain()
#async def main():
#    while True:
#        print('Hello world!')
#        await asyncio.sleep(5)

#@pack()
#@SimpleButton(main, text='Test')
#def click():
#    print('Hello button!')

#main()