# -*- coding: utf-8 -*-

import os
import logging
import urllib.request, urllib.error, urllib.parse
import requests
import base64
from xml.dom import minidom
import xml.etree.ElementTree as ET
import codecs
import json
import os
from http.client import HTTPSConnection
from base64 import b64encode

# importa re per fare le regular espression che effettuano i cambiamenti nel xml
import re

import rsi_python_lib.pyTools as pyTools

# debug setting
http_handler = urllib.request.HTTPHandler(debuglevel=1)
# mettere a 1 per vedere cosa mandiamo con le chiamate

try:
	import ssl
	https_handler = urllib.request.HTTPSHandler(debuglevel=0)
	opener = urllib.request.build_opener(http_handler, https_handler)
except ImportError:
	opener = urllib.request.build_opener(http_handler)

urllib.request.install_opener(opener)



logger = logging.getLogger()

# definizione dei namespaces per parsare gli atom
namespaces = { 'atom':'{http://www.w3.org/2005/Atom}',
               'dcterms' : '{http://purl.org/dc/terms/}',
                'mam' : '{http://www.vizrt.com/2010/mam}',
                'age' : '{http://purl.org/atompub/age/1.0}',
                'opensearch' : '{http://a9.com/-/spec/opensearch/1.1/}',
                'vaext' : '{http://www.vizrt.com/atom-ext}',
                'app' : '{http://www.w3.org/2007/app}',
                'vdf' : '{http://www.vizrt.com/types}',
                'metadata' : '{http://xmlns.escenic.com/2010/atom-metadata}',
                #'': '{http://www.w3.org/1999/xhtml}',
                'playout' : '{http://ns.vizrt.com/ardome/playout}' }
userContent = {
        "programmeVideo":"TSMM-MPV",
        "mamProgrammeVideo":"TSMM-MPV",
        "segmentedProgrammeVideo":"TSMM-MSV",
        "segmentAudio":"TSMM-MTA",
        "mamSegmentedProgrammeVideo":"TSMM-MSV",
        "transcodableVideo":"TSMM-MTV",
        "mamTranscodableVideo":"TSMM-MTV",
        "transcodableAudio":"TSMM-MTA",
        "mamTranscodableAudio":"TSMM-MTA",
        "livestreaming":"TSMM-MLS",
        "programme":"TSMM-MP",
        "mamProgramme":"TSMM-MP",
        "keyframe":"TSMM-MK",
        "delete":"TSMM-MD"
}

_UPDATE_FUNC_ = 0
_CREATE_FUNC_ = 1
_SISTEMA_FUNC_ = 2

for entry in namespaces:
        #logger.debug(entry, namespaces[entry])
        ET._namespace_map[namespaces[entry].replace('{','').replace('}','')] = entry

def Dump_Link ( link, filename ):

        auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
        base64string = b64encode(auth.encode())
        base64string = base64string.decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  base64string }

        logger.debug (link )
        logger.debug (filename)

        try:
                request = urllib.request.Request(link, headers=headers)
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        xml = minidom.parse(resultResponse)
                fout = codecs.open(filename, 'w', 'utf-8')
                fout.write( xml.toxml() )
                fout.close()

        except Exception as e:
                logger.debug ( 'PROBLEMI in Dump_Link ' + str(e) )
                pass
        return

def Dump_ET_Link ( idStr, filename ):

        auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
        base64string = b64encode(auth.encode())
        base64string = base64string.decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  base64string }

        link = os.environ['CUE_CONTENT']  + str(idStr)

        logger.debug (idStr )
        logger.debug (link )
        logger.debug (filename)
        try:
                request = urllib.request.Request(link, headers=headers)
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        xml = minidom.parse(resultResponse)
                tree = ET.parse(resultResponse)
                #logger.debug ( ET.tostring( tree.getroot() ))
                tree.write(filename)

        except Exception as e:
                logger.debug ( 'PROBLEMI in Dump_ET_Link : ' + str(e) )
                pass

        return

def putLink( link, filename ):

        logger.info('------------------------ inizia putLink -------------- ')

        auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
        base64string = b64encode(auth.encode())
        base64string = base64string.decode("ascii")
        headers = { 'Authorization' : 'Basic %s' %  base64string }
        file = open(filename)
        dati = file.read()

        request = urllib.request.Request(link, data=dati)

        request.add_header("Authorization", "Basic %s" % base64string)
        request.add_header('If-Match', '*')
        request.add_header('Content-Type', 'application/atom+xml')
        request.get_method = lambda: 'PUT'
        #result = urllib.request.urlopen(request)
        with urllib.request.urlopen(request) as result:
                xml = minidom.parse(result)

        #logger.debug(result.read())
        return
        xml = minidom.parse(result)
        fout = codecs.open(filename, 'w', 'utf-8')
        fout.write( xml.toxml() )
        fout.close()


        return

def putIdProd( idx, filename ):

        logger.info('------------------------ inizia putIdProd -------------- ')
        try:
                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")
                headers = { 'Authorization' : 'Basic %s' %  base64string }

                with open( filename ,'r') as fin:
                        dati=fin.read()
                link = os.environ['CUE_CONTENT']  + str(idx)

                request = urllib.request.Request(link, data=dati)

                request.add_header("Authorization", "Basic %s" % base64string)
                request.add_header('If-Match', '*')
                request.add_header('Content-Type', 'application/atom+xml')
                request.get_method = lambda: 'PUT'
                #result = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as result:
                        xml = minidom.parse(result)

                logger.debug('putIdProd' )
                logger.debug(result.read())


        except Exception as e:
                logger.debug ( 'PROBLEMI in putIdProd : ' + str(e) )
                logger.warning( 'PROBLEMI in putIdProd : ' + str(e) )
                return False

        logger.info('------------------------ finisce putIdProd -------------- ')
        return True

