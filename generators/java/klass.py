from generators.java import Generator, class_name_from_package, package_name_from_package
from generators.java.attribute import Attribute
from generators.java.method import Method, getter, setter
from generators.java.typs import ANNOTATION_LEVEL_ATTRIBUTE, process_type, ANNOTATION_LEVEL_GETTER


class Klass(Generator):
    def __init__(self, fqcn, std_indent=4, generate_folder=None, extends=None, implements=None,
                 annotations=None):
        if fqcn:
            self.class_name = class_name_from_package(fqcn)
            self.package = package_name_from_package(fqcn)
        self.imports = set()
        self.attributes = []
        self.methods = []

        # Process inheritance
        self.extends = None
        if extends:
            try:
                self.extends = class_name_from_package(extends)
                self.imports.add(extends)
            except ValueError:
                raise ValueError("Please provide inheritance class and its fqcn")

        # Process class level implementations
        self.implements = None
        if implements and not type(implements) == list:
            raise ValueError("Please provide implementation data properly")
        if implements:
            if len(implements) > 0:
                all_implementation_classes = []
                for i in implements:
                    try:
                        all_implementation_classes.append(class_name_from_package(i))
                        self.imports.add(i)
                    except ValueError:
                        raise ValueError("Please provide implementation class and its fqcn")
                self.implements = ",".join(all_implementation_classes)

        # Process class level annotations
        self.annotations = []
        if annotations and type(annotations) == list and len(annotations) > 0:
            for a in annotations:
                self.imports.add(a.get_fqcn())
                self.annotations.append(a)

        self.std_indent = std_indent
        self.generate_folder = generate_folder

    def process_annotations(self, annotations, apply_to):
        if annotations and apply_to and len(annotations) > 0:
            for a in annotations:
                self.imports.add(a.get_fqcn())
                apply_to.apply_annotation(a)

    def add_method(self, method, imports, annotations=None):
        self.imports.update(imports)
        self.process_annotations(annotations, apply_to=method)
        self.methods.append(method)

    def add_attribute(self, attribute, imports, annotations=None):
        self.imports.update(imports)
        self.process_annotations(annotations, apply_to=attribute)
        self.attributes.append(attribute)

    def add_attribute_with_accessors(self, attribute, imports, annotation_level=None, annotations=None):
        self.imports.update(imports)
        annotation_level = annotation_level or ANNOTATION_LEVEL_ATTRIBUTE
        if annotation_level == ANNOTATION_LEVEL_ATTRIBUTE:
            self.process_annotations(annotations, apply_to=attribute)
        self.attributes.append(attribute)

        g = getter(attribute.get_name(), attribute.get_type())
        s = setter(attribute.get_name(), attribute.get_type())
        if annotation_level == ANNOTATION_LEVEL_GETTER:
            self.process_annotations(annotations, g)
        self.methods.append(g)
        self.methods.append(s)

    def add_simple_attribute(self, name, attribute_type, fqcn=None, mode=None, annotations=None):
        typ, import_list = process_type(attribute_type, fqcn=fqcn)
        self.__process_attribute(name, typ, import_list, mode=mode, annotations=annotations)

    def add_simple_attribute_with_accessors(self, name, attribute_type, fqcn=None, mode=None,
                                            annotation_level=ANNOTATION_LEVEL_ATTRIBUTE, annotations=None):
        typ, import_list = process_type(attribute_type, fqcn=fqcn)
        if annotation_level == ANNOTATION_LEVEL_ATTRIBUTE:
            self.__process_attribute(name, typ, import_list, mode=mode, annotations=annotations)
        else:
            self.__process_attribute(name, typ, import_list, mode=mode)
        g = getter(name, typ)
        s = setter(name, typ)
        if annotation_level == ANNOTATION_LEVEL_GETTER:
            self.process_annotations(annotations, g)
        self.methods.append(g)
        self.methods.append(s)

    def __process_attribute(self, name, typ, import_list, mode=None, annotations=None):
        if typ:
            att = Attribute(name, typ, mode=mode)
            if annotations and len(annotations) > 0:
                self.process_annotations(annotations, att)
            self.attributes.append(att)
            if import_list and len(import_list) > 0:
                self.imports.update(import_list)
        else:
            raise ValueError(f"The list attribute {name} could not be added")

    def add_simple_method(self, name, output, mode=None, fqcn=None, annotations=None):
        if name and output:
            method_return_type, import_list = process_type(output, fqcn=fqcn)
            if method_return_type:
                m = Method(name, method_return_type, mode=mode)
                if annotations and len(annotations) > 0:
                    self.process_annotations(annotations, m)
                self.methods.append(m)
                if import_list and len(import_list) > 0:
                    self.imports.update(import_list)
            else:
                raise ValueError(f"The list method {name} of type {output} could not be added")
        else:
            raise ValueError("Check your method arguments")

    def handle_inheritance_and_implementation(self):
        response = f"public class {self.class_name}"
        if self.extends:
            response = f"{response} extends {self.extends}"
        if self.implements:
            response = f"{response} implements {self.implements}"
        return response

    def generate(self, indentation=4):
        generated = ""
        generated += f'package {self.package};'
        generated += "\n\n"
        self.imports = sorted(self.imports)
        for i in self.imports:
            generated += f'import {i};\n'
        generated += "\n\n"
        if len(self.annotations) > 0:
            generated += "\n".join([x.generate() for x in self.annotations])
        generated += f"\n{self.handle_inheritance_and_implementation()} {{"
        generated += "\n\n"
        self.attributes = sorted(self.attributes)
        for att in self.attributes:
            generated += att.generate(indentation=indentation)
            generated += "\n"
        generated += "\n"
        for meth in self.methods:
            generated += meth.generate(indentation=indentation)
            generated += "\n"
        generated += "\n"
        generated += f"}}"

        if self.generate_folder:
            with open("/".join([self.generate_folder, f'{self.class_name}.java']), "w") as fh:
                fh.write(generated)
                fh.flush()
            print(f'Written java class {self.generate_folder}/{self.class_name}.java')
        else:
            print(generated)
