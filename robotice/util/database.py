def get_db_values(config, system_name, plan_name, type='sensors'):
    """return tuple(model_value, real_value)
    """
    db_key_real = '%s.%s.%s.%s' % (system_name, type, plan_name, 'real')
    db_key_model = '%s.%s.%s.%s' % (system_name, type, plan_name, 'model')
    model_value = config.database.get(db_key_model)
    if model_value == None:
        return None, None
    model_value = model_value.replace("(", "").replace(")", "").split(", ")
    if len(model_value) == 1:
        model_value = int(model_value[0])
    else:
        model_value = (int(model_value[0]), int(model_value[1]))
    real_value = config.database.get(db_key_real)
    if real_value != None:
        real_value = int(float(real_value))
    return model_value, real_value