class NoRedirect(urllib.request.HTTPRedirectHandler):
	def redirect_request(self, req, fp, code, msg, headers, newurl):
	
		auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		headers = { 'Authorization' : 'Basic %s' % base64string,
		#'If-Match': '*',
		'Content-Type': 'text/plain; charset=utf-8'
		}

		logger.debug('in redirect_request')
		logger.debug( headers )
		logger.debug( req.data )
		logger.debug( req.method )
		logger.debug( newurl )
		#logger.debug( fp )
		if code == 301:
			redirect = urllib.request.Request(url=newurl, data=req.data, headers=headers, method='POST')
			logger.debug( code )
			#chiama newurl 
			with urllib.request.urlopen(redirect) as resultResponse:
				logger.debug ( resultResponse.status )
				logger.debug ( resultResponse.headers )
				#logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
		#logger.debug( msg )
		#logger.debug( newurl )
		return None


def putSectionParameters( sectionPath, filename ):

	logger.debug('------------------------ inizia putSectionParameters -------------- ')
	logger.info('------------------------ inizia putSectionParameters -------------- ')
	try:

		auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		headers = { 'Authorization' : 'Basic %s' % base64string,
		#'If-Match': '*',
		'Content-Type': 'text/plain; charset=utf-8'
		}

		with open( filename ,'r') as fin:
			dati=fin.read()

		#logger.debug ( dati ) 
		#dati = html.escape(dati)
		dati =  dati.encode('ISO-8859-1', 'ignore')
		#dati =  dati.encode()
		#logger.debug ( bytes(dati, 'utf-8') ) 
		#logger.debug(dati.encode('utf-8'))
		#logger.debug(dati.encode('ascii', 'ignore'))
		
		link = os.environ['CUE_SECTION_PARAMETERS']  + sectionPath
		logger.debug ( link )

		request = urllib.request.Request(url=link, data=dati, headers=headers, method='POST')
		#resultResponse = urllib.request.urlopen(request)

		#opener = urllib.request.build_opener(NoRedirect)
		#urllib.request.install_opener(opener)

		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.headers )
			#logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
			logger.debug ( resultResponse.reason )


	except Exception as e:
		logger.debug ( 'PROBLEMI in putSectionParameters : ' + str(e) )
		logger.warning( 'PROBLEMI in putSectionParameters : ' + str(e) )
		return False

	logger.info('------------------------ finisce putSectionParameters -------------- ')
	return True




def putSectionId( idx, filename ):

        logger.debug('------------------------ inizia putSectionId -------------- ')
        logger.info('------------------------ inizia putSectionId -------------- ')
        try:
                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'If-Match': '*',
                                'Content-Type': 'application/atom+xml'
                        }

                with open( filename ,'r') as fin:
                        dati=fin.read()
                dati = ( dati ).encode()
                link = os.environ['CUE_SECTION']  + str(idx)
                logger.debug ( link )

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='PUT')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        logger.debug ( resultResponse.reason )


        except Exception as e:
                logger.debug ( 'PROBLEMI in putSectionId : ' + str(e) )
                logger.warning( 'PROBLEMI in putSectionId : ' + str(e) )
                return False

        logger.info('------------------------ finisce putSectionId -------------- ')
        return True

def putIdStr( idx, xmlStr ):

        logger.debug('------------------------ inizia putIdStr -------------- ')
        logger.info('------------------------ inizia putIdStr -------------- ')
        try:
                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'If-Match': '*',
                                'Content-Type': 'application/atom+xml'
                        }

                dati = xmlStr
                link = os.environ['CUE_CONTENT']  + str(idx)
                logger.debug ( link )

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='PUT')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        logger.debug ( resultResponse.reason )


        except Exception as e:
                logger.debug ( 'PROBLEMI in putIdStr : ' + str(e) )
                logger.warning( 'PROBLEMI in putIdStr : ' + str(e) )
                return False

        logger.info('------------------------ finisce putIdStr -------------- ')
        return True



def putIdeTag( idx, filename, eTag ):

        logger.debug('------------------------ inizia putId -------------- ')
        logger.info('------------------------ inizia putId -------------- ')
        try:
                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'If-Match':  eTag ,
                                'Content-Type': 'application/atom+xml;type=entry'
                        }

                #logger.debug ( headers )

                with open( filename ,'r') as fin:
                        dati=fin.read()
                dati = ( dati ).encode()
                link = os.environ['CUE_CONTENT']  + str(idx)
                logger.debug ( link )

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='PUT')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        logger.debug ( resultResponse.reason )


        except Exception as e:
                logger.debug ( 'PROBLEMI in putId : ' + str(e) )
                logger.warning( 'PROBLEMI in putId : ' + str(e) )
                return False

        logger.info('------------------------ finisce putId -------------- ')
        return True






def putId( idx, filename ):

        logger.debug('------------------------ inizia putId -------------- ')
        logger.info('------------------------ inizia putId -------------- ')
        try:
                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'If-Match': '*',
                                'Content-Type': 'application/atom+xml'
                        }

                with open( filename ,'r') as fin:
                        dati=fin.read()
                dati = ( dati ).encode()
                link = os.environ['CUE_CONTENT']  + str(idx)
                logger.debug ( link )

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='PUT')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        logger.debug ( resultResponse.reason )


        except Exception as e:
                logger.debug ( 'PROBLEMI in putId : ' + str(e) )
                logger.warning( 'PROBLEMI in putId : ' + str(e) )
                return False

        logger.info('------------------------ finisce putId -------------- ')
        return True



def deleteId( idx ):

        logger.debug('------------------------ inizia deleteId -------------- ')
        logger.info('------------------------ inizia deleteId -------------- ')
        try:
                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string
                        }

                link = os.environ['CUE_CONTENT']  + str(idx)
                logger.debug ( link )

                request = urllib.request.Request(url=link, headers=headers, method='DELETE')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        logger.debug ( resultResponse.reason )


        except Exception as e:
                logger.debug ( 'PROBLEMI in deleteId : ' + str(e) )
                logger.warning( 'PROBLEMI in deleteId : ' + str(e) )
                return False

        logger.info('------------------------ finisce deleteId -------------- ')
        return True


