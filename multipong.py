from common import *
import event
import display
import player
import game

def parse():
    parser = argparse.ArgumentParser(description='A multiplayer pong clone')
    parser.add_argument('-H', '--hostname', help='The hostname of a server to connect to', required=False)
    parser.add_argument('-s', '--server', help='Start the game in server mode for clients to connect', required=False)
    parser.add_argument('-S', '--speed', help='The starting speed of the ping pong ball', required=False)
    parser.add_argument('-d', '--display', help='The display type to use (curses)', required=False, default='curses')
    parser.add_argument('-l', '--loglevel', help='The loglevel (DEBUG|INFO|WARNING|ERROR|CRITICAL)', required=False, default='INFO')
    return parser.parse_args()

def main():
    args = parse()
    flags = {'type': 'local', 'hostname': '', 'display': args.display}
    if args.server:
        flags['type'] = 'server'
    else:
        flags['type'] = 'local'
    if args.hostname:
        flags['type'] = 'remote'
        flags['hostname'] = str(args.hostname)
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename="logfile.txt",
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        level=getattr(logging, args.loglevel))
    logger = logging.getLogger()
    logger.info("Starting:")
    for line in json.dumps(flags, indent=4, sort_keys=True).split('\n'):
        logger.info(line)

    pong = None
    try:
        pong = game.Game.NewGame(flags)
        pong.eventLoop()
    except Exception, e:
        for line in traceback.format_exc().split('\n'):
            logger.error(line)
    logger.info("Cleaning up ...")
    try:
        pong.cleanup()
    except Exception, e:
        for line in traceback.format_exc().split('\n'):
            logger.error(line)
    return 0

if __name__ == "__main__":
    sys.exit(main())
