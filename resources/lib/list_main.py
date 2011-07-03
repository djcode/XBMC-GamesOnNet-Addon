import sys,urllib,xbmcgui,xbmcplugin,xbmcaddon
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

		listitem	=	xbmcgui.ListItem( "Latest Media", iconImage="DefaultVideo.png")
		item_url	=	'%s?action=latestmedia' % ( sys.argv[ 0 ] )
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=item_url, listitem=listitem, isFolder=True)
		
		listitem	=	xbmcgui.ListItem( "Revision3 Shows", iconImage="DefaultVideo.png")
		item_url	=	'%s?action=company&url=%s' % ( sys.argv[ 0 ], urllib.quote_plus( "http://games.on.net/filelist.php?company=1328" ) )
		xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=item_url, listitem=listitem, isFolder=True)
		
		# Disable sorting...
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

		# End of directory...
		xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
		