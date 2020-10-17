from generators.java import Generator, to_camel_case, padding
from generators.java.annotations import Annotation
from generators.java.typs import ANNOTATION_LEVEL_ATTRIBUTE, MODE_PUBLIC, TYPE_VOID, MODE_PRIVATE


class Method(Generator):
    def __init__(self, name, output, mode=None, is_abstract=False, is_static=False):
        self.name = name
        self.mode = mode or MODE_PRIVATE
        self.inputs = []
        self.named_inputs = {}
        self.output = output
        self.body = None
        self.annotations = []
        self.isAbstract = is_abstract
        self.isStatic = is_static

    def add_input(self, i):
        if i:
            self.inputs.append(i)

    def add_named_input(self, typ, name):
        if typ and name:
            self.named_inputs[name] = typ

    def apply_annotation(self, annotation):
        if annotation:
            self.annotations.append(annotation)

    def add_body(self, body):
        if body:
            self.body = body

    def generate(self, indentation=0):
        input_string = None
        named_input_string = None
        annotation_string = None

        # Calculate the annotation string
        if len(self.annotations) > 0:
            annotation_string = "\n".join([x.generate(indentation=indentation) for x in self.annotations])

        # Calculate the input string, this is for the inputs, where only the type of the args are known
        if len(self.inputs) > 0:
            input_string = ", ".join([f'{x} val{i}' for i, x in enumerate(self.inputs)])

        # Calculate the input string, this is for the inputs, where the name and type is known
        if len(self.named_inputs) > 0:
            named_input_string = ",".join([f'{y} {x}' for x, y in self.named_inputs.items()])

        # Create the common method structure
        if self.isStatic:
            common_structure = f'{padding(indentation)}{self.mode} static {self.output} {self.name}'
        else:
            common_structure = f'{padding(indentation)}{self.mode} {self.output} {self.name}'

        # Add input arguments
        total_input_string = None
        if input_string and named_input_string:
            total_input_string = f'{named_input_string},{input_string}'
        elif input_string and not named_input_string:
            total_input_string = input_string
        elif named_input_string and not input_string:
            total_input_string = named_input_string

        if total_input_string:
            common_structure = f'{common_structure}({total_input_string})'
        else:
            common_structure = f'{common_structure}()'

        # Add body
        if self.isAbstract:
            common_structure = f'{common_structure};'
        else:
            if self.body:
                common_structure = f'{common_structure}{{\n{padding(indentation+4)}{self.body}\n{padding(indentation)}}}'
            else:
                common_structure = f'{common_structure}{{\n{padding(indentation)}}}'

        # Add annotations
        if annotation_string:
            common_structure = f'{annotation_string}\n{common_structure}'

        return common_structure


def getter(attribute_name, typ):
    method = Method(f'get{to_camel_case(attribute_name)}', typ, mode=MODE_PUBLIC)
    method.add_body(f'return this.{attribute_name};')
    return method


def setter(attribute_name, typ):
    method = Method(f'set{to_camel_case(attribute_name)}', TYPE_VOID, mode=MODE_PUBLIC)
    method.add_named_input(typ, attribute_name)
    method.add_body(f'this.{attribute_name} = {attribute_name};')
    return method

