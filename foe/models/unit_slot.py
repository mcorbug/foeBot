
"""
"""

# Native

# 3rd-Party
from sqlalchemy import Column, Integer, Boolean, ForeignKey

#
from foe.models.model import Model

class UnitSlot(Model):
    """
    """

    REQUEST_CLASS = 'CityProductionService'

    __tablename__ = 'unity_slot'

    # Attributes
    # ---------------------------------------------------------

    nr = Column(Integer, primary_key=True, default=0)

    unit_id = Column(Integer, default=0)

    is_training = Column(Boolean, default=False)

    is_unlockable = Column(Boolean, default=False)

    unlocked = Column(Boolean, default=False)

    # Back-refs
    # ---------------------------------------------------------

    entity_id = Column(Integer, ForeignKey('building.id'), primary_key=True)

    # Containers
    # ---------------------------------------------------------

    def __repr__(self):
        """
        """

        return "Unit slot nr %s (building %s)" % (self.nr, self.entity_id)

    def populate(self, *args, **kwargs):
        """
        """

        for key in ['unlock_costs', 'unit', 'unlockCosts']:
            kwargs.pop(key, None)        

        if 'nr' not in kwargs:
            kwargs['nr'] = 0

        return super(UnitSlot, self).populate(*args, **kwargs)