def getSection( eceSection ):
        logger.debug ( '------------------------ CUE inizia getSection -------------- ' )
        logger.debug ( '------------------------ CUE inizia getSection -------------- ' )
        result=[ False, None ]

        try:

                link = os.environ['CUE_SECTION']  + str(eceSection)
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'Content-Type': 'application/atom+xml'
                        }

                request = urllib.request.Request(url=link, headers=headers, method='GET')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('Location') )

                        resultStr = resultResponse.read()
                #tree.write('newx.xml')
                #exit(0)
                #ET.dump(tree)

                #title =  PrendiField( tree, "title")
                #logger.debug(title)
                #programmeId =  PrendiField( tree, "programmeId")
                #logger.debug(programmeId)

        except urllib.error.HTTPError as e:
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                return [ False, str(e) ]

        logger.debug ( '------------------------ END getSection -------------- ' )
        logger.debug ( '------------------------ END getSection -------------- ' )

        return [ True, resultStr.decode('utf-8')]



def getSubSections( subSectionsUrl ):
        logger.debug ( '------------------------ inizia getSubSections -------------- ' )
        logger.debug ( '------------------------ inizia getSubSections -------------- ' )
        result=None

        try:
                link = subSectionsUrl
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'Content-Type': 'application/atom+xml'
                        }

                request = urllib.request.Request(url=link, headers=headers, method='GET')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('Location') )

                        resultStr = resultResponse.read()

        except urllib.error.HTTPError as e:
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                return str(e)

        logger.debug ( '------------------------ END getSubSections -------------- ' )
        logger.debug ( '------------------------ END getSubSections -------------- ' )

        return resultStr



def getSectionDouble( eceSection ):
        logger.debug ( '------------------------ inizia getSectionDouble -------------- ' )
        logger.debug ( '------------------------ inizia getSectionDouble -------------- ' )
        result=[ False, None ]

        try:
                link = os.environ['CUE_SECTION']  + str(eceSection)
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'Content-Type': 'application/atom+xml'
                        }

                request = urllib.request.Request(url=link, headers=headers, method='GET')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('Location') )

                        resultStr = resultResponse.read()
                        tree = ET.fromstring(resultStr)
                        logger.debug(tree)
                        xml = minidom.parseString( resultStr )
                        resultXml = xml.toxml()
                        logger.debug(resultXml)
                #tree.write('newx.xml')
                #exit(0)
                #ET.dump(tree)

                #title =  PrendiField( tree, "title")
                #logger.debug(title)
                #programmeId =  PrendiField( tree, "programmeId")
                #logger.debug(programmeId)

        except urllib.error.HTTPError as e:
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                return [ False, str(e), str(e) ]

        logger.debug ( '------------------------ END getSectionDouble -------------- ' )
        logger.debug ( '------------------------ END getSectionDouble -------------- ' )

        return [ True, tree, resultXml ]



def getIdDouble( eceId ):
        logger.debug ( '------------------------ inizia getIdDouble -------------- ' )
        logger.debug ( '------------------------ inizia getIdDouble -------------- ' )
        result=[ False, None ]

        try:
                link = os.environ['CUE_CONTENT']  + str(eceId)
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'Content-Type': 'application/atom+xml'
                        }

                request = urllib.request.Request(url=link, headers=headers, method='GET')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('Location') )

                        resultStr = resultResponse.read()
                        tree = ET.fromstring(resultStr)
                        logger.debug(tree)
                        xml = minidom.parseString( resultStr )
                        resultXml = xml.toxml()
                        logger.debug(resultXml)
                #tree.write('newx.xml')
                #exit(0)
                #ET.dump(tree)

                #title =  PrendiField( tree, "title")
                #logger.debug(title)
                #programmeId =  PrendiField( tree, "programmeId")
                #logger.debug(programmeId)

        except urllib.error.HTTPError as e:
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                return [ False, str(e), str(e) ]

        logger.debug ( '------------------------ END getIdDouble -------------- ' )
        logger.debug ( '------------------------ END getIdDouble -------------- ' )

        return [ True, tree, resultXml ]

def getIdTree( eceId ):
        logger.debug ( '------------------------ inizia getIdTree -------------- ' )
        logger.debug ( '------------------------ inizia getIdTree -------------- ' )
        result=[ False, None ]

        try:
                link = os.environ['CUE_CONTENT']  + str(eceId)
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'Content-Type': 'application/atom+xml'
                        }

                request = urllib.request.Request(url=link, headers=headers, method='GET')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('Location') )

                        tree = ET.parse(resultResponse)
                #logger.debug ( tree )
                #logger.debug ( type(tree))
                result = tree
                #tree.write('newx.xml')
                #exit(0)
                #ET.dump(tree)

                #title =  PrendiField( tree, "title")
                #logger.debug(title)
                #programmeId =  PrendiField( tree, "programmeId")
                #logger.debug(programmeId)

        except urllib.error.HTTPError as e:
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ')
                return [ False, str(e) ]

        logger.debug ( '------------------------ END getIdTree -------------- ' )
        logger.debug ( '------------------------ END getIdTree -------------- ' )

        return [ True, result ]




def getId( eceId ):
        logger.debug ( '------------------------ inizia getId -------------- ' )
        logger.debug ( 'C------------------------ inizia getId -------------- ' )
        result=[ False, None ]

        try:
                link = os.environ['CUE_CONTENT']  + str(eceId)
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                headers = { 'Authorization' : 'Basic %s' % base64string,
                                'Content-Type': 'application/atom+xml'
                        }

                request = urllib.request.Request(url=link, headers=headers, method='GET')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse )
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.headers )
                        logger.debug ( resultResponse.getheader('ETag') )
                        eTag =  resultResponse.getheader('ETag') 
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('Location') )

                        result = resultResponse.read()
                #logger.debug(result)

        except urllib.error.HTTPError as e:
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ' + str(e))
                logger.debug(' EXCEPTIOOOONNNNNN - ritorno none !!!! ' + str(e))
                return [ False, str(e), None ]

        logger.debug ( '------------------------ END getId -------------- ' )
        logger.debug ( '------------------------ END getId -------------- ' )

        return [ True, result.decode('utf-8'), eTag ]


