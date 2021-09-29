
"""
"""

# Native
import time
import pprint

# 3rd-Party
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

#
from foe.request import Request
from foe.models.model import Model
from foe.models.resources import Resources
from foe.models.unit_slot import UnitSlot



class Building(Model):
    """
    """

    REQUEST_CLASS = 'CityProductionService'

    __tablename__ = 'building'

    # Attributes
    # ---------------------------------------------------------

    id = Column(Integer, primary_key=True, default=0)

    connected = Column(Integer, default=0)

    x = Column(Integer, default=0)

    y = Column(Integer, default=0)

    type = Column(String, default='')

    cityentity_id = Column(String, default='')

    level = Column(String, default='')
    # Custom field to denormalize state into
    state = Column(String, default='')
    # Custom field so we can keep track of when stuff should be collected
    collection_time = Column(Float, default=0)

    # Back-refs
    # ---------------------------------------------------------

    city_id = Column(String, ForeignKey('city.id'))

    # Containers
    # ---------------------------------------------------------

    unitSlots = relationship(UnitSlot, backref=backref('building', uselist=False))

    def __repr__(self):
        """
        """

        return "Building %s (%s)" % (self.id, self.cityentity_id)

    def populate(self, *args, **kwargs):
        """
        """

        for key in ['player_id', 'clan', 'clan_id', 'topAchievements', '__class__']:
            kwargs.pop(key, None)

        # set ID in advance so relationships will be working correctly
        for key in ['id']:
            setattr(self, key, kwargs.pop(key))

        state = kwargs.pop('state')

        if 'unitSlots' in kwargs:
            unitSlots = kwargs.pop('unitSlots')
            for raw_unit_slot in unitSlots:

                unitNr = 0 if 'nr' not in raw_unit_slot else raw_unit_slot['nr']
                unitSlot = self.session.query(UnitSlot).filter_by(entity_id=raw_unit_slot['entity_id'], nr=unitNr).first()
                if not unitSlot:
                    unitSlot = UnitSlot(building=self)

                unitSlot.update(**raw_unit_slot)

        if state:

            self.state = state['__class__']

            if self.state == 'ProducingState':
                self.collection_time = time.time() + state['next_state_transition_in']

            elif self.state == 'ProductionFinishedState':
                self.collection_time = time.time()

            elif self.state == 'IdleState':
                self.collection_time = 0
                # Technically 'next_state_transition_in' would tell us when the build finishes
                # So we could work out when its first produce would finish..let the update handle this for now
            elif self.state == 'ConstructionState':
                self.collection_time = 0
            elif self.state == 'UnconnectedState':
                self.collection_time = 0
            else:
                # State we don't know about... so print it
                pprint.pprint(state)

        return super(Building, self).populate(*args, **kwargs)

    def update_state_from_response(self, data):
        """
   
        """

        updated = Request.service(data, 'CityProductionService')['updatedEntities']

        if updated:
            for item in updated:
                if item['id'] == self.id and item['cityentity_id'] == self.cityentity_id :
                    self.update(**item)
                    break

        resources_response = Request.service(data, 'ResourceService')

        if resources_response and 'resources' in resources_response:

            resources_response = resources_response['resources']

            resources = self.session.query(Resources).first()
            if resources_response and resources:
                resources.update(**resources_response)

        return self

    def produce(self):
        """
        Starts production in the building
        """

        if self.type in ['residential']:
            return None

        if self.collection_time:
            return None

        if self.state in ['ProducingState', 'ProductionFinishedState', 'ConstructionState', 'UnconnectedState']:
            return None

        # NOTE: '1' means the first slot, which is 5 minutes for supplies or 4 hours for resources
        slot = 1

        if self.type == 'military':
            # Try to find free military slot
            slot = -1
            if self.unitSlots:

                free_slot = list(filter(lambda slot: slot.unlocked and slot.unit_id == -1 and not slot.is_training, self.unitSlots))

                if len(free_slot) > 0:
                    slot = free_slot[0].nr

            if slot == -1:
                return None

        response = self.request('startProduction', [self.id, slot])

        print("%s started production" % (self))

        self.update_state_from_response(response)

        return response

    def pickup(self):
        """
        Picks up/gather the coins/supplies/resources from the building
        """

        if not self.pickupable():
            return None

        response = self.request('pickupProduction', [[self.id]])

        print("%s picked up production" % (self))

        self.update_state_from_response(response)

        return response

    def pickupable(self):
        """
        Returns True if the build is ready to be picked up
        """

        if not self.collection_time:
            return False

        if self.collection_time > time.time():
            return False

        if self.state in ['ConstructionState', 'UnconnectedState']:
            return False

        return True


    def cancel(self):
        """
        Cancels the current prodution of the building, reverting it to the idle state
        """

        if self.type == 'residential':
            return None

        response = self.request('cancelProduction', [[self.id]])

        print("%s cancelled production" % (self))

        #
        self.collection_time = 0
        self.state = 'IdleState'

        return response
