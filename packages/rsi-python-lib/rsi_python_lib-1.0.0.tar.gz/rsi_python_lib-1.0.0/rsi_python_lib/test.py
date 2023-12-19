
# -*- coding: utf-8 -*-


import logging
import logging.config

import os
import shutil
import json
import glob
import time

import pySettaVars as pySettaVars

import pyTools as pyTools
import pyCueContenType as CCType
import pyCueServices as cueServices




def Prendi_Lista( workingDir ):

	result = {}
	
	lista_files = glob.glob( workingDir + '*.jpg' )
	lista_files = lista_files + glob.glob( workingDir + '*.JPG' )
	
	# dove trovo filenames del tipo : GP765997_P00000011_1.jpg
	# con ancora tutto il path
	# e a me interessano il primo campo = LegacyId
	# e il numero prima del . che rappresenta quanti ce ne sono per quel LegacyId

	for lis in lista_files:
		nome_file = os.path.basename(lis)
		logger.debug(nome_file)
		componenti = nome_file.split('_')
		if len(componenti) > 2:
			legacyId = componenti[0]
			progressivo = componenti[-1]
			if legacyId in result:
				result[legacyId].append(lis)
			else:
				result[legacyId] =  [lis]
			
	# qui restituisco un json tipo :
	# {'GP765997': ['/home/perucccl/Webservices/STAGING/ImportKeyFramesTraffic/Ftp_Dir/GP765997_P00000011_3.jpg', '/home/perucccl/Webservices/STAGING/ImportKeyFramesTraffic/Ftp_Dir/GP765997_P00000011_2.jpg'], 'GP765666': ['/home/perucccl/Webservices/STAGING/ImportKeyFramesTraffic/Ftp_Dir/GP765666_P00000011_2.jpg', '/home/perucccl/Webservices/STAGING/ImportKeyFramesTraffic/Ftp_Dir/GP765666_P00000011_1.jpg']}
	# nota il 3 che mi dice che probabilmente ne ho gia' importati 2 per quel legacy id

	return result



def Importa_Img( lista_immagini ):

	logger.debug('------------------------ INIT Importa_Img -------------- ')

	result = {}
	lista_rimaste = {}
	lista_archivio = []

	section = os.environ['IMPORT_SECTION']
	
	# dove trovo filenames del tipo : GP765997_P00000011_1.jpg
	# con ancora tutto il path
	# e a me interessano il primo campo = LegacyId
	# e il numero prima del . che rappresenta quanti ce ne sono per quel LegacyId

	for legacy, img in lista_immagini.items():
		# in img ho la lista di file_path che passo per upload del binary
		#logger.debug(legacy, img)
		message = {}
		for file_path in img:

			logger.debug( ' file path = ' + file_path )
		
			resultBool = False
			[ resultBool, binaryLocation ] = cueServices.uploadBinaryFromFile( file_path, legacy )
			if not resultBool :
				# non son riuscito a fare la load del file ....
				# continuo senza cambiare img con id
				if legacy in lista_rimaste:
					lista_rimaste[legacy].append(file_path)
				else:
					lista_rimaste[legacy] = [file_path]
				continue
				
			else:

				message['section'] = section
				message['contentType'] = 'picture'
				message['oldType'] = 'keyframe'
				message['title'] = legacy
				resultBool = False
				[ resultBool, newKeyframe ] = CCType.MasterType( None, None, message )
				newKeyframe.createDocument()
				newKeyframe.updateFields( message, newKeyframe.listaFields)

				newKeyframe.sistemaBinary( binaryLocation )
				newKeyframe.createState('published')
				newKeyframe.dumpDoc()
				[ resultBool, imageCueId ] = cueServices.createMamStr( message['section'], newKeyframe.getDoc())

				# ho fatto upload binary e in binary[1] ho la location url del binary
				# da passare alla creazione del content picture
				#result_crea = cueServices.createImg( binary[1] , legacy, section )
				
				if not resultBool:
					# con quel binary non sono riuscito a costruire un asset immagine
					if legacy in lista_rimaste:
						lista_rimaste[legacy].append(file_path)
					else:
						lista_rimaste[legacy] = [file_path]
					continue
				else:
					# ho creato img ed e andato tutto bene
					if legacy in result:
						result[legacy].append(imageCueId)
					else:
						result[legacy] =  [imageCueId]
				
					# e andato tutto bene posso spostarla nella directory di archiviazione
					# e la muovo in archived
					logger.debug( 'passo da sposta Img' )
					Sposta_Img( file_path )

	logger.debug( ' result = ' + str(result))
	logger.debug( ' rimaste = ' + str(lista_rimaste))
	logger.debug('------------------------ END Importa_Img -------------- ')

	return [ result , lista_rimaste ]

def Merge_Liste( lista_nuova, lista_old ):

	logger.debug('------------------------ INIT Merge_Liste -------------- ')
	result = {}
	

	try:
			
		result = lista_nuova.copy()
		
		for key, valueList in result.items():
			if key in lista_old:
				# in lista_old[ key ] ho una lista di CUE ID 
				# da aggiungere alla result[ key ] 
				for lis in lista_old[ key ]:
					result[ key ].append( lis )
		for key, valueList in lista_old.items():
			if key not in result:
				result[ key ] = valueList
				
	except Exception as e:
		logger.debug( 'PROBLEMI in Merge_Liste : ' + str(e) )
		return {}


	logger.debug( ' result = ' + str(result))
	logger.debug('------------------------ finisce Merge_Liste -------------- ')
	return result

def Sposta_Img(  file_path ):
	
	logger.debug('------------------------ INIT Sposta_Img -------------- ')
	try:
		file_name = os.path.basename( file_path )
		logger.debug( "mv " + file_path + " to -> " + os.environ['FTP_ARCHIVE_DIR'] + file_name )
		shutil.move( file_path,  os.environ['FTP_ARCHIVE_DIR'] + file_name )
		
	except Exception as e:
		logger.error('ERROR: EXCEPT in Sposta_Img  = ' + str(e))
		logger.error('ERROR: EXCEPT in Sposta_Img per immagine = ' + file_path)
		pass

	logger.debug('------------------------ END Sposta_Img -------------- ')


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