def createImg( binaryUrl, titolo, section ):

        logger.debug( '------------------------ inizia createImg -------------- ' )
        logger.debug( '------------------------ inizia createImg -------------- ' )

        result = [False, '']

        # che deve fare la  curl --include -u perucccl:perucccl -X POST -H "Content-Type: application/atom+xml"
        # http://internal.publishing.production.rsi.ch/webservice/escenic/section/__CREATE_SECTION__/content-items
        # --upload-file Resources/template_picture.xml
        # dove __CREATE_SECTION__ deve essere cambiato con section e il file template deve essere aggiornato con i valori
        # dei parametri

        #try:
        link =  os.environ['IMG_CREATE_URL'].replace('__CREATE_SECTION__', section )
        logger.debug( 'link : ' + link )
        logger.debug ( 'link : ' + link )
        logger.debug ( 'link : ' + link )

        # apro il template file


        logger.debug ( 'binaryUrl : ' + binaryUrl )
        logger.debug ( 'binaryUrl : ' + binaryUrl )
        logger.debug ( 'titolo : ' + titolo )
        logger.debug ( 'titolo : ' + titolo )

        auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
        base64string = b64encode(auth.encode())
        base64string = base64string.decode("ascii")

        headers = { 'Authorization' : 'Basic %s' % base64string,
                        'Content-Type': 'application/atom+xml'
                }

        #logger.debug (  os.environ['IMG_RESOURCE_TEMPLATE'] )
        #logger.debug (  os.environ['IMG_RESOURCE_TEMPLATE'] )
        with open( os.environ['IMG_RESOURCE_TEMPLATE'] ,'r') as fin:
                dati=fin.read()
        #logger.debug ( dati )
        #logger.debug ( dati )


        #dati = dati.replace('__CREATE_SECTION__', section )
        dati = dati.replace('__TITOLO_PICTURE__', titolo )
        dati = dati.replace('__ECE_MODEL__', os.environ['CUE_MODEL'] )
        dati = dati.replace('__BINARY_LOCATION__', binaryUrl )

        #logger.debug ( ' data da mandare --> ' + dati )
        #logger.debug ( ' data  = ' + dati )
        dati = ( dati ).encode()

        try:
                request = urllib.request.Request(url=link, data=dati, headers=headers, method='POST')
                resultResponse = urllib.request.urlopen(request)
                logger.debug ( resultResponse.status )
                logger.debug ( resultResponse.status )
        except Exception as e:
                logger.debug ( 'PROBLEMI in createImg : ' + str(e) )
                logger.debug ( 'PROBLEMI in prendiS3Img : ' + str(e) )
                return [ False, { 'error' : str(e) } ]
        if  201 == resultResponse.status:
                #logger.debug ( 'tutto ok ' )
                logger.debug ( resultResponse.getheader('Location') )
                logger.debug ( resultResponse.getheader('Location') )
                #logger.debug ( resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1]  )
                return [ True, resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1] ]
        else:
                return [ False, resultResponse.status ]
        #logger.debug ( resultResponse.headers )
        #logger.debug ( resultResponse.headers )
        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
        #logger.debug ( resultResponse.reason )
        #logger.debug ( resultResponse.getheader('ocation') )
        #for lis  in resultResponse.getheaders():
                #logger.debug ( lis )
                #logger.debug (type(lis))

        '''
        except Exception as e:
                logger.debug( 'PROBLEMI in createImg : ' + str(e) )
                return [False, '' ]
        '''

        logger.debug('------------------------ finisce createImg -------------- ')
        logger.debug('------------------------ finisce createImg -------------- ')
        return result

def uploadBinaryFromBin( binData , title):

        logger.debug(" ---------------------- INIT uploadBinaryFromBin CLAD ------------------ " )
        logger.debug(" ---------------------- INIT uploadBinaryFromBin CLAD ------------------ " )
        result = [False, '']
        url = os.environ['CUE_BINARY']
        logger.debug( 'url per upload : ' + url )
        logger.debug( 'url per upload : ' + url )

        try:

                link =  url
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                #xmlStr = urllib.parse.urlencode(xmlStr).encode("utf-8")

                headers = { 'Authorization' : 'Basic %s' %  base64string ,
                          'Content-Type':'image/jpeg',
			  'x-escenic-media-filename': title
		}
                dati=binData

                #logger.debug( ' data  = ' + dati  )
                # probabilmente non necessario
                #dati = ( dati ).encode()

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='POST')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        if  201 == resultResponse.status:
                                #logger.debug ( 'tutto ok ' )
                                logger.debug ( 'Location = ' + resultResponse.getheader('Location') )
                                #logger.debug ( resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1]  )
                                return [ True, resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1] ]
                        else:
                                return [ False, resultResponse.status ]
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('ocation') )
                        #for lis  in resultResponse.getheaders():
                                #logger.debug ( lis )
                                #logger.debug (type(lis))

        except Exception as e:
                logger.debug( 'PROBLEMI in uploadBinaryFromBin: ' + str(e)  )
                logger.error('ERROR: EXCEPT in uploadBinaryFromBin  = ' + str(e))
                return [False, str(e) ]


        logger.debug(" ---------------------- FINE uploadBinaryFromBin ------------------ " )
        logger.debug(" ---------------------- FINE uploadBinaryFromBin ------------------ " )
        return result

def uploadBinaryFromFile( file_path , title):

        logger.debug(" ---------------------- INIT uploadBinaryFromFile CLAD ------------------ " )
        logger.debug(" ---------------------- INIT uploadBinaryFromFile CLAD ------------------ " )
        result = [False, '']
        url = os.environ['CUE_BINARY']
        logger.debug( 'url per upload : ' + url )
        logger.debug( 'file path per upload : ' + file_path )
        logger.debug( 'url per upload : ' + url )
        logger.debug( 'file path per upload : ' + file_path  )
        logger.debug( 'title : ' + title  )

        try:

                link =  url
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                #xmlStr = urllib.parse.urlencode(xmlStr).encode("utf-8")

                headers = { 'Authorization' : 'Basic %s' %  base64string ,
                          'Content-Type':'image/jpeg',
			  'x-escenic-media-filename': title  + '.jpg'
		}

                with open( file_path ,'rb') as fin:
                        dati=fin.read()

                #logger.debug( ' data  = ' + dati  )
                # probabilmente non necessario
                #dati = ( dati ).encode()

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='POST')
                #resultResponse = urllib.request.urlopen(request)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        if  201 == resultResponse.status:
                                #logger.debug ( 'tutto ok ' )
                                logger.debug ( resultResponse.getheader('Location') )
                                #logger.debug ( resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1]  )
                                return [ True, resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1] ]
                        else:
                                return [ False, resultResponse.status ]
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('ocation') )
                        #for lis  in resultResponse.getheaders():
                                #logger.debug ( lis )
                                #logger.debug (type(lis))

        except Exception as e:
                logger.debug( 'PROBLEMI in uploadBinaryFromFile: ' + str(e)  )
                logger.error('ERROR: EXCEPT in uploadBinaryFromFile  = ' + str(e))
                return [False, str(e) ]


        logger.debug(" ---------------------- FINE uploadBinaryFromFile ------------------ " )
        return result


