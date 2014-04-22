from blitzdb import Document

class Plan(Document):

    class Meta(Document.Meta):
       collection = 'plans'

class System(Document):

    class Meta(Document.Meta):
       collection = 'systems'

class Device(Document):
    
    class Meta(Document.Meta):
       collection = 'devices'

class Sensor(Document):

    class Meta(Document.Meta):
       collection = 'sensors'

class Config(Document):

    class Meta(Document.Meta):
       collection = 'configs'