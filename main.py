
"""
"""

# Native
import sys
import time
from datetime import datetime
import random

# 3rd-Party

# Proprietary
from foe.models.account import Account
from foe.models.tavern import Tavern

from foe import deploy

from foe.db import session

from foe.config import config, load_config

if __name__ == "__main__":
    # --help / -h
    for argument in sys.argv:
        match argument:
            case "--help" | "-h":
                if sys.argv.index(argument) != 0:
                    print("Use the following args to provide specific Parameters")
                    print("--sid / -s \t\t SID from Cookie")
                    print("--userKey / -u \t\t user_key from Request URL")
                    print("--configFile / -c \t foe.yml File with config")
            case "--userKey" | "-u":
                if sys.argv.index(argument) != 0:
                    try:
                        config['login']['user_key'] = (sys.argv[sys.argv.index(argument) + 1])
                    except IndexError:
                        print("No valid Parameter for user_key")
            case "--sid" | "-s":
                if sys.argv.index(argument) != 0:
                    try:
                        config['login']['sid'] = (sys.argv[sys.argv.index(argument) + 1])
                    except IndexError:
                        print("No valid Parameter for SID")
            case "--configFile" | "-c":
                if sys.argv.index(argument) != 0:
                    try:
                        config = load_config(sys.argv[sys.argv.index(argument) + 1])
                    except IndexError:
                        print("No valid Parameter for Config File")

    account = Account()

    session.add(account)

    count = 0

    refresh = random.randrange(config['settings']['update']['min'], config['settings']['update']['max'])

    while True:

        if not count or count >= refresh:
            account.fetch()
            session.commit()

            #break

            print("Players: %s" % (len(account.players)))

            print("Buildings: %s" % (len(account.city.buildings)))

            print("Taverns: %s" % (len(account.taverns)))

            print("Hidden Rewards: %s" % (len(account.hiddenRewards)))

            print("Money: %s" % "{:,}".format(account.resources.money))

            print("Supplies: %s" % "{:,}".format(account.resources.supplies))

            for tavern in account.taverns:
                tavern.sit()

            for hiddenReward in account.hiddenRewards:
                hiddenReward.collect()

            for player in account.players:
                player.aid()

            Tavern.collect()

            session.commit()

            refresh = count + random.randrange(config['settings']['update']['min'], config['settings']['update']['max'])

        print("Checking... (%s)" % (datetime.now().strftime("%H:%M:%S")))
        # NOTE: The full update should adjust for any coins/supplies/resources gained from these pickups
        account.city.pickup()

        account.city.produce()

        session.commit()

        sleep = 30

        time.sleep(sleep)

        count += sleep
