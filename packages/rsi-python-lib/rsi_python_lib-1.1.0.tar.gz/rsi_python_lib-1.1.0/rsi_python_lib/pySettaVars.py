import os
from pathlib import Path
home = str(Path.home()) + '/'

import rsi_python_lib.pyConfig


PROD_CONFIG_FILE_SECTIONS = home+'/PRODUCTION/article-structure-mananager/LOGS/conf.sections-structure-mananager_logging_PROD.conf'
TEST_CONFIG_FILE_SECTIONS = home+'/STAGING/article-structure-mananager/LOGS/conf.sections-structure-mananager_logging_TEST.conf'


KAFKA_SERVERS =[]

listaContentTypesAll = ["story","banner", "gallery", "htmlContent", "keyframe", "link", "livestreaming", "mamTranscodableAudio", "media", "migrationAudio", "migrationVideo", "picture", "programme", "programmeAudio", "programmeVideo", "promo", "recipe", "segmentedProgrammeVideo", "series", "shortStory", "transcodableAudio", "transcodableVideo", "vmeVideo", "youtubeVideo", "votazione", "linklist", "event", "mamProgramme", "mamProgrammeVideo", "mamTranscodableVideo", "mamProgrammeAudio", "segmentAudio", "mamTranscodableAudio", "mamSegmentedProgrammeVideo", "liveCenterEvent", "profile", "rioVideo", "vmeAudio", "migrationAudio"]
listaContentTypesNoKeyframes = ["story","banner", "gallery", "htmlContent", "link", "livestreaming", "mamTranscodableAudio", "media", "migrationAudio", "migrationVideo", "picture", "programme", "programmeAudio", "programmeVideo", "promo", "recipe", "segmentedProgrammeVideo", "series", "shortStory", "transcodableAudio", "transcodableVideo", "vmeVideo", "youtubeVideo", "votazione", "linklist", "event", "mamProgramme", "mamProgrammeVideo", "mamTranscodableVideo", "mamProgrammeAudio", "segmentAudio", "mamTranscodableAudio", "mamSegmentedProgrammeVideo", "liveCenterEvent", "profile", "rioVideo", "vmeAudio", "migrationAudio"]

listaContentTypesVideo = ["migrationVideo", "programmeVideo", "transcodableVideo", "vmeVideo",
			  "mamTranscodableVideo", "mamProgrammeVideo", "mamSegmentedProgrammeVideo", "segmentedProgrammeVideo" ]

dictModelCodes = {
      "com.escenic.section": 0,
      "banner": 10,
      "event": 15,
      "forum": 20,
      "gallery": 30,
      "htmlContent": 40,
      "keyframe": 50,
      "link": 60,
      "linklist": 70,
      "liveCenterEvent": 75,
      "livestreaming": 80,
      "mamProgramme": 83,
      "mamProgrammeAudio": 85,
      "mamProgrammeVideo": 86,
      "mamSegmentedProgrammeVideo": 87,
      "mamTranscodableAudio": 90,
      "mamTranscodableVideo": 95,
      "media": 100,
      "migrationAudio": 110,
      "migrationVideo": 120,
      "picture": 130,
      "profile": 135,
      "programme": 140,
      "programmeAudio": 150,
      "programmeVideo": 160,
      "promo": 170,
      "recipe": 180,
      "rioVideo": 185,
      "segmentAudio": 186,
      "segmentedProgrammeVideo": 190,
      "series": 200,
      "shortStory": 210,
      "story": 220,
      "transcodableAudio": 230,
      "transcodableVideo": 240,
      "vmeAudio": 250,
      "vmeVideo": 260,
      "votazione": 265,
      "youtubeVideo": 270
}

sectionsBlackList = {
	"26910":"teche",
	"16693":"autenticazione",
	"23595":"la-tua-opinione",
	"20203":"newHome",
	"7943":"search",
	"26601":"servizio",
	"5869":"podcast-old",
	"5909":"temp",
	"5914":"profile",
	"27304":"test-dev	",
	"4089":"config",
	"5927":"config.newsletter.section"
}

sectionMapping = {}

