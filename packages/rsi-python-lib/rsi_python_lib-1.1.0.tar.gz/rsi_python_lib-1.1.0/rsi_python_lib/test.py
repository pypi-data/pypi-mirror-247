# -*- coding: utf-8 -*-
import os

import logging

import rsi_python_lib
import rsi_python_lib.pySettaVars as pySettaVars
import rsi_python_lib.pyTools as pyTools
import rsi_python_lib.pyCueContenType as CCType
import rsi_python_lib.pyCueServices as cueServices

logger = logging.getLogger()
print(logger)

if __name__ == "__main__":

	logger.debug('-\n')
	logger.debug('------------ INIT ---------- test rsi_python_lib  ---------------------')
	#logger.debug(os.environ)

	newlib = rsi_python_lib.rsi_lib('STAG')
	print(os.environ)
	print()
	newlib = rsi_python_lib.rsi_lib('PROD')
	print(os.environ)

	resultBool = False
	[ resultBool, ct ] = CCType.MasterType( '2023056', None, None)
	if not resultBool :
		print('ERRORE')
		exit(0)
	ct.dumpDoc()
	logger.debug('------------ END ---------- test rsi_python_lib  ---------------------')
	exit(0)
