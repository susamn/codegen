import unittest

from generators.java.annotations import Annotation


class TestAnnotations(unittest.TestCase):

    def test_simple_annotation(self):
        m = Annotation("Scheduled")
        g = m.generate(4)
        print(g)

    def test_annotation_with_data_primitive_int(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "INTEGER",
                "value": 23
            }
        })
        g = m.generate(4)
        print(g)

    def test_annotation_with_data_primitive_float(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "INTEGER",
                "value": 23.80
            }
        })
        g = m.generate(4)
        print(g)

    def test_annotation_with_data_string(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "STRING",
                "value": "Some string data"
            }
        })
        g = m.generate(4)
        print(g)

    def test_annotation_with_data_evaluated(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "EVALUATED",
                "value": "RequestConstants.HTTP_CODE"
            }
        })
        g = m.generate(4)
        print(g)


    def test_annotation_with_data_class(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "CLASS",
                "value": "com.susamn.SomeClass"
            }
        })
        g = m.generate(4)
        print(g)

    def test_annotation_with_data_annotation(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "ANNOTATION",
                "value": {
                    "fqcn": "com.susamn.Annotation1",
                    "data": {
                        "key12": {
                            "type": "INTEGER",
                            "value": 23
                        }
                    }
                }
            }
        })
        g = m.generate(4)
        print(g)

    def test_annotation_with_data_nested_annotation(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "ANNOTATION",
                "value": {
                    "fqcn": "com.susamn.Annotation1",
                    "data": {
                        "key11": {
                            "type": "ANNOTATION",
                            "value": {
                                "fqcn": "com.susamn.Annotation2",
                                "data": {
                                    "key111": {
                                        "type": "INTEGER",
                                        "value": 23
                                    }
                                }
                            }
                        }
                    }
                }
            }
        })
        g = m.generate(4)
        print(g)


    def test_annotation_with_data_list_annotation(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "LIST_ANNOTATION",
                "value": [
                    {
                        "fqcn": "com.susamn.Annotation1",
                        "data": {
                            "key1": {
                                "type": "FLOAT",
                                "value": 23.20
                            },
                            "key2":{
                                "type": "CLASS",
                                "value": "com.susamn.Comcast"
                            }
                        }
                    },
                    {
                        "fqcn": "com.susamn.Annotation2",
                        "data": {
                            "key1": {
                                "type": "INTEGER",
                                "value": 67
                            }
                        }
                    }
                ]
            }
        })
        g = m.generate(4)
        print(g)


    def test_annotation_with_data_list_primitive(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "LIST_INTEGER",
                "value": [12, 23, 34]
            }
        })
        g = m.generate(4)
        print(g)


    def test_annotation_with_data_list_class(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "LIST_CLASS",
                "value": ["com.susamn.Comcast","com.susamn.SomeClass"]
            }
        })
        g = m.generate(4)
        print(g)


    def test_annotation_with_data_list_string(self):
        m = Annotation("Scheduled")
        m.add_data({
            "key1": {
                "type": "LIST_STRING",
                "value": ["some string 1","some string 2"]
            }
        })
        g = m.generate(4)
        print(g)


if __name__ == '__main__':
    unittest.main()