def createMamStr( section, xmlStr ):


        logger.debug( '------------------------ INIT createMamStr -------------- '  )
        logger.debug( '------------------------ INIT createMamStr -------------- '  )

        result = [False, '']

        # che deve fare la  curl --include -u perucccl:perucccl -X POST -H "Content-Type: application/atom+xml"
        # http://internal.publishing.production.rsi.ch/webservice/escenic/section/__CREATE_SECTION__/content-items
        # --upload-file Resources/template_mamProgramme.xml
        # dove __CREATE_SECTION__ deve essere cambiato con section e il file template deve essere aggiornato con i valori
        # dei parametri

        try:

                link =  os.environ['CUE_CREATE_URL'].replace('__CREATE_SECTION__', section )
                #link =  "http://internal.publishing.staging.rsi.ch/webservice/escenic/section/5909/content-items"
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                #xmlStr = urllib.parse.urlencode(xmlStr).encode("utf-8")

                headers = { 'Authorization' : 'Basic %s' %  base64string ,
                          'Content-Type':'application/atom+xml'}



                dati = xmlStr.replace('__ECE_MODEL__', os.environ['CUE_MODEL'] )

                logger.debug( ' data  = ' + dati  )
                logger.debug( ' data  = ' + dati  )
                dati = ( dati ).encode()

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='POST')
                #resultResponse = urllib.request.urlopen(request, timeout=3000)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        #logger.debug ( resultResponse.getheader('Location') )

                        if  201 == resultResponse.status:
                                #logger.debug ( 'tutto ok ' )
                                #logger.debug ( resultResponse.getheader('Location') )
                                #logger.debug ( resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1]  )
                                return [ True, resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1] ]
                        else:
                                return [ False, resultResponse.status ]
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers )
                        #logger.debug ( resultResponse.headers.split('rsi.ch/webservice/escenic/content/' )[-1] )
                        #logger.debug ( resultResponse.reason )
                        #logger.debug ( resultResponse.getheader('ocation') )
                        #for lis  in resultResponse.getheaders():
                                #logger.debug ( lis )
                                #logger.debug (type(lis))


        except Exception as e:
                logger.debug( 'PROBLEMI in createMamStr: ' + str(e)  )
                logger.debug( 'PROBLEMI in createMamStr: ' + str(e)  )
                return [False, str(e) ]

        logger.debug('------------------------ END createMamStr-------------- ' )
        logger.debug('------------------------ END createMamStr-------------- ' )
        return result

def createSectionStr( xmlStr ):

        logger.debug( '------------------------ INIT createSectionStr -------------- '  )
        logger.debug( '------------------------ INIT createSectionStr -------------- '  )

        result = [False, '']

        # che deve fare la curl --include -u rsi_admin:admin -X POST  -H "Content-Type: application/atom+xml" 
	# http://10.101.8.38:8080/webservice/escenic/section --upload-file Resources/template_section.xml
        # dove __CREATE_SECTION__ deve essere cambiato con section e il file template deve essere aggiornato con i valori
        # dei parametri

        #try:
        if True:

                link =  os.environ['CUE_SECTION']
                #link =  "http://internal.publishing.staging.rsi.ch/webservice/escenic/section/"
                logger.debug( 'link : ' + link  )
                logger.debug( 'link : ' + link  )

                auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
                base64string = b64encode(auth.encode())
                base64string = base64string.decode("ascii")

                #xmlStr = urllib.parse.urlencode(xmlStr).encode("utf-8")

                headers = { 'Authorization' : 'Basic %s' %  base64string ,
                          'Content-Type':'application/atom+xml'}

                dati = xmlStr

                logger.debug( ' data  =' + dati  )
                logger.debug( ' data  =' + dati  )
                dati = ( dati ).encode()

                request = urllib.request.Request(url=link, data=dati, headers=headers, method='POST')
                #resultResponse = urllib.request.urlopen(request, timeout=3000)
                with urllib.request.urlopen(request) as resultResponse:
                        logger.debug ( resultResponse.status )
                        logger.debug ( resultResponse.status )
                        #logger.debug ( resultResponse.getheader('Location') )

                        if  201 == resultResponse.status:
                                logger.debug ( 'tutto ok ' )
                                logger.debug ( resultResponse.getheader('Location') )
                                #logger.debug ( resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1]  )
				#for lis  in resultResponse.getheaders():
					#logger.debug ( lis )
					#logger.debug (type(lis))
                                return [ True, resultResponse.getheader('Location').split('webservice/escenic/section/' )[-1] ]
                        else:

                                logger.debug ( 'NO ok ' )
                                return [ False, resultResponse.status ]


        '''
        except Exception as e:
                logger.debug( 'PROBLEMI in createSectionStr: ' + str(e)  )
                logger.debug( 'PROBLEMI in createSectionStr: ' + str(e)  )
                return [False, str(e) ]

        '''
        logger.debug('------------------------ END createSectionStr-------------- ' )
        logger.debug('------------------------ END createSectionStr-------------- ' )
        return result

