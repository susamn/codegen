import json

from generators.java.enum import Enum
from generators.java.interface import Interface
from generators.java.klass import Klass
from generators.java.typs import  TYPE_CLASS, TYPE_ENUM, TYPE_INTERFACE


def engage(file=None, data=None):
    """
    :param file: The mapping file which will be used to generate the classes
    :param data: The mapping data as dict or json payload to do the same thing
    :return: Does not return anything, generates the class files
    """
    if file:
        with open(file, 'r') as f:
            payload = json.load(f)
    else:
        payload = data
    if payload:
        folder = payload.get("generate_path")
        classes = payload.get("classes")
        if classes and len(classes) > 0:
            for mapping in classes:
                mapping_type = mapping.get("type")
                if not mapping_type:
                    raise ValueError("Can't determine the mapping type, please provide the correct type")
                generation = None
                if mapping_type == TYPE_CLASS:
                    generation = Klass(mapping, folder)
                elif mapping_type == TYPE_ENUM:
                    generation = Enum(mapping, folder)
                elif mapping_type == TYPE_INTERFACE:
                    generation = Interface(mapping, folder)

                if generation:
                    generation.generate()

    else:
        raise ValueError("Please check your provided data")

