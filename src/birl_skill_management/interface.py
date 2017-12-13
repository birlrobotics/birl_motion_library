from core import PickleStorer, PickleExtracter

def store_skill(data_id, data):
    PickleStorer(data_id, data)

def extract_skill(data_id):
    data = PickleExtracter(data_id)
    return data
