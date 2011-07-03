# Imports
import os,sys,datetime,urllib,urllib2
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup

# Main class
class Main:

	# Init
	def __init__( self ) :

		# Constants
		self.__addon__ = xbmcaddon.Addon('plugin.video.gamesonnet')
		self.__setting__ = self.__addon__.getSetting
		self.__lang__ = self.__addon__.getLocalizedString
		self.__cwd__ = self.__addon__.getAddonInfo('path')
		self.DEBUG            = False
		self.IMAGES_PATH      = xbmc.translatePath( os.path.join( self.__cwd__, 'resources', 'images' ) )
		self.USER_DATE_FORMAT = xbmc.getRegion( "dateshort" ).replace( "MM", "%m" ).replace( "DD", "%d" ).replace( "YYYY", "%Y" ).strip()
		
		# Parse parameters...
		if sys.argv[ 2 ] != "" :
			params  = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
			if "page" in params:
				page_no = int( params[ "page" ] )
			else :
				page_no = 1
		url = urllib.unquote_plus( str( params[ "url" ] ))
		# Get the videos...
		self.getVideos( url, page_no )

	# Get plugins...
	def getVideos( self, cat_url, page_no ) :
		url = cat_url
		# Init
		# Get HTML page...
		
		usock = urllib2.urlopen( url )
		htmlSource = usock.read()
		usock.close()

		# Parse response...
		soupStrainer  = SoupStrainer( "div", { "class" : "file_table" } )
		beautifulSoup = BeautifulSoup( htmlSource, soupStrainer )
		print beautifulSoup
		second_div = beautifulSoup.div.nextSibling
		table_file_list = second_div.table
		table_rows = table_file_list.findAll( "tr" )
		for table_row in table_rows :
			table_row_columns = table_row.findAll( "td" )
			# print str(table_row_columns)
			if len(table_row_columns) == 3 :
				# 1st column - app page url + summary
				a = table_row_columns[0].a
				if a == None :
					continue

				app_page_url = a[ "href" ]
				app_summary  = a.string

				# Add to list...
				listitem        = xbmcgui.ListItem( app_summary, iconImage="DefaultVideo.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'logo.png' ) )
				listitem.setInfo( "video", { "Title" : app_summary, "Studio" : "Games On Net" } )
				app_url = '%s?action=app&url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( app_page_url ) )
				xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=app_url, listitem=listitem, isFolder=True)

		# Next page entry...
		# listitem = xbmcgui.ListItem (self.__lang__(30402), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		# xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list&page=%i" % ( sys.argv[0], page_no + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )