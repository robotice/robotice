
import logging
import pickle
from redis import StrictRedis

LOG = logging.getLogger(__name__)

class PickledRedis(StrictRedis):
    """custom picled redis
    """

    def hgetall(self, name):
        pickled_value = super(PickledRedis, self).hgetall(name)

        for key, value in pickled_value.iteritems():
            try:
                pickled_value[key] = pickle.loads(value)
            except Exception, e:
                pass
        return pickled_value

    def get(self, name):
        pickled_value = super(PickledRedis, self).get(name)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super(PickledRedis, self).set(name, pickle.dumps(value), ex, px, nx, xx)

def get_db_values(config, system_name, plan_name):
    """return tuple(model_value, real_value)
    """
    db_key_real = ':'.join([str(system_name), str(plan_name), 'real'])
    db_key_model = ':'.join([str(system_name), str(plan_name), 'model'])
    model_value = config.database.get(db_key_model)
    
    if model_value == None:
        return None, None
    if isinstance(model_value, basestring):
        model_value = model_value.replace("(", "").replace(")", "").split(", ")
        if len(model_value) == 1:
            model_value = int(model_value[0])
        else:
            model_value = (int(model_value[0]), int(model_value[1]))
    real_value = config.database.get(db_key_real)
    if real_value != None:
        real_value = int(float(real_value))
    return model_value, real_value