from generators.java import Generator, padding, class_name_from_package, package_name_from_package
from generators.java.method import Method
from generators.java.typs import MODE_PRIVATE, MODE_PUBLIC, TYPE_STRING, process_type


class Enum(Generator):
    # TODO Need to support initialization
    def __init__(self, fqcn, mode=None, implements=None, generate_folder=None):
        if fqcn:
            self.class_name = class_name_from_package(fqcn)
            self.package = package_name_from_package(fqcn)
        self.mode = mode or MODE_PRIVATE
        self.annotations = []
        self.enums = []
        self.imports = set()

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

        self.generate_folder = generate_folder

    def add_enum(self, value):
        if value:
            self.enums.append(value)

    def apply_annotation(self, annotation):
        if annotation:
            self.annotations.append(annotation)

    def handle_inheritance_and_implementation(self):
        response = f"public enum {self.class_name}"
        if self.implements:
            response = f"{response} implements {self.implements}"
        return response

    def generate(self, indentation=4):

        typ, ims = process_type(TYPE_STRING)
        self.imports.update(ims)

        method_from_value = Method("fromValue", self.class_name, mode=MODE_PUBLIC, is_static=True)
        method_from_value.add_named_input(typ, "value")
        method_from_value.add_body("return valueOf(value);")

        method_getter = Method(f'getValue', typ, mode=MODE_PUBLIC)
        method_getter.add_body(f'return this.toString();')

        generated = ""
        generated += f'package {self.package};'
        generated += "\n\n"
        self.imports = sorted(self.imports)
        for i in self.imports:
            generated += f'import {i};\n'
        generated += "\n\n"
        generated += f"\n{self.handle_inheritance_and_implementation()} {{"
        generated += "\n"
        self.enums = sorted(self.enums)

        enum_string = f'{padding(indentation)}{",".join(self.enums)};'
        generated += enum_string
        generated += "\n"

        generated += "\n"
        generated += method_from_value.generate(indentation=indentation)
        generated += "\n"
        generated += method_getter.generate(indentation=indentation)
        generated += "\n"
        generated += "\n"
        generated += f"}}"

        if self.generate_folder:
            with open("/".join([self.generate_folder, f'{self.class_name}.java']), "w") as fh:
                fh.write(generated)
                fh.flush()
            print(f'Written java enum {self.generate_folder}/{self.class_name}.java')
        else:
            print(generated)