sectionMapping_PROD = { '5':'2',
		'15100' : '1106',
		'22357' :'697',
		'30019' :'2350',
		'14779' :'446',
		'4127' :'447',
		'15097' :'600',
		'14782' :'1093',
		'23075' :'440',
		'23093' :'201',
		'28635' :'223',
		'4553' :'1094',
		'10630' :'-1'
}

sectionMapping_STAG = { '5':'2',  
		'15100' : '6291',
		'22357' : '5882', 
		'30019' : '7520', 
		'14779' : '5634', 
		'4127' : '5635', 
		'15097' : '5785', 
		'14782' : '6278', 
		'23075' : '5628', 
		'23093' : '5396', 
		'28635' : '5418', 
		'4553' : '6279',
		'10630' : '-1' 
}

listaCartoniUniqueNames = [ "a-casa-dei-loud",
	"alvinnn-",
	"animalis",
	"arthur-e-il-popolo-dei-minimei",
	"belle-e-sebastian",
	"bing",
	"blaze-e-le-mega-macchine",
	"bob-aggiustatutto-serie-2-",
	"bob-aggiustatutto",
	"c-era-una-volta-la-vita",
	"disney-miles-dal-futuro",
	"i-piccoli-racconti-di-wismo",
	"i-pirati-della-porta-accanto",
	"la-famiglia-volpitassi",
	"lejo",
	"mamma-jamie-ha-i-tentacoli",
	"masha-tales-i-racconti-di-masha",
	"max-maestro",
	"mig-said",
	"molly-il-mostro",
	"monchhichi",
	"munki-e-trunk",
	"nella-principessa-coraggiosa",
	"ollie",
	"peanuts",
	"polly-pocket",
	"rocket-jo",
	"simone",
	"spirit",
	"super-wings",
	"telmo-e-tula",
	"the-deep",
	"trulli-tales-le-avventure-dei-trullalleri",
	"tvbio",
	"vita-da-giungla-alla-riscossa-2-serie-",
	"wissper",
	"zipzip",
	"zou",
	"rev-roll",
	# la2 (senza doppioni)
	"l-ape-maia",
	"c-era-una-volta--cappuccetto-a-pois",
	"c-era-una-volta-il-gatto-arturo",
	"c-era-una-volta-la-bottega-del-signor-pietro",
	"c-era-una-volta-la-vita",
	"e-sempre-lunedi",
	"garfield",
	"gli-abissi",
	"hank-zipzer-fuori-dalle-righe-",
	"i-rimedi-di-eva",
	"il-libro-della-giungla-1-serie-2-parte-",
	"il-nonno-nel-taschino-anno-4-",
	"il-nonno-nel-taschino",
	"insieme-a-rosie",
	"le-avventure-del-gatto-con-gli-stivali",
	"leonardo",
	"mademoiselle-zazie",
	"miraculous",
	"miss-moon",
	"morph",
	"nicky-ricky-dicky-and-dawn",
	"ollie-e-moon",
	"olly-il-sottomarino-1-serie-",
	"paw-patrol",
	"ralph-e-i-dinosauri",
	"robin-hood",
	"s-rini-culture-del-mondo",
	"s-rini-ector-rocco",
	"s-rini-ector-e-olga",
	"shaun-vita-da-pecora",
	"sherlock-yack-zoo-detective",
	"te-lo-dimostro-io-",
	"toot-e-puddle",
	"topo-tip",
	"vicky-il-vichingo",
	"zip-zip"]

tagDictDocu = {'STORIE VERE' : '2017:documentaristorievere',
		'PERSONAGGI' : '2017:documentaristorievere',
		'DOCUMENTARI' : '2017:documentari',
                        'VIAGGI' : '2017:documentariviaggi',
                        'STORIA' : '2017:documentaristoria',
                        'ARTE' : '2017:documentariarte',
                        'SCIENZA E TECNOLOGIA' : '2017:documentariscienzaetecnologia',
                        'SCIENZA&amp;TECNOLOGIA' : '2017:documentariscienzaetecnologia',
                        'NATURA' : '2017:documentarinatura',
                        'SOCIETA' : '2017:documentarisocieta',
                        'SOCIETÀ' : '2017:documentarisocieta'
}

