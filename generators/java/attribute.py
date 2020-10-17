from generators.java import Generator, padding
from generators.java.typs import MODE_PRIVATE


class Attribute(Generator):
    # TODO Need to support initialization
    def __init__(self, name, typ, mode=None):
        self.name = name
        self.mode = mode or MODE_PRIVATE
        self.typ = typ
        self.annotations = []

    def apply_annotation(self, annotation):
        if annotation:
            self.annotations.append(annotation)

    def get_name(self):
        return self.name

    def get_type(self):
        return self.typ

    def __gt__(self, other):
        if not type(other) == Attribute:
            raise ValueError(f"{other} is not a type that cam be compared to an Attribute")
        if self.annotations and not other.annotations:
            return True

    def generate(self, indentation=0):
        annotation_string = None

        common_structure = f'{padding(indentation)}{self.mode} {self.typ} {self.name};'

        # Calculate the annotation string
        if len(self.annotations) > 0:
            annotation_string = "\n".join([x.generate(indentation=indentation) for x in self.annotations])

        # Add annotations
        if annotation_string:
            common_structure = f'\n{annotation_string}\n{common_structure}'

        return common_structure

