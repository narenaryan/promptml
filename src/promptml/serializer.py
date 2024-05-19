import json
from xml.etree import ElementTree as ET
from xml.dom import minidom
from abc import ABC, abstractmethod

import yaml

class Serializer(ABC):
    """ A class for serializing data to a specific format. """
    @abstractmethod
    def serialize(self, data, **kwargs) -> str:
        pass

class XMLSerializer(Serializer):
    """ A class for serializing data to XML format. """
    def _dict_to_xml(self, data, root_name="prompt"):
        """Convert a dictionary to XML"""
        root = ET.Element(root_name)

        def add_node(parent, data):
            """Recursively add nodes to the XML tree"""
            for key, value in data.items():
                node = ET.SubElement(parent, key)

                if key == "examples":
                    for example in value:
                        example_node = ET.SubElement(node, "example")
                        for k, v in example.items():
                            child = ET.SubElement(example_node, k)
                            child.text = str(v)
                    continue

                if key == "instructions":
                    for instruction in value:
                        instruction_node = ET.SubElement(node, "step")
                        instruction_node.text = instruction
                    continue

                if isinstance(value, dict):
                    add_node(node, value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            add_node(node, item)
                        else:
                            child = ET.SubElement(node, "item")
                            child.text = str(item)
                else:
                    node.text = str(value)

        add_node(root, data)
        xml_doc = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        return xml_doc

    def serialize(self, data, **kwargs):
        return self._dict_to_xml(data)

class JSONSerializer(Serializer):
    """ A class for serializing data to JSON format. """
    def serialize(self, data, **kwargs):
        indent = kwargs.get("indent", 4)
        return json.dumps(data, indent=indent)

class YAMLSerializer(Serializer):
    """ A class for serializing data to YAML format. """
    def serialize(self, data, **kwargs):
        return yaml.dump(data)

class SerializerFactory:
    """ A class for creating serializers. """
    @staticmethod
    def create_serializer(format: str) -> Serializer:
        if format == "xml":
            return XMLSerializer()
        elif format == "json":
            return JSONSerializer()
        elif format == "yaml":
            return YAMLSerializer()
        raise ValueError("Invalid format")