def createSectionFromFile( filename ):

	logger.debug('------------------------ inizia createSectionFromFile -------------- ')
	logger.info('------------------------ inizia createSectionFromFile -------------- ')
	try:
	#if True:
		auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		with open( filename ,'r') as fin:
			dati=fin.read()

		dati = ( dati ).encode()
		logger.debug(dati)
		link = os.environ['CUE_SECTION']
		logger.debug ( link )

		request = urllib.request.Request(url=link, data=dati, headers=headers, method='POST')
		#resultResponse = urllib.request.urlopen(request)
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			if 201 == resultResponse.status:
				logger.debug ( resultResponse.getheader('Location') )
				location =  resultResponse.getheader('Location')
				logger.debug( location.split('webservice/escenic/section/'))
				location = location.split('webservice/escenic/section/')[-1]
				return [ True, location ]
			else:
				logger.debug ( 'No ok')
				return [ False,  resultResponse.status ]

	
	except Exception as e:
		logger.debug ( 'PROBLEMI in createSectionFromFile : ' + str(e) )
		logger.warning( 'PROBLEMI in createSectionFromFile : ' + str(e) )
		return [ False, str(e) ]


	logger.info('------------------------ finisce createSectionFromFile -------------- ')
	return [ False, 'NONZO']




def deleteSection( sectionId ):

	logger.debug( '------------------------ INIT deleteSection -------------- '  )
	logger.debug( '------------------------ INIT deleteSection -------------- '  )

	result = [False, '']

	# che dovrebbe fare la curl --include -u rsi_admin:admin -X DELETE
	# http://10.101.8.38:8080/webservice/escenic/section/sectionId
	# da cui riceve 303 con nel Location Header la risorsa di delete
	# generalmente qualcosa tipo : http://10.101.8.38:8080/webservice/escenic/section/sectionId/delete 
	# seguendo il link si prende la url in model che mi permette di compilare il mio 
	# template_section_delete.xml con la sostituzione di __DELETE_URL__ con 
	# http://10.101.8.38:8080/webservice/escenic/model/cpm-escenic.section.delete.sectionID e fare una PUT su
	# quella url appena presa : 
	# http://10.101.8.38:8080/webservice/escenic/section/sectionId/delete

	# ma invece chiama semplicemente la 
	# curl --include -u rsi_admin:admin -X PUT 
	# -H "Content-Type: application/atom+xml"  
	# os.environ['CUE_SECTION'] + /sectionID/delete  --upload-file template_section_deletete.xml
	# a cui ha cambiato il valore di __SECTION_ID__ con sectionId
	# e __CUE_MODEL__ con os.environ['CUE_MODEL']

	try:

		auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		headers = { 'Authorization' : 'Basic %s' %  base64string ,
		'Content-Type':'application/atom+xml'}

		filename = os.environ['RESOURCE_DIR'] + "template_section_delete.xml"
		with open( filename ,'r') as fin:
			dati=fin.read()
		dati = dati.replace( '__SECTION_ID__', sectionId )
		dati = dati.replace( '__CUE_MODEL__', os.environ['CUE_MODEL'] )
		dati = ( dati ).encode()
		logger.debug( dati )

		linkDelete = os.environ['CUE_SECTION'] +  sectionId + '/delete'
		logger.debug ( 'linkDelete = ' + linkDelete )
		request = urllib.request.Request(url=linkDelete, data=dati, headers=headers, method='PUT')
		#resultResponse = urllib.request.urlopen(request, timeout=3000)
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			#logger.debug ( resultResponse.getheader('Location') )

			if  204 == resultResponse.status:
				logger.debug ( 'tutto ok ' )
				logger.debug('Section : ' + sectionId + ' - cancellata' )
				#logger.debug ( resultResponse.getheader('Location') )
				#logger.debug ( resultResponse.getheader('Location').split('rsi.ch/webservice/escenic/content/' )[-1]  )
				return [ True, 'Section : ' + sectionId + ' - cancellata' ]
			else:
				if 301 == resultResponse.status:
					logger.debug ( resultResponse.getheader('Location') )
					exit(0)
					
				return [ False, resultResponse.status ]
	except Exception as e:
		logger.debug( 'PROBLEMI in deleteSection: ' + str(e)  )
		logger.debug( 'PROBLEMI in deleteSection: ' + str(e)  )
		return [False, str(e) ]

	logger.debug('------------------------ END deleteSection-------------- ' )
	logger.debug('------------------------ END deleteSection-------------- ' )
	return result

def getIdServizioSezioniEce( channel, sectionName, result ) :

	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	# funzione per prendere il numero di sezione partendo dal nome 
	# trovato nel serie- titlepress
	# modificato come segue:
	# tutti i caratteri devono essere trasformati in minuscolo
	brand = sectionName.lower()
	# replace dei caratteri accentati con i caratteri semplici. es. Fal --> brand=falo**
	brand = pyTools.togliAccenti( brand )
	brand = pyTools.rimpiazzaIlResto( brand )

	# replace degli spazi con "-" es: Criminal minds --> brand=criminal-minds
	brand = brand.replace(' ', '-')
	# replace dei caratteri speciali con "-". es Grey's anatomy --> brand = grey-s-anatomy
	brand = brand.replace('\'','-').replace('\"', '-')

	logger.debug ( brand )
	logger.debug ( brand )
	

	# CLAD _DEBUG
	#brand = 'via-col-venti'
	#channel = 'la1'
	# e quindi devo passarla come parametro alla 
	# http://internal.publishing.rsi.ch/webservice-extensions/srg/sectionIdForBrand/?publicationName=rsi&channel=la1&brand=via-col-venti
	
	auth = '%s:%s' % ('perucccl','perucccl')
	base64string = b64encode(auth.encode())
	base64string = base64string.decode("ascii")

	link = os.environ['ECE_BRAND'] 
	# in cui devo poi rimpiazzare __BRAND__ e __CHANNEL__
	link = link.replace('__CHANNEL__', channel.lower()).replace('__BRAND__',brand)
	logger.debug ( link )
	logger.debug ( link )
	
	headers = { 'Authorization' : 'Basic %s' %  base64string }

	try:
		request = urllib.request.Request(link, headers=headers)
		#resultResponse = urllib.request.urlopen(request)
		with urllib.request.urlopen(request) as resultResponse:
			tree = ET.parse(resultResponse)
		#logger.debug ( ET.tostring( tree.getroot() ))
		list = tree.getroot().findall( namespaces['atom'] + "id" )
		#logger.debug  (list[0].text)
		#logger.debug  (list[0].text.split('.rsi.ch:8080/webservice/escenic/section/')[-1])
		resultRequest = list[0].text.split('.rsi.ch:8080/webservice/escenic/section/')[-1]
		# questa ritorna 0 se non aveva una section corrispondente a quel nome
		if len(resultRequest) > 1:
			# mi ha restituito un id valido di sezione e lo metto 
			# e lo metto in result al posto dell id di altri programmi
			result = resultRequest
			logger.debug ( 'result di getIdServizioSezioni = ' + resultRequest )
			logger.debug ( 'result di getIdServizioSezioni = ' + resultRequest )
			
	except Exception as e:
		logger.debug ( 'PROBLEMI in getIdServizioSezioni : ' + str(e) )
		logger.warning ( 'PROBLEMI in getIdServizioSezioni : ' + str(e) )
		return result
		
	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	return result



