# 
# Constants
#
__plugin__  = "Games On Net"
__author__  = "Dan Dar3 & Daniel Jolly"
__url__     = "http://dandar3.blogspot.com & http://www.danieljolly.com"
__date__    = "19 February 2011"
__version__ = "1.1"

#
# Imports
#

import sys

#
# Play
#
if ( "action=play" in sys.argv[ 2 ] ):
    import resources.lib.gamesonnet_play as plugin
#
# Main menu
#
else :
    import resources.lib.gamesonnet_list as plugin

plugin.Main()
