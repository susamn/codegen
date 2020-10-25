import unittest

from generators.java import TYPE_CLASS
from generators.java.klass import Klass


class MyTestCase(unittest.TestCase):
    def test_simple_class(self):
        doc={
            "fqcn": "com.susamn.MetaEnum",
            "type": TYPE_CLASS
        }
        m = Klass(doc)
        g = m.generate(4)
        print(g)

    def test_simple_class_with_attributes(self):
        doc={
            "fqcn": "com.susamn.MetaClass",
            "type": TYPE_CLASS,
            "attributes": [
                {
                    "name": "logger",
                    "mode": "public",
                    "type": {
                        "of": TYPE_CLASS,
                        "fqcn": "org.slf4j.api.Logger"
                    }
                }]
        }
        m = Klass(doc)
        g = m.generate(4)
        print(g)

    def test_simple_class_with_attribute_accessors(self):
        doc={
            "fqcn": "com.susamn.MetaClass",
            "type": TYPE_CLASS,
            "attributes": [
                {
                    "name": "logger",
                    "mode": "public",
                    "type": {
                        "of": TYPE_CLASS,
                        "fqcn": "org.slf4j.api.Logger"
                    },
                    "accessors": True
                }]
        }
        m = Klass(doc)
        g = m.generate(4)
        print(g)


    def test_simple_class_with_attribute_accessors(self):
        doc={
            "fqcn": "com.susamn.MetaClass",
            "type": TYPE_CLASS,
            "attributes": [
                {
                    "name": "logger",
                    "mode": "public",
                    "type": {
                        "of": TYPE_CLASS,
                        "fqcn": "org.slf4j.api.Logger"
                    },
                    "initialized_form": {
                        "form": "LoggerFactory.getLogger(RiskAssessmentController.class)",
                        "imports": ["org.apache.logger.api.LoggerFactory","com.susamn.RiskAssessmentController"]
                    }
                }]
        }
        m = Klass(doc)
        g = m.generate(4)
        print(g)


if __name__ == '__main__':
    unittest.main()
