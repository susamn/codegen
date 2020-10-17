import unittest

from generators.java.annotations import Annotation
from generators.java.attribute import Attribute
from generators.java.typs import MODE_PUBLIC


class TestMethods(unittest.TestCase):

    def test_simple_attribute(self):
        m = Attribute("hello", "String", mode=MODE_PUBLIC)
        g = m.generate(4)
        print(g)


    def test_annotated_attribute(self):
        annotation1=Annotation("com.susamn.Foo")
        annotation1.add_data({
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        m = Attribute("hello", "String")
        m.apply_annotation(annotation1)
        g = m.generate(4)
        print(g)


if __name__ == '__main__':
    unittest.main()