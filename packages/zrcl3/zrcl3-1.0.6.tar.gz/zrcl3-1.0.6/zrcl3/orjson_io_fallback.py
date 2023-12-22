import json
try:
    import orjson
except: # noqa
    orjson = None

def load_json(filename : str):
    try:
        if orjson:
            with open(filename, 'rb') as f:
                return orjson.loads(f.read())
        else:
            with open(filename, 'r') as f:
                return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, orjson.JSONDecodeError):
        return {}
    
def save_json(filename : str, data : dict):
    if orjson:
        with open(filename, 'wb') as f:
            f.write(orjson.dumps(data))
    else:
        with open(filename, 'w') as f:
            json.dump(data, f)
