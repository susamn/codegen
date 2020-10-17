from generators.java import Generator, padding
from generators.java.typs import *


class Annotation(Generator):
    def __init__(self, fqcn):
        self.fqcn = fqcn
        self.data = {}

    def get_fqcn(self):
        return self.fqcn

    def add_data(self, data):
        if type(data) is not dict:
            raise ValueError("The data to an annotation can only be a dict, got : ", type(data))
        if len(data) > 0:
            parsed_data = self.__parse_data(data)
            self.data.update(parsed_data)

    def generate(self, indentation=0):
        if len(self.data) == 0:
            return f'{padding(indentation)}@{class_name_from_package(self.fqcn)}'
        else:
            parts = []
            for k, v in self.data.items():
                parts.append(f'{k} = {v}')
            return f'{padding(indentation)}@{class_name_from_package(self.fqcn)}(' + ", ".join(parts) + ')'

    @staticmethod
    def __parse_data(data):
        result_data = {}
        for k, v in data.items():
            value_type = v["type"]
            value_data = v["value"]
            parsed_data = JAVA_ANNOTATION_MAPPER[value_type](value_data)
            result_data[k] = parsed_data
        return result_data


JAVA_ANNOTATION_MAPPER = {
    TYPE_STRING: lambda x: f'"{x}"',
    TYPE_EVALUATED: lambda x: x,
    TYPE_CLASS: lambda x: f'{class_name_from_package(x)}.class',
    TYPE_INTEGER: lambda x: x,
    TYPE_FLOAT: lambda x: x,
    TYPE_BOOLEAN: lambda x: x,
    TYPE_ANNOTATION: lambda x: create_annotation_from_document(x).generate(),
    TYPE_LIST_STRING: lambda x: f'{{{", ".join([wrap_with_quotes(a) for a in x])}}}',
    TYPE_LIST_EVALUATED: lambda x: f'{{{", ".join([a for a in x])}}}',
    TYPE_LIST_CLASS: lambda x: f'{{{", ".join([f"{class_name_from_package(a)}.class" for a in x])}}}',
    TYPE_LIST_INTEGER: lambda x: f'{{{", ".join([str(a) for a in x])}}}',
    TYPE_LIST_FLOAT: lambda x: f'{{{", ".join([str(a) for a in x])}}}',
    TYPE_LIST_BOOLEAN: lambda x: f'{{{", ".join([str(a) for a in x])}}}',
    TYPE_LIST_ANNOTATION: lambda x: f'{{{", ".join([create_annotation_from_document(a).generate() for a in x])}}}'
}


def wrap_with_quotes(val):
    return f'"{val}"'


def create_annotation_from_document(doc):
    if not type(doc) == dict:
        raise ValueError("The document provided to create an annotation is not a dict")
    fqcn = doc.get("fqcn")
    data = doc.get("data")
    if not fqcn:
        raise ValueError("The document provided to create an annotation does not have fqcn")
    a = Annotation(fqcn)
    if data:
        a.add_data(data)
    return a
