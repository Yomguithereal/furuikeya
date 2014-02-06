#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Furuikeya Command Line Hub
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependencies
#=============
import nltk.data
from colifrapy import Colifrapy
from model.controller import Controller


# Main Class
#=============
class Furuikeya(Colifrapy):

    def launch(self):

        # Verifying nltk resources
        nltk.data.path[0] = self.settings.nltk_data

        # Determining action
        if self.opts.saijiki:
            self.controller.generateSaijikiHaikus(self.opts.number)
        else:
            self.controller.generateMultipleHaikus(self.opts.kigo, self.opts.number)



# Launching
#===========
if __name__ == '__main__':
    hub = Furuikeya(Controller)
    hub.launch()
