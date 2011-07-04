# Imports
import sys

# Play
if ( "action=play" in sys.argv[ 2 ] ):
    import resources.lib.play_media as plugin

# Company
elif ( "action=company" in sys.argv[ 2 ] ):
    import resources.lib.list_company as plugin

# Company
elif ( "action=app" in sys.argv[ 2 ] ):
    import resources.lib.list_app as plugin

# Latest Media
elif ( "action=latestmedia" in sys.argv[ 2 ] ):
    import resources.lib.list_latestmedia as plugin

# Main menu
else :
    import resources.lib.list_main as plugin

plugin.Main()