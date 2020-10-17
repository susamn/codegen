import unittest

from generators.java.annotations import Annotation
from generators.java.klass import Klass
from generators.java.typs import MODE_PRIVATE, MODE_PUBLIC, ANNOTATION_LEVEL_GETTER, TYPE_STRING


class MyTestCase(unittest.TestCase):
    def test_simple_class(self):
        meta = Klass("com.susamn.Meta")
        annotation=Annotation("com.susamn.Foo")
        annotation.add_data(data={
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        meta.add_simple_attribute("foo", TYPE_STRING, annotations=[annotation])
        meta.add_simple_method("process", TYPE_STRING, annotations=[annotation])
        meta.generate()

    def test_simple_class_with_attribute_accessors(self):
        meta = Klass("com.susamn.Meta")
        annotation=Annotation("com.susamn.Foo")
        annotation.add_data(data={
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            },
            "key2": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass2"
            }
        })
        meta.add_simple_attribute_with_accessors("foo", TYPE_STRING, annotation_level=ANNOTATION_LEVEL_GETTER, annotations=[annotation])
        meta.generate()


    def test_simple_class_file_generate(self):
        meta = Klass("com.susamn.Meta", generate_folder="/Users/ssaman002c/data")
        annotation=Annotation("com.susamn.Foo")
        annotation.add_data(data={
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        meta.add_simple_attribute("foo", TYPE_STRING,annotations=[annotation])
        meta.add_simple_method("process", TYPE_STRING,annotations=[annotation])
        meta.generate()


if __name__ == '__main__':
    unittest.main()