def get_servizio_mam( mamUrn ) :

	logger.debug ( '------------------------ INIT get_servizio_mam -------------- ' )
	logger.debug ( '------------------------ INIT get_servizio_mam -------------- ' )
	
	#auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
	#base64string = b64encode(auth.encode())
	#base64string = base64string.decode("ascii")

	link = os.environ['CUE_MAM_SERVICE'] 
	if 'rundown' in mamUrn:
		link = link + 'rundown/'
	else:
		link = link + 'video/'

	logger.debug ( mamUrn.split(':')[-1] )
	link = link +  mamUrn.split(':')[-1]
	logger.debug( link )

	productId = None
	
	#headers = { 'Authorization' : 'Basic %s' %  base64string }

	try:
		#request = urllib.request.Request(link, headers=headers)
		request = urllib.request.Request(link)
		#resultResponse = urllib.request.urlopen(request)
		with urllib.request.urlopen(request) as resultResponse:
			responseJsonStr = resultResponse.read().decode('utf-8')
			responseJsonObj = json.loads( responseJsonStr ) 
			logger.debug(responseJsonObj)
			if 'sourceSystem' in responseJsonObj and (not (responseJsonObj['sourceSystem'] is None)) and 'louise' in responseJsonObj['sourceSystem']: 
				sourceSystem_louise = responseJsonObj['sourceSystem']['louise']
				logger.debug(sourceSystem_louise)
				if not( sourceSystem_louise is None ) and 'urn' in sourceSystem_louise:
					productId = sourceSystem_louise['urn']
					productId = productId.split(':')[-1]
					logger.debug('XXXXXXXXX : ' + productId)
			
	except Exception as e:
		logger.debug ( 'PROBLEMI in get_servizio_mam : ' + str(e) )
		logger.warning ( 'PROBLEMI in get_servizio_mam : ' + str(e) )
		return productId
					
		
	logger.debug ( '------------------------ END get_servizio_mam -------------- ' )
	logger.debug ( '------------------------ END get_servizio_mam -------------- ' )
	return productId



def getIdServizioSezioni( channel, sectionName, result ) :

	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	sectionId = '-1'
	# funzione per prendere il numero di sezione partendo dal nome 
	# trovato nel serie- titlepress
	# modificato come segue:
	# tutti i caratteri devono essere trasformati in minuscolo
	brand = sectionName.lower()
	# replace dei caratteri accentati con i caratteri semplici. es. Fal --> brand=falo**
	brand = pyTools.togliAccenti( brand )
	brand = pyTools.rimpiazzaIlResto( brand )

	brand = channel + '_programmi_' + brand
	logger.debug ( brand )
	logger.debug ( brand )
	

	# CLAD _DEBUG
	#brand = 'via-col-venti'
	#channel = 'la1'
	# e quindi devo passarla come parametro alla 
	# http://internal.publishing.rsi.ch/webservice-extensions/srg/sectionIdForBrand/?publicationName=rsi&channel=la1&brand=via-col-venti
	
	auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
	base64string = b64encode(auth.encode())
	base64string = base64string.decode("ascii")

	link = os.environ['CUE_BRAND'] 
	# in cui devo poi rimpiazzare __BRAND__ e __CHANNEL__
	link = link + brand
	logger.debug ( link )
	logger.debug ( link )
	
	headers = { 'Authorization' : 'Basic %s' %  base64string }

	try:
		request = urllib.request.Request(link, headers=headers)
		#resultResponse = urllib.request.urlopen(request)
		with urllib.request.urlopen(request) as resultResponse:
			responseJsonStr = resultResponse.read().decode('utf-8')
			responseJsonObj = json.loads( responseJsonStr ) 
			if 'data' in responseJsonObj and 'section' in responseJsonObj['data'] and 'displayId' in responseJsonObj['data']['section']:
				sectionId = responseJsonObj['data']['section']['displayId']
					
			
	except Exception as e:
		logger.debug ( 'PROBLEMI in getIdServizioSezioni : ' + str(e) )
		logger.warning ( 'PROBLEMI in getIdServizioSezioni : ' + str(e) )
		return result
		
	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	logger.debug ( '------------------------ END getIdServizioSezioni -------------- ' )
	return sectionId

def getContentSearchSitemap( contentType, zuluDateFrom, zuluDateTo ):

	logger.debug('-------------- INIT ---- getContentSearch ----------- ' )

	dateFrom = zuluDateFrom.replace(':','%3A')
	dateTo = zuluDateTo.replace(':','%3A')
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link_template = os.environ['CUE_COOK_SEARCH'] + "?q=*%3A*&type=" + contentType + "&creationdate=" + dateFrom + "%20TO%20" +  dateTo + "&sort=sitemap&start=__START__&rows=100&"

		link = link_template.replace('__START__', '0')
		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		logger.debug('Presi dal solrPrendiContent : ' + str(len(response['data']['results'])) + ' ' + "documents found")
		logger.debug('Presi dal solrPrendiContent : ' + str(len(response['data']['results'])) + ' ' + "documents found")

		#logger.debug(len(response['response']['docs']))

		listaContentId = response['data']['results']
		logger.debug(len(listaContentId))

		totresult = int(len(response['data']['results']))
		items_per_page = int(100)
	
		count = 0

		while totresult == items_per_page:
			__start__ = (count+1) * items_per_page
			logger.debug(str(count+1) + ' ' + str(__start__) )
			logger.debug(str(count+1) + ' ' + str(__start__) )

			#logger.debug(' giro per prenderli tutti')
			#e qui faccio la request sul campo next
			link_next = link_template.replace('__START__', str(__start__))
			#logger.debug(link_next)
			request = urllib.request.Request(url=link_next, headers=headers, method='GET')
			with urllib.request.urlopen(request) as resultResponse:
				logger.debug ( resultResponse.status )
				logger.debug ( resultResponse.status )
				response = json.loads(resultResponse.read().decode('utf-8'))

			listaContentId = listaContentId +  response['data']['results']
			totresult = int(len(response['data']['results']))
			count += 1


			#listaContentId.append( response['response']['docs'] )
			#logger.debug(len(listaContentId))

		logger.debug(len(listaContentId))
	
		
		for lis in listaContentId:
			id = lis['id']
			loc = lis['href']
			lastmod = lis['updated']
			result.append({'id' : id, 'loc' : loc, 'lastmod' : lastmod })

	except Exception as e:
		logger.warning ( 'PROBLEMI in solrPrendiContent : ' + str(e) )
		logger.debug( 'PROBLEMI in solrPrendiContent : ' + str(e)  )
		return []

	return result


