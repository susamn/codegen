import unittest

from generators.java.annotations import Annotation
from generators.java.method import Method, getter, setter
from generators.java.typs import MODE_PRIVATE


class TestMethods(unittest.TestCase):

    def test_simple_method(self):
        m = Method("hello", "String", mode=MODE_PRIVATE)
        g = m.generate(4)
        print(g)


    def test_arg_method(self):
        m = Method("hello", "String")
        m.add_input("ArrayList<String>")
        m.add_input("String")
        g = m.generate(4)
        print(g)

    def test_body_method(self):
        m = Method("hello", "String")
        m.add_body("this.val = val;")
        g = m.generate(4)
        print(g)


    def test_annotated_method(self):
        m = Method("hello", "String")
        annotation=Annotation("com.susamn.Foo")
        annotation.add_data({
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        m.apply_annotation(annotation)
        g = m.generate(4)
        print(g)

    def test_multiple_annotated_method(self):
        m = Method("hello", "String")
        annotation1=Annotation("com.susamn.Foo")
        annotation1.add_data(data={
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        annotation2=Annotation("com.susamn.Bar")
        annotation2.add_data(data={
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        m.apply_annotation(annotation1)
        m.apply_annotation(annotation2)
        g = m.generate(4)
        print(g)


    def test_arg_method_with_annotation(self):
        m = Method("hello", "String")
        m.add_input("ArrayList<String>")
        m.add_input("String")
        annotation1=Annotation("com.susamn.Foo")
        annotation1.add_data(data={
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        annotation2=Annotation("com.susamn.Bar")
        annotation2.add_data({
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        m.apply_annotation(annotation1)
        m.apply_annotation(annotation2)
        g = m.generate(4)
        print(g)

    def test_arg_method_with_annotation_and_body(self):
        m = Method("hello", "String")
        m.add_input("ArrayList<String>")
        m.add_input("String")
        annotation1=Annotation("com.susamn.Foo")
        annotation1.add_data({
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        annotation2=Annotation("com.susamn.Bar")
        annotation2.add_data({
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        m.apply_annotation(annotation1)
        m.apply_annotation(annotation2)
        m.add_body("this.val = val;")
        g = m.generate(4)
        print(g)

    def test_getter(self):
        m = getter("foo", "String")
        print(m.generate())

    def test_setter(self):
        m = setter("foo", "String")
        print(m.generate())


if __name__ == '__main__':
    unittest.main()