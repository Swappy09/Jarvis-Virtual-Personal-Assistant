import ast
import json
config_file = "config.json"
def get(key):
    config = dict()
    try:
        
        config = json.load(open(config_file))
        if key in config:
            return config[key]
        else:
            None
    except Exception as e:
        print("There is error in Config.py",e)
        return None
def set_tag(key,value):
    config = dict()
    try:
        
        config = json.load(open(config_file))
        config['TAGS'][key]=value.upper()
        write_to_json(config)
        return True
    except Exception as e:
        print("There is error in Config.py",e)
        return None
def set(key,value):
    config = dict()
    try:
      
        config = json.load(open(config_file))
        config[key]=value
        write_to_json(config)
        return True
    except Exception as e:
        print("There is error in Config.py",e)
        return None
def getApps():
    try:
        return json.load(open("Apps_cmd.json"))
    except Exception as e:
        print("There is error in Config.py :",e)
        return None
def get_json_dict():
    j = json.load(open(config_file))
    return j
def write_to_json(dict_obj):
    import json
    json_data = json.dumps(dict_obj)
    f = open(config_file,'w')
    f.write(str(json_data))
    f.close()

if __name__ == "__main__":
    print(get("TAGS"))
    print(set("INPUT MODE","TEXT"))