def getContentSearchDetail( cueid ):

	logger.debug('-------------- INIT ---- getContentSearch ----------- ' )
	listaContentId = []
	result = []


	try:

		auth = '%s:%s' % (os.environ['CUE_USER'], os.environ['CUE_PWD'])
		base64string = b64encode(auth.encode())
		base64string = base64string.decode("ascii")

		# prende items con 
		# state:published 
		# contenttype:contentType
		link = os.environ['CUE_COOK_SEARCH'] + cueid 

		logger.debug( link )
		#logger.debug('link : ' + link )
		headers = { 'Authorization' : 'Basic %s' % base64string,
		'Content-Type': 'application/atom+xml'
		}

		request = urllib.request.Request(url=link, headers=headers, method='GET')
		with urllib.request.urlopen(request) as resultResponse:
			logger.debug ( resultResponse.status )
			logger.debug ( resultResponse.status )
			response = json.loads(resultResponse.read().decode('utf-8'))

		#logger.debug(response)
		#logger.debug(type(response))
		#logger.debug(len(response['response']['docs']))
		if 'data' in response and 'context' in response['data']:

			listaContentId = response['data']['context']
			assetId = listaContentId['id']
			loc = listaContentId['href']
			lastmod = listaContentId['updated']
			result = [ True, {'id' : assetId, 'loc' : loc, 'lastmod' : lastmod }]

		elif 'errors' in response:
			logger.debug('ERROR: probabilmente DELETED id :' + str(cueid))
			return [ False, 'probabilemnte DELETED']

	except Exception as e:
		logger.warning ( 'PROBLEMI in getContentSearch : ' + str(e) )
		logger.debug( 'PROBLEMI in getContentSearch : ' + str(e)  )
		return [ False, str(e)]

	return result

if __name__ == "__main__":


	# 'CUE_USER' : 'TSMM', 'CUE_PWD':'8AKjwWXiWAFTxb2UM3pZ'

	os.environ['CUE_USER'] = 'rsi_admin'
	os.environ['CUE_PWD'] = 'admin'

	cueServer = 'http://10.101.8.38:8080'
	cueServer = 'http://18.158.61.219:8080'
	cueServer = 'https://cue.cue-test.rsi.ch'
	cueAdmin = 'https://admin.cue-test.rsi.ch'
	cueCook = 'https://cook.cue-test.rsi.ch/'

	os.environ['CUE_COOK'] = cueCook
	os.environ['CUE_COOK_SEARCH'] = cueCook + 'rsi/search/'
	os.environ['CUE_MODEL'] = cueServer + '/webservice/publication/rsi/escenic/model/'
	os.environ['CUE_SECTION_MODEL'] = cueServer + '/webservice/escenic/publication/rsi/model/content-type/com.escenic.section'
	os.environ['CUE_SECTION'] = cueServer + '/webservice/escenic/section/'
	os.environ['CUE_CONTENT'] = cueServer + '/webservice/escenic/content/'
	os.environ['CUE_SERVER'] = cueServer
	os.environ['CUE_BINARY' ] =  cueServer + '/webservice/escenic/binary'
	os.environ['CUE_SECTION_PARAMETERS'] = cueAdmin + '/escenic-admin/section-parameters-declared/rsi'

	os.environ['IMG_CREATE_URL'] = cueServer + '/webservice/escenic/section/__CREATE_SECTION__/content-items'
	os.environ['RESOURCE_DIR'] = '/home/perucccl/PRODUCTION/article-structure-mananager/Resources/'

	getContentSearchSitemap( "audio", '2023-05-15T10:19:25Z', 'NOW' )

	os.environ['CUE_MAM_SERVICE'] = 'https://mam-blackhole.rsi.ch/mam-video-api/'
	
	exit(0)


	putSectionParameters('/', '/home/perucccl/PRODUCTION/article-structure-mananager/LOGS/FILES/sectionparams_06.09.2022_16.31.06.810824.xml' )
	exit(0)

	#subsectionXml = getSubSections( 'https://cue.cue-test.rsi.ch/webservice/escenic/section/1/subsections' )
	#logger.debug(type(subsectionXml))
	#exit(0)

	#listaDel = [ 3 ]
	listaDel = [ 27,3,9,11,24,25,26 ]
	listaDel = [2177]
	for lis in listaDel:
		deleteSection( str(lis) )

	# se stai cancellando le sezioni di CUE ricordati
	# di toglierle dal SQL 
	# MA di aggiungere 4-1 e 5-2
	exit(0)

	#createSectionFromFile("/home/perucccl//PRODUCTION/article-structure-mananager/LOGS/FILES/section_19.05.2022_23.28.59.629005.xml")	
	#exit(0)
	#logger.debug(createSectionFromFile( '/home/perucccl/PRODUCTION/article-structure-mananager/LOGS/FILES/section_20.05.2022_17.26.12.880872.xml'))
	logger.debug(putSectionId( '28', './section28.xml' ))
	exit(0)

	logger.debug(getSection( '28' ))
	exit(0)

	deleteSection( '39' )
	exit(0)

	putSection('4097', './4097.xml')
	exit(0)
	putSectionId('4097', './4097.xml')
	exit(0)
	logger.debug(result)
	exit(0)
	getId( '14915243' )

