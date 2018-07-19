#!/usr/bin/python3.6
#functions de conversion à passer à apply pour convertir les types:

#string est le type par defaut

#on a soit un cast, soit un remlacement par mediane ou moyenne ou valeur par defaut, ou bien une suppression de la ligne (correspond à un NaN)
import json
from flask.json import JSONEncoder
class my_encoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, conversion_parameters):
            return obj.to_json()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class conversion_parameters:
    def __init__(self,type_function, behaviour, default_value = None, true_value = "True", false_value = "False"):
        self.type_function = type_function
        self.behaviour = behaviour #chaine de caractere qui est soit mean soit median soit default_value soit delete
        self.default_value = default_value # la valeur par defaut eventuelle , pour bool elle est soir true value soit false value
        self.true_value = true_value
        self.false_value = false_value
    
    def to_json(self):
        #return json.dumps(self, default=lambda o: o.__dict__, 
         #   sort_keys=True, indent=4)
        return {
            "type_function": self.type_function,
            "behaviour": self.behaviour,
            "default_value": self.default_value
        }

#type_function est un nom des fonctions ci-dessous

def convert_int (value, parameters):

    try:
        return int(value)
    except:
        if parameters.behaviour == "default_value":
            return parameters.default_value
        else:
            return None


def convert_float(value, parameters):

    try :
        return float(value)
    except:
        if parameters.behaviour == "default_value":
            return parameters.default_value
        else:
            return None




def convert_bool(value, parameters):

    try:
        return bool(value)
    except:
        if value == parameters.true_value:
            return True
        elif value == parameters.false_value:
            return False
        else:
            if parameters.behaviour == "default_value":
                if parameters.default_value == parameters.true_value:
                    return True
                elif parameters.default_value == parameters.false_value:
                    return False
            else:
                return None


def convert_object(value, parameters):

    try:
        return str(value)
    except:
        return ""

def converter(value, parameters):

    try:
        return parameters.type_function(value)
    except:
        if parameters.behaviour == "default_value":
            return parameters.default_value
        else:
            return None

