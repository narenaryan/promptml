from unittest import TestCase
from src.promptml.serializer import (
    SerializerFactory,
    XMLSerializer,
    JSONSerializer,
    YAMLSerializer
)

class TestSerializer(TestCase):
    def test_create_serializer(self):
        self.assertIsInstance(SerializerFactory.create_serializer("xml"), XMLSerializer)
        self.assertIsInstance(SerializerFactory.create_serializer("json"), JSONSerializer)
        self.assertIsInstance(SerializerFactory.create_serializer("yaml"), YAMLSerializer)
        self.assertRaises(ValueError, SerializerFactory.create_serializer, "invalid")
