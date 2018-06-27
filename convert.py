#!/usr/bin/python3.6

class conversion_parameters:
    def __init__(self,type_function, behaviour, default_value = None, true_value = "True", false_value = "False"):
        self.type_function = type_function
        self.behaviour = behaviour #chaine de caractere qui est soit mean soit median soit default_value soit delete
        self.default_value = default_value # la valeur par defaut eventuelle , pour bool elle est soir true value soit false value
        self.true_value = true_value
        self.false_value = false_value

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