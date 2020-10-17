class Generator:
    def generate(self, indentation=0):
        pass


def to_camel_case(s):
    return s[0].upper() + s[1:] if s else s


def padding(indentation):
    return f'{"":>{indentation}}'


def package_name_from_package(clazz):
    splits = clazz.split(".")
    return ".".join(splits[:-1])


def class_name_from_package(clazz):
    splits = clazz.split(".")
    return splits[-1]
