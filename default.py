# Imports
import sys

# Play
if ( "action=play" in sys.argv[ 2 ] ):
    import resources.lib.playmedia as plugin

# Main menu
else :
    import resources.lib.list_latestmedia as plugin

plugin.Main()