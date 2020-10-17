import json

from generators.java import class_name_from_package, package_name_from_package
from generators.java.annotations import Annotation
from generators.java.attribute import Attribute
from generators.java.enum import Enum
from generators.java.klass import Klass
from generators.java.method import Method
from generators.java.typs import process_type, TYPE_CLASS, TYPE_ENUM


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
                if mapping_type == TYPE_CLASS:
                    generate_class(mapping, folder)
                elif mapping_type == TYPE_ENUM:
                    generate_enum(mapping, folder)

    else:
        raise ValueError("Please check your provided data")

def generate_enum(mapping, folder):
    enum_fqcn = mapping.get("fqcn")
    values = mapping.get("values")
    if not enum_fqcn or not values or not type(values) == list or len(values) == 0:
        raise ValueError("Check the enum parameters, it seems to be faulty")
    enum = Enum(enum_fqcn, generate_folder=folder)
    for val in values:
        enum.add_enum(val)

    # Generate the enum
    enum.generate()


def generate_class(mapping, folder):
    fully_qualified_class_name = mapping.get("fqcn")
    class_name = class_name_from_package(fully_qualified_class_name)
    class_package = package_name_from_package(fully_qualified_class_name)


    extends_info = mapping.get("extends")
    implements_info = mapping.get("implements")

    class_annotations_data = mapping.get("annotations")
    class_annotations = parse_annotations(class_annotations_data)

    if not class_name or not class_package:
        raise ValueError("The class name and package must be provided")

    clazz = Klass(fully_qualified_class_name, generate_folder=folder, extends=extends_info,
                  implements=implements_info, annotations=class_annotations)

    # Handle attributes
    attributes = mapping.get("attributes")
    if not attributes or len(attributes) == 0:
        raise ValueError("The attributes section is empty, you are not trying to crate an empty class, aren't you?")
    for attribute in attributes:
        if attribute:
            attribute_name = attribute.get("name")
            attribute_mode = attribute.get("mode")
            attribute_type = attribute.get("type")
            attribute_accessors_generate = attribute.get("accessors")
            annotation_level = attribute.get("annotation_level")

            # Type information fetching
            typ, imports = obtain_type(attribute_name, attribute_type)

            # Form the attribute
            att = Attribute(attribute_name, typ, mode=attribute_mode)

            if att:
                annotation_map = attribute.get("annotations")
                annotations = parse_annotations(annotation_map)
                if attribute_accessors_generate:
                    clazz.add_attribute_with_accessors(att, imports, annotation_level=annotation_level,
                                                   annotations=annotations)
                else:
                    clazz.add_attribute(att, imports, annotations=annotations)

    # Handle methods
    methods = mapping.get("methods")
    if methods and len(methods) > 0:
        for method in methods:
            method_name = method.get("name")
            method_mode = method.get("mode")
            method_type = method.get("type")

            # Type check of the method
            typ, method_imports = obtain_type(method_name, method_type)

            if not typ:
                raise ValueError(f"The return type of method {method_name} could not be obtained")

            meth = Method(method_name, method_mode, typ)

            inputs = method.get("inputs")
            if inputs and len(inputs) > 0:
                for i in inputs:
                    input_type_information = i.get("type")
                    if not input_type_information:
                        raise ValueError(f"The input type of method {method_name} could not be found")
                    method_input_type, method_input_imports = obtain_type(method_name, input_type_information)
                    if not method_input_type:
                        raise ValueError(f"The input type of method {method_name} could not be parsed")
                    # Add method input type
                    meth.add_input(method_input_type)
                    if len(method_input_imports) > 0:
                        method_imports.extend(method_input_imports)

            if meth:
                method_annotations_info = method.get("annotations")
                method_annotations = parse_annotations(method_annotations_info)

                clazz.add_method(meth, method_imports, annotations=method_annotations)

    # Generate the class
    clazz.generate()


# Helper methods

def parse_annotations(annotations=None):
    result = list()
    if annotations and len(annotations) > 0:
        for annotation in annotations:
            annotation_package = annotation.get("fqcn")
            annotation_data = annotation.get("data")
            if not annotation_package:
                raise ValueError("If you are providing annotation, it must have package and data")
            if annotation_package:
                a = Annotation(annotation_package)
                if annotation_data:
                    a.add_data(annotation_data)
                result.append(a)
    return result


def __get_type_checked(name, doc):
    if not doc or not type(doc) == dict:
        raise ValueError(f"Please check the type information of member {name}")


# Obtain type information
def obtain_type(name, doc):
    __get_type_checked(name, doc)

    # Type information
    type_of = doc.get("of")
    object_fqcn = doc.get("fqcn")
    annotations_info = doc.get("annotations")

    annotations = None
    if annotations_info:
        annotations = parse_annotations(annotations_info)

    if not type_of:
        raise ValueError("Check attribute section, it is not properly structured")

    typ, imports = process_type(type_of, fqcn=object_fqcn, annotations=annotations)
    if not typ:
        raise ValueError("The attribute type could not be parsed")
    return typ, imports
