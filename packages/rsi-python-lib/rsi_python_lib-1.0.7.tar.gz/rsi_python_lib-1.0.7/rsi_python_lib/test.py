
# -*- coding: utf-8 -*-


import logging
import logging.config

import os
import shutil
import json
import glob
import time

import rsi_python_lib.pySettaVars as pySettaVars
import rsi_python_lib.pyTools as pyTools
import rsi_python_lib.pyCueContenType as CCType
import rsi_python_lib.pyCueServices as cueServices

logger = logging.getLogger('pyCue')

if __name__ == "__main__":

	logger.debug('-\n')
	logger.debug('------------ INIT ---------- pyImpKeyTraffic.py ---------------------')
	#logger.debug(os.environ)


	logger.debug( '-\n')
	logger.debug( '------------ INIT ---------- pyKafkaParamTot.py.py ---------------------')
	#logger.debug( os.environ)

	# questa e per settare le veriabili di ambiente altrimenti come cron non andiamo da nessuna parte
	pyTools.SettaEnvironment( False )


	logFile = os.environ['LOGS_FILES'] + '/importKeyTraffic.log'

	logger.debug( '\n\n log configuration file : ' +  os.environ['LOGS_CONFIG_FILE'] + '\n')
	logging.config.fileConfig(os.environ['LOGS_CONFIG_FILE'], disable_existing_loggers=False, defaults={'logfilename': logFile})
	logger = logging.getLogger('pyMig')
	logger.debug( ' logging file : \t\t' + logger.handlers[0].baseFilename + '\n')
	logger.debug(pySettaVars.KAFKA_SERVERS)

	logger = logging.getLogger('pyMig')

	# qui ci sara la lista delle immagini da importare prese dall ftp
	lista_immagini = {}
	# qui la lista delle immagini importate ( se esistono )
	lista_importate = {}
	# qui la lista delle immagini presenti nel DB ( se esistono )
	items_da_db = {}

	# qui devo prendere quelle eventualmente ancora presenti nel DB
	logger.debug('prendo i valori dal DB = ' +  os.environ['DB_NAME'])
	[ lista_importate, lista_rimaste ] = Importa_Img( lista_immagini )
			# dove quelle importate hanno adesso la lista di CUE 
			# mentre le altre hanno ancora il path


	logger.debug('------------ END ---------- pyImpKeyTraffic.py ---------------------')