tagDictTelefilms = {'ALTA TENSIONE' : '2017:seriealtatensione',
                        'GIALLO&amp;CRIME' : '2017:seriegialloecrime',
                        'SERIE - GIALLO&amp;CRIME' : '2017:seriegialloecrime',
                        'TARGATO CH' : '2017:serietargatoch',
                        'DRAMA&amp;AVVENTURA' : '2017:seriedrammaeavventura'
}

tagDictFilms = {'ALTA TENSIONE' : '2017:filmaltatensione',
                'COMMEDIA' : '2017:filmcommedia',
                'AVVENTURA' : '2017:filmavventura',
                'NATURA' : '2017:filmnatura',
                'SENTIMENTALE': '2017:filmsentimentali',
                'GIALLO&amp;CRIME':'2017:filmgialloecrime',
                'SERIE - GIALLO&amp;CRIME':'2017:filmgialloecrime',
                'DRAMMATICO':'2017:filmdrammatico',
                'SCIENZA E TECNOLOGIA' : '2017:filmscienzaetecnologia',
                'JUNIOR':'2017:filmjunior',
                'VINTAGE':'2017:filmvintage',
                'STORIE VERE':'2017:filmstorievere',
                'SOCIETA' : '2017:filmsocieta',
                'SOCIETÀ' : '2017:filmsocieta',
                'VIAGGI':'2017:filmviaggi',
                'TARGATO CH': '2017:filmtargatoch',
                'KIDS': '2017:bambini',
                'PICCOLI': '2017:kidspiccoli',
                'GRANDI': '2017:kidsgrandi'
}

tagDictKids = { 'KIDS': '2017:bambini',
                'PICCOLI': '2017:kidspiccoli',
                'GRANDI': '2017:kidsgrandi'
}



sectionDictVOD = {
       'Allmen':'28686',
        'Art of crime':'28689',
        'Cuore d\'africa':'28650',
        'Dottoressa dell\'isola':'28647',
        'Dupin':'28671',
        'Garage sale mistary':'28674',
        'I misteri di brokenwood':'28680',
        'I misteri di Emma Fielding':'28683',
        'Il mistero delle lettere perdute':'28644',
        'In the vineyard':'28677',
        'Sea Patrol':'28659',
        'Soko - Misteri tra le montagne':'28692',
        'Una nuova vita per Zoe':'28656',
        'Van Der Valk':'28668'
}


fieldsRelationPerGiu = {
	"escenicId":"__ESCENICID__",
	"SectionId":"__SECTIONID__",
	"subTitle":"editorialContent_shortDescriptionPress",
	"title":"editorialContent_show_title",
	"startTime":"dateTimes_startBroadcastPress",
	"state":"published",
	"text":"editorialContent_longDescriptionPress",
	"productId":"sourceSystem_louise_urn",
	"geoBlock":"rights_geoblocked",
	"network":"channel",
	"series":"editorialContent_show_title"
}


caratteriSpeciali =  {'&':'&#38;','<':'&lt;','>':'&gt;'}

if __name__ == "__main__":

        logger = logging.getLogger()
        logger.debug('PRIMA DI SETTARE ENVIRONMENT')
        logger.debug('ENV : ')
        logger.debug(os.environ)

        #for param in os.environ.keys():
            #logger.debug("%20s %s" % (param,os.environ[param]))
            #dict_env[ param ] = os.environ[param]

        logger.debug('---------------------------------')

        logger.debug('verifico se la variabile _APICoreXEnv_ e settata')
        if '_APICoreXEnv_' in os.environ:
                if 'PRODUCTION' in os.environ['_APICoreXEnv_']:
                        logger.debug('setto ENV di PROD')
                else:
                        logger.debug('Variabile _APICoreXEnv_ su valore diverso da \'PRODUCTION\'')
                        logger.debug('setto ENV di TEST')

        else:
                logger.debug('setto ENV di TEST')


        exit(0)
        for param in Environment_Variables.keys():
            #logger.debug("%20s %s" % (param,dict_env[param]))
            os.environ[param] = Environment_Variables[ param ]


        logger.debug('DOPO AVER SETTATO ENVIRONMENT')
        logger.debug('ENV : ')
        logger.debug(os.environ)



