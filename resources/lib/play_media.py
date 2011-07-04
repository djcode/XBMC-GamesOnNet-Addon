# Imports
import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import re
import urllib,urllib2
from BeautifulSoup import SoupStrainer
from BeautifulSoup import BeautifulSoup

# Main class
class Main:
	
	# Init
	def __init__( self ) :

		# Constants
		self.DEBUG = False
		
		self.__addon__ = xbmcaddon.Addon('plugin.video.gamesonnet')
		self.__setting__ = self.__addon__.getSetting
		self.__lang__ = self.__addon__.getLocalizedString
		self.__cwd__ = self.__addon__.getAddonInfo('path')

		# Parse parameters...
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
		self.video_page_url = urllib.unquote_plus( params[ "video_page_url" ] )

		# Settings
		self.video_players = { "0" : xbmc.PLAYER_CORE_AUTO,
							"1" : xbmc.PLAYER_CORE_DVDPLAYER,
							"2" : xbmc.PLAYER_CORE_MPLAYER }
		self.video_player = self.__setting__("video_player")

		# Play video...
		self.playVideo()

	# Play video...
	def playVideo( self ) :
		if (self.DEBUG) :
			print "video_page_url = " + self.video_page_url

		# Get current list item details...
		title     = unicode( xbmc.getInfoLabel( "ListItem.Title"  ), "utf-8" )
		thumbnail =          xbmc.getInfoImage( "ListItem.Thumb"  )
		studio    = unicode( xbmc.getInfoLabel( "ListItem.Studio" ), "utf-8" )
		plot      = unicode( xbmc.getInfoLabel( "ListItem.Plot"   ), "utf-8" )
		genre     = unicode( xbmc.getInfoLabel( "ListItem.Genre"  ), "utf-8" )

		# Show wait dialog while parsing data...
		dialogWait = xbmcgui.DialogProgress()
		dialogWait.create( self.__lang__(30403), title )

		# Get video page...
		url = "http://games.on.net%s" % self.video_page_url
		usock = urllib2.urlopen( url )
		htmlSource = usock.read()
		usock.close()

		soupStrainer2  = SoupStrainer( "div", { "class" : "file_table" } )
		beautifulSoup2 = BeautifulSoup( htmlSource, soupStrainer2 )

		# Thumbnail...
		table_file            = beautifulSoup2.table
		table_1st_row         = table_file.tr
		table_1st_row_3rd_col = table_1st_row.findAll( "td" )[2]
		thumbnail             = table_1st_row_3rd_col.img[ "src" ]
		
		# Work out whether "view" is possible
		hyperlinks			= table_file.findAll("a", attrs={"href": re.compile("^javascript")})
	#	print str(hyperlinks)
		if "javascript:vidplayer" in str(hyperlinks):
			use_view_method = 1
		else:
			use_view_method = 0
		print use_view_method
		# Video ID
		url_dict = self.video_page_url.split( "/" )
		video_id = url_dict[ 2 ]
		
		dialogWait.update(50)
		
		# Video URL...
		if use_view_method == 1:
			if self.__setting__('quality')=='0':
				quality = 'high'
			else:
				quality = 'low'
			url = "http://games.on.net/filepopup.php?video=%(id)s&quality=%(q)s" % {'id':video_id, 'q': quality}
			regex = "\'(.+?\.(flv|mp4|mov|avi|3gp))\'"
		else:
			url = "http://games.on.net/filepopup.php?file=%(id)s" % {'id':video_id}
			regex = 'URL=(.+?\.(flv|mp4|mov|avi|3gp))\"'
		usock = urllib2.urlopen( url )
		htmlSource = usock.read()
		usock.close()
		video_url = re.compile( regex ).search( htmlSource ).group( 1 )
		print video_url
		video_dom = "http://gon.cdn.on.net"
		if video_url.startswith('http://'):
			video_url = video_url
		else :
			video_url = video_dom+video_url

		# Close wait dialog...
		dialogWait.close()
		del dialogWait

		# Play video...
		playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		playlist.clear()
		listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
		listitem.setInfo( "video", { "Title": title, "Studio" : studio, "Plot" : plot, "Genre" : genre } )
		playlist.add( video_url, listitem )

		# Play video...
		xbmcPlayer = xbmc.Player(self.video_players[ self.video_player ]) 
		xbmcPlayer.play( playlist )