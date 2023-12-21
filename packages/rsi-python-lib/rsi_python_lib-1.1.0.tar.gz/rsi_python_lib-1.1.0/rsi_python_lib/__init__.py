# -*- coding: utf-8 -*-

import logging

import rsi_python_lib.pySettaVars as pySettaVars
import rsi_python_lib.pyTools as pyTools
import rsi_python_lib.pyCueContenType as CCType
import rsi_python_lib.pyCueServices as cueServices
import rsi_python_lib.pyConfig as pyConfig

logger = logging.getLogger()

class rsi_lib:
	def __init__( self, prod_o_stag ):
		config = pyConfig.config( prod_o_stag )
		
