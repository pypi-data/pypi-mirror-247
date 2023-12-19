
from pathlib import Path
home = str(Path.home()) + '/'

class config():

	def __init(self):

		cueServer = 'http://10.101.8.38:8080'
		cueServer = 'https://cue.cue-test.rsi.ch:8080'
		cueServer = 'http://18.158.61.219:8080'
		# ocio a http o https che ti manda il 301

		cueServer = 'https://cue.cue-test.rsi.ch'
		# per l'admin
		cueAdmin = 'https://admin.cue-test.rsi.ch'

		ecePresentation = 'http://presentation5.rsi.ch'
		#ecePublishing = 'http://internal.publishing.production.rsi.ch'
		# DEBUG PER ANDARE SOLO SUL pub3
		ecePublishing = 'http://internal.publishing3.production.rsi.ch'

		cueServerProd = 'https://cue.cue.rsi.ch'
		# per l'admin
		cueAdminProd = 'https://admin.cue.rsi.ch'

		PROD_KAFKA_SERVERS =['rsis-zp-kafka1:9092','rsis-zp-kafka2:9092','rsis-zp-kafka3:9092']
		PROD_Environment_Variables = {
			'AWS_DEFAULT_REGION':'eu-central-1',
			'AWS_S3_BUCKET':'rsistatic-prd',
			'AWS_S3_ACCESSKEY' : 'AKIAWKQD34FYKYBLIV7D', 
			#'AWS_S3_ACCESSKEY' : 'AKIAWKQD34FYA62YL26Q', 
			'AWS_S3_SECRETKEY':'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',
			#'AWS_S3_SECRETKEY':'TWx1RBVWmFRVIKrWUB5BdDxoU/OTouAJc52vlNO7',
			'CUE_SOLR':'https://solr.cue.rsi.ch/solr/editorial',
			'CUE_SOLR_USR':'rsisolr',
			'CUE_SOLR_PWD':'6igq-YOYOE1C27ftpnTPHrfJgh8FewND',
			'CUE_MAM_SERVICE':'https://mam-blackhole.rsi.ch/mam-video-api/',
			'SITEMAP_PATH':'https://www.rsi.ch/generic-static/',
			'RESOURCE_DIR':'/opt/import-keyframe/Resources/',
			'LOCK_RESOURCE_DIR':'/opt/import-keyframe/Resources/',
			'IMPORT_SECTION':'471',
			'DB_NAME' : '/opt/import-keyframe/Resources/_ImportKeyFramesDb_',
			'CUE_SECTION_PARAMETERS':cueAdminProd + '/escenic-admin/section-parameters-declared/rsi',
			'CUE_USER':'rsi_admin',
			'CUE_PWD':'pM4U4$k3eouwY1sWy61Q',
			'CUE_SECTION_FILES':'/opt/import-keyframe/LOGS/FILES/',
			'CUE_CREATE_FILES':'/opt/import-keyframe/LOGS/FILES/',
			'CUE_SECTION_MODEL':cueServerProd + '/webservice/escenic/publication/rsi/model/content-type/com.escenic.section',
			'CUE_MODEL':cueServerProd + '/webservice/publication/rsi/escenic/model/',
			'CUE_TAG_URL':cueServerProd + '/webservice/escenic/classification/tag/',
			#'CUE_BRAND':'https://cook.cue-test.rsi.ch/rsi/search/section/?uniqueName=',
			'CUE_CONTENTTYPE':cueServerProd + '/webservice/escenic/publication/rsi/model/content-type/',
			'CUE_CONTENTSUMMARY':cueServerProd + '/webservice/escenic/publication/rsi/model/content-summary/',
			'CUE_SECTION':cueServerProd + '/webservice/escenic/section/',
			'CUE_SERVER':cueServerProd,
			'CUE_CONTENT':cueServerProd + '/webservice/escenic/content/',
			'CUE_BINARY' : cueServerProd + '/webservice/escenic/binary',
			'CUE_CREATE_URL':cueServerProd + '/webservice/escenic/section/__CREATE_SECTION__/content-items',
			'CUE_THUMB':cueServerProd + '/webservice/thumbnail/article/',
			'CUE_STORYLINE':cueServerProd + '/webservice/escenic/shared/model/storyline-template/' ,
			'CUE_STORYELEMENTS':cueServerProd + '/webservice/escenic/shared/model/story-element-type/' ,
			'SQL_DB':'struttura_int',
			'IMG_RESOURCE_TEMPLATE':'/opt/import-keyframe/Resources/template_picture.xml.prod',
			'LOCK_ID' : '11868353' ,
			'REST_POST_URL': 'http://publishing.rsi.ch/rsi-api/intlay/mockup/importkeyframe/keyframes.json',
			'REST_GET_URL': 'https://www.rsi.ch/rsi-api/intlay/mockup/importkeyframe/keyframes.json',
			'FTP_ARCHIVE_DIR' : '/mnt/rsi_import/keyframe_traffic/archived/',
			'FTP_DIR' : '/mnt/rsi_import/keyframe_traffic/prod/',
			'VERSION' : '3.2',
			'ECE_USER' : 'TSMM',
			'ECE_PWD':'8AKjwWXiWAFTxb2UM3pZ',
			'ECE_METADATA': ecePresentation + '/rsi-api/intlay/srgplay/migration/transcoder/metadata/',
			'ECE_PACKAGING': 'https://packaging.rsi.ch/media-delivery/audio/ww/',
			'MEDIA_PATH' : '/mnt/rsi_transcoded/vmeo/httpd/html/',
			#'ECE_PLAY': ecePresentation + '/rsi-api/intlay/srgplay/play/',
			'ECE_PLAY': 'http://pindex.rsi.ch/api/',
			'ECE_ENTRIES': ecePresentation + '/live-center-presentation-webservice/event/__ECE_ID__/entries?count=10',
			'ECE_SECTION' : ecePublishing + '/webservice/escenic/section/',
			'ECE_MODEL':ecePublishing + '/webservice/publication/rsi/escenic/model/',
			'ECE_SERVER' : ecePublishing + '/webservice/escenic/content/',
			'ECE_BINARY' : ecePublishing + '/webservice/escenic/binary',
			'ECE_SECTION' : ecePublishing + '/webservice/escenic/section/',
			'SOLR_SERVER' : ecePublishing + ':8180/solr/collection1',
			'CREATE_URL':ecePublishing + '/webservice/escenic/section/__CREATE_SECTION__/content-items',
			'IMG_CREATE_URL':ecePublishing + '/webservice/escenic/section/__CREATE_SECTION__/content-items',
			'LOCK_URL' : ecePublishing + '/webservice/escenic/lock/article/',
			'http_proxy': 'http://gateway.zscloud.net:10268',
			'LOGS_CONFIG_FILE':'/opt/import-keyframe/LOGS/conf.sitemap-gen_logging_PROD.conf',
			'LOGS_FILES':'/opt/import-keyframe/LOGS/',
			'PATH': '/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin',
			'LANG': 'en_US.UTF-8',
			'https_proxy': 'http://gateway.zscloud.net:10268',
			'no_proxy': 'amazonaws.com, rsis-zp-mongo1, localhost, 127.0.0.1, .media.int, rsis-tifone-t1, rsis-tifone-t2, rsis-tifone-t, rsis-tifone-01, rsis-tifone-02, .rsi.ch, 10.102.7.38:8180, 10.101.8.27:8180, .twitter.com'
		}


		# PYTHONPATH=:/home/perucccl/PRODUCTION/import-keyframe/CUE:/home/perucccl/PRODUCTION/import-keyframe/MODULES:/home/perucccl/PRODUCTION/import-keyframe/Resources:/home/perucccl/PRODUCTION/import-keyframe/KAFKA:/home/perucccl/PRODUCTION/import-keyframe/ECE:/home/perucccl/PRODUCTION/import-keyframe/SOLR:/home/perucccl/PRODUCTION/import-keyframe/XML:/home/perucccl/PRODUCTION/import-keyframe/SQL


		cueServer = 'https://cue.cue-int.rsi.ch'
		cueServer = 'http://cue-private-nlb-9efdfb5fe32811df.elb.eu-central-1.amazonaws.com:9080'
		# per l'admin
		cueAdmin = 'https://admin.cue-int.rsi.ch'
		#ecePresentation = 'http://internal.presentation.staging.rsi.ch'
		#ecePublishing = 'http://internal.publishing.staging.rsi.ch'
		ecePresentation = 'http://presentation5.rsi.ch'
		#ecePublishing = 'http://internal.publishing.production.rsi.ch'
		ecePublishing = 'http://internal.publishing3.production.rsi.ch'
		cueSolr = 'http://cue-private-nlb-9efdfb5fe32811df.elb.eu-central-1.amazonaws.com:9983'

		STAG_Environment_Variables = {
			'AWS_DEFAULT_REGION':'eu-central-1',
			'AWS_S3_BUCKET':'rsistatic-int',
			'AWS_S3_ACCESSKEY' : 'AKIA4HLRXFHO7CIK7G73', 
			'AWS_S3_SECRETKEY':'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',
			'SITEMAP_PATH':'www.rsi.ch/generic-stat<ic/',
			'RESOURCE_DIR':home+'/PRODUCTION/import-keyframe/Resources/',
			'LOCK_RESOURCE_DIR':home+'/PRODUCTION/import-keyframe/Resources/',
			'DB_NAME' : home+'/PRODUCTION/import-keyframe/Resources/_ImportKeyFramesDb_',
			'CUE_SECTION_PARAMETERS':cueAdminProd + '/escenic-admin/section-parameters-declared/rsi',
			'CUE_USER':'rsi_admin',
			'CUE_PWD':'admin',
			'CUE_SECTION_FILES':home+'PRODUCTION/import-keyframe/LOGS/FILES/',
			'CUE_CREATE_FILES':home+'PRODUCTION/import-keyframe/LOGS/FILES/',
			'CUE_SECTION_MODEL':cueServerProd + '/webservice/escenic/publication/rsi/model/content-type/com.escenic.section',
			'CUE_SOLR': cueSolr + '/solr/editorial',
			'CUE_SOLR_USR':'',
			'CUE_SOLR_PWD':'',
			#'CUE_BRAND':'https://cook.cueint.rsi.ch/rsi/search/section/?uniqueName=',
			'CUE_TAG_URL':cueServerProd + '/webservice/escenic/classification/tag/',
			'CUE_MODEL':cueServerProd + '/webservice/publication/rsi/escenic/model/',
			'CUE_MAM_SERVICE':'https://mam-bh-stage.rsi.ch/mam-video-api/',
			'CUE_CONTENTTYPE':cueServerProd + '/webservice/escenic/publication/rsi/model/content-type/',
			'CUE_CONTENTSUMMARY':cueServerProd + '/webservice/escenic/publication/rsi/model/content-summary/',
			'CUE_SECTION':cueServerProd + '/webservice/escenic/section/',
			'CUE_SERVER':cueServerProd,
			'CUE_CONTENT':cueServerProd + '/webservice/escenic/content/',
			'CUE_BINARY' : cueServerProd + '/webservice/escenic/binary',
			'CUE_CREATE_URL':cueServerProd + '/webservice/escenic/section/__CREATE_SECTION__/content-items',
			'CUE_THUMB':cueServerProd + '/webservice/thumbnail/article/',
			'CUE_STORYLINE':cueServerProd + '/webservice/escenic/shared/model/storyline-template/' ,
			'CUE_STORYELEMENTS':cueServerProd + '/webservice/escenic/shared/model/story-element-type/' ,
			'SQL_DB':'struttura_int',
			'IMG_RESOURCE_TEMPLATE':home+'/PRODUCTION/import-keyframe/Resources/template_picture.xml.prod',
			'LOCK_ID' : '11868353' ,
			'REST_POST_URL': 'http://publishing.rsi.ch/rsi-api/intlay/mockup/importkeyframe/keyframes.json',
			'REST_GET_URL': 'https://www.rsi.ch/rsi-api/intlay/mockup/importkeyframe/keyframes.json',
			'FTP_ARCHIVE_DIR' : '/home/perucccl/Ftp_Dir/archived/',
			'FTP_DIR' : '/home/perucccl/Ftp_Dir/',
			'VERSION' : '3.2',
			'ECE_USER' : 'TSMM',
			'ECE_PWD':'8AKjwWXiWAFTxb2UM3pZ',
			'IMPORT_SECTION':'445',
			'ECE_METADATA': ecePresentation + '/rsi-api/intlay/srgplay/migration/transcoder/metadata/',
			'ECE_PACKAGING': 'https://packaging.rsi.ch/media-delivery/audio/ww/',
			'MEDIA_PATH' : '/mnt/rsi_transcoded/vmeo/httpd/html/',
			#'ECE_PLAY': ecePresentation + '/rsi-api/intlay/srgplay/play/',
			'ECE_PLAY': 'http://pindex.rsi.ch/api/',
			'ECE_ENTRIES': ecePresentation + '/live-center-presentation-webservice/event/__ECE_ID__/entries?count=10',
			'ECE_SECTION' : ecePublishing + '/webservice/escenic/section/',
			'ECE_MODEL':ecePublishing + '/webservice/publication/rsi/escenic/model/',
			'ECE_SERVER' : ecePublishing + '/webservice/escenic/content/',
			'ECE_BINARY' : ecePublishing + '/webservice/escenic/binary',
			'ECE_SECTION' : ecePublishing + '/webservice/escenic/section/',
			'SOLR_SERVER' : ecePublishing + ':8180/solr/collection1',
			'CREATE_URL':ecePublishing + '/webservice/escenic/section/__CREATE_SECTION__/content-items',
			'IMG_CREATE_URL':ecePublishing + '/webservice/escenic/section/__CREATE_SECTION__/content-items',
			'LOCK_URL' : ecePublishing + '/webservice/escenic/lock/article/',
			'http_proxy': 'http://gateway.zscloud.net:10268',
			'HOME': home+'',
			'LOGS_CONFIG_FILE':home+'/PRODUCTION/import-keyframe/LOGS/conf.sitemap-gen_logging_PROD.conf',
			'LOGS_FILES':home+'/PRODUCTION/import-keyframe/LOGS/',
			'PATH': '/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:~/bin',
			'LANG': 'en_US.UTF-8',
			'https_proxy': 'http://gateway.zscloud.net:10268',
			'no_proxy': 'amazonaws.com, rsis-zp-mongo1, localhost, 127.0.0.1, .media.int, rsis-tifone-t1, rsis-tifone-t2, rsis-tifone-t, rsis-tifone-01, rsis-tifone-02, .rsi.ch, 10.102.7.38:8180, 10.101.8.27:8180, .twitter.com'
		}
