from generators.java import class_name_from_package

MODE_PRIVATE = "private"
MODE_PROTECTED = "protected"
MODE_PUBLIC = "public"

TYPE_INTEGER = "INTEGER"
TYPE_FLOAT = "FLOAT"
TYPE_BOOLEAN = "BOOLEAN"
TYPE_STRING = "STRING"
TYPE_EVALUATED = "EVALUATED"
TYPE_CLASS = "CLASS"
TYPE_ENUM = "ENUM"
TYPE_ANNOTATION = "ANNOTATION"
TYPE_LIST = "LIST"
TYPE_LIST_INTEGER = "LIST_INTEGER"
TYPE_LIST_FLOAT = "LIST_FLOAT"
TYPE_LIST_BOOLEAN = "LIST_BOOLEAN"
TYPE_LIST_STRING = "LIST_STRING"
TYPE_LIST_CLASS = "LIST_CLASS"
TYPE_LIST_EVALUATED = "LIST_EVALUATED"
TYPE_LIST_ANNOTATION = "LIST_ANNOTATION"
TYPE_VOID = "void"

ANNOTATION_LEVEL_ATTRIBUTE = "ATTRIBUTE_ANNOTATION"
ANNOTATION_LEVEL_GETTER = "GETTER_ANNOTATION"
ANNOTATION_LEVEL_METHOD = "METHOD_ANNOTATION"


def process_type(typ, fqcn=None, annotations=None):
    import_list = []
    final_type = None

    if typ.upper() == TYPE_VOID:
        final_type = "void"
    if typ == TYPE_STRING:
        import_list.append("java.lang.String")
        final_type = "String"
    elif typ == TYPE_INTEGER:
        final_type = "int"
    elif typ == TYPE_FLOAT:
        final_type = "float"
    elif typ == TYPE_BOOLEAN:
        final_type = "boolean"
    elif typ == TYPE_CLASS:
        if not fqcn:
            raise ValueError("For custom type, the fqcn of the class must be provided")
        final_type = class_name_from_package(fqcn)
        import_list.append(fqcn)
    elif typ == TYPE_LIST_STRING:
        final_type = "List<String>"
        import_list.append("java.util.List")
        import_list.append("java.lang.String")
    elif typ == TYPE_LIST_INTEGER:
        final_type = "List<Integer>"
        import_list.append("java.util.List")
        import_list.append("java.lang.Integer")
    elif typ == TYPE_LIST_FLOAT:
        final_type = "List<Float>"
        import_list.append("java.util.List")
        import_list.append("java.lang.Float")
    elif typ == TYPE_LIST_BOOLEAN:
        final_type = "List<Boolean>"
        import_list.append("java.util.List")
        import_list.append("java.lang.Boolean")
    elif typ == TYPE_LIST_CLASS:
        if not fqcn:
            raise ValueError("For custom type, the fqcn of the class must be provided")
        final_type = f"List<{class_name_from_package(fqcn)}>"
        import_list.append("java.util.List")
        import_list.append(fqcn)

    if annotations and len(annotations) > 0:
        for a in annotations:
            final_type = f'{a.generate()} {final_type}'
            import_list.append(a.get_fqcn())

    return final_type, import_list
