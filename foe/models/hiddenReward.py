
"""
"""

# Native

# 3rd-Party
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import time
import datetime
import random

#
from foe.request import Request
from foe.models.model import Model

from foe.config import config



class HiddenReward(Model):
    """
    """

    REQUEST_CLASS = 'HiddenRewardService'

    __tablename__ = 'hidden_reward'

    # Attributes
    # ---------------------------------------------------------

    hiddenRewardId = Column(Integer, primary_key=True, default=0)

    startTime = Column(Integer, default=0)

    expireTime = Column(Integer, default=0)

    animated = Column(Boolean, default=False)

    # Back-refs
    # ---------------------------------------------------------

    account_id = Column(Integer, ForeignKey('account.player_id'))

    # Containers
    # ---------------------------------------------------------

    def __repr__(self):
        """
        """

        return "Hidden reward %s from %s => to %s" % (self.hiddenRewardId, datetime.datetime.fromtimestamp(self.startTime).strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.fromtimestamp(self.expireTime).strftime('%Y-%m-%d %H:%M:%S'))

    def populate(self, *args, **kwargs):
        """
        """

        return super(HiddenReward, self).populate(*args, **kwargs)

    def collectable(self):
        """
        """

        if time.time() < self.startTime:
            return False

        if time.time() >= self.expireTime:
            return False

        return True

    def collect(self):
        """
        """

        if not self.collectable():
            return None

        sleep = random.uniform(6, 24)
        time.sleep(sleep)

        print("Collecting hidden reward = %s" % self)

        data = self.request('collectReward', [self.hiddenRewardId])

        # hiddenRewards = Request.service(data, 'HiddenRewardService')

        # print("Collected hidden reward data: %s" % data)

        # Clean up. Otherwise entry will be picked up on the next reload resulting in server error
        self.session.query(HiddenReward).filter_by(hiddenRewardId=self.hiddenRewardId).delete()

        return self