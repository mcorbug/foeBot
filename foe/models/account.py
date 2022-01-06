
"""
"""

# Native
import time
import pprint
from collections import OrderedDict
import json

# 3rd-Party
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, backref

import pydash

#
from foe.request import Request
from foe.models.model import Model
from foe.models.city import City
from foe.models.player import Player
from foe.models.tavern import Tavern
from foe.models.resources import Resources
from foe.models.hiddenReward import HiddenReward


class Account(Model):
    """
    """

    REQUEST_CLASS = "StartupService"

    __tablename__ = 'account'

    # Attributes
    # ---------------------------------------------------------

    player_id = Column(Integer, primary_key=True, default=0)

    id = Column(String, default=0)

    user_name = Column(String, default='', unique=True)

    # Back-refs
    # ---------------------------------------------------------

    # Containers
    # ---------------------------------------------------------

    city = relationship(City, backref=backref('account', uselist=False), uselist=False)

    players = relationship(Player, backref=backref('account', uselist=False))

    taverns = relationship(Tavern, backref=backref('account', uselist=False))

    resources = relationship(Resources, backref=backref('account', uselist=False), uselist=False)

    hiddenRewards = relationship(HiddenReward, backref=backref('account', uselist=False))

    def __repr__(self):
        """
        """

        return "Account %s (%s)" % (self.player_id, self.user_name)

    def fetch(self):
        """
        Does a HTTP request to get the start up blob for the city, then populates the models
        """

        print("%s fetching..." % (self))

        timer = time.time()

        data = self.request('getData', [])

        account = Request.service(data, 'StartupService')
        account['taverns'] = Request.method(data, 'getOtherTavernStates')
        account['resources'] = Request.method(data, 'getPlayerResources')['resources']
        # account['hiddenRewards'] = Request.method(data, 'getOverview')['hiddenRewards']

        self.update(**account)

        print("%s fetched in %.2fs" % (self, time.time() - timer))

        return self

    def updateFromResponse(self, data):
        """
        """

        if not data:
            return self

        resources = Request.method(data, 'getPlayerResources')['resources']

        if resources:
            self.resources.update(**resources)

        return self

    def populate(self, *args, **kwargs):
        """
        """

        user = kwargs.pop('user_data')
        social = kwargs.pop('socialbar_list')
        taverns = kwargs.pop('taverns')
        city = kwargs.pop('city_map')
        resources = kwargs.pop('resources')
        # hiddenRewards = kwargs.pop('hiddenRewards')

        for key in ['player_id', 'user_name']:
            setattr(self, key, user[key])

        for key in list(kwargs.keys()):
            kwargs.pop(key)

        # City

        if not self.city:
            self.city = City(account=self)

        self.city.update(**city)

        # Players

        for raw_player in social:

            player = self.session.query(Player).filter_by(player_id=raw_player['player_id']).first()
            if not player:
                player = Player(account=self)

            player.update(**raw_player)

        # Taverns

        for raw_tavern in taverns:

            tavern = self.session.query(Tavern).filter_by(ownerId=raw_tavern['ownerId']).first()
            if not tavern:
                tavern = Tavern(account=self)

            tavern.update(**raw_tavern)

        # Resources

        if not self.resources:
            self.resources = Resources(account=self)

        self.resources.update(**resources)

        # hiddenRewards
        """
        for raw_hiddenReward in hiddenRewards:

            hiddenReward = self.session.query(HiddenReward).filter_by(hiddenRewardId=raw_hiddenReward['hiddenRewardId']).first()
            if not hiddenReward:
                hiddenReward = HiddenReward(account=self)

            hiddenReward.update(**raw_hiddenReward)
        """

        return super(Account, self).populate(*args, **kwargs)
