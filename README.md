# Introduction

The Host Lookup Tool is a simple GUI implementation of `nslookup` in Python. It's aim is to assist with requests for multiple hosts. It can perform a `nslookup` for a single hostname or IP address or, when needed, multiple hostnames or IP addresses. It's primary aim is on the multiple hosts as performing `nslookup` on multiple hosts can be time consuming.

Keep in mind a few things please:

- I am a new/beginner python coder, don't be shocked if the code reflects that
- This is a work in progress that I am using to develop my python skills
- If you see something that would improve this, I appreciate any and all constructive criticism

I spent a great deal of time trying to find that _awesome_ project I could build from the ground up before I realized the value of just doing something with python. So I scaled my thinking back some and started looking at what I do day-to-day that I could potentially write code for whether it be work related or personal.

You'll find in my repositories a few projects with Microcontrollers using MicroPython. I absolutely **LOVE** those things. This repo, however, is something spawned from work related tasks. I also very much like creating GUI's for the tools I use. I don't have any issue using the command line, but I like creating the GUI's to have options for those that dont. This project is something of project of taking a commonly used command line tool and turning it into something GUI based.

[PySimpleGUI](https://pysimplegui.readthedocs.io/) is the framework that is being used for creating the GUI. I find it much easier and more friendly to use than [tkinter](https://docs.python.org/3/library/tkinter.html).

In my day-to-day work, I am often asked to verify whether or not hosts are in DNS. The list can occasionally be vast and some of the hosts in that list will be in DNS and some won't. Runnig `nslookup` one at a time over so many hosts seems like a perfect opportunity to create Python based tool to do that and do so with a GUI.

# Next Steps

There is lots of work to do here. I feel there are several opportunities to write this better. It works well as is, but this is also a tool for learning as well. In addition to that, I would very much love to package this up in a Windows executable so that it can be distributed not only amongst those that may find value in it, but also amongst those I work with who all use Windows.

# Build and Test

In progress

# Contribute

In progress
