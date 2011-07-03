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
		url = "http://www.games.on.net"+urllib.unquote_plus( str( params[ "url" ] ))
		# Get the videos...
		self.getVideos( url, page_no )

	# Get plugins...
	def getVideos( self, url, page_no ) :
		# Init
		# Get HTML page...
		
		usock = urllib2.urlopen( url )
		htmlSource = usock.read()
		usock.close()

		# Parse response...
		soupStrainer  = SoupStrainer( "table", { "class" : "files" } )
		beautifulSoup = BeautifulSoup( htmlSource, soupStrainer )
		for table in beautifulSoup :
			table_row_columns = table.tr.findAll( "td" )
			# print str(table_row_columns)
			if len(table_row_columns) == 1 :
				# 1st column - app page url + summary
				a = table_row_columns[0].a
				if a == None :
					continue

				vid_page_url = a[ "href" ]
				vid_summary  = a.string

				# Add to list...
				listitem        = xbmcgui.ListItem( vid_summary, iconImage="DefaultVideo.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'logo.png' ) )
				listitem.setInfo( "video", { "Title" : vid_summary, "Studio" : "Games On Net" } )
				vid_url = '%s?action=play&video_page_url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( vid_page_url ) )
				xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=vid_url, listitem=listitem, isFolder=True)

		# Next page entry...
		# listitem = xbmcgui.ListItem (self.__lang__(30402), iconImage = "DefaultFolder.png", thumbnailImage = os.path.join(self.IMAGES_PATH, 'next-page.png'))
		# xbmcplugin.addDirectoryItem( handle = int(sys.argv[1]), url = "%s?action=list&page=%i" % ( sys.argv[0], page_no + 1 ), listitem = listitem, isFolder = True)

		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )