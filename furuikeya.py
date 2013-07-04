#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# -------------------------------------------------------------------
# Furuikeya Command Line Hub
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependancies
#=============
import nltk.data
from colifrapy import Settings, Commander
from model.controller import Controller

# Loading Colifrapy
settings = Settings()
settings.load()

# Verifying nltk resources
nltk.data.path[0] = settings.nltk_data

# Launching Controller
controller = Controller()
# print command

# Generating haikus
# if command.opts['number'] == 1:
# 	# controller.generateHaiku(command.opts['kigo'])
# 	pass
# else:
# 	print 'trop'
