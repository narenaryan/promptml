"""
This module provides a PromptParser class for parsing DSL code and extracting prompt information.

The PromptParser class can parse DSL code and extract sections such as context,
objective, instructions, examples, constraints, and metadata from the code.
It uses regular expressions to search for specific
patterns in the DSL code and extract the corresponding content.

Example usage:
    dsl_code = '''
        ...
    '''

    parser = PromptParser(dsl_code)
    prompt = parser.parse()
"""

import os
from lark import Lark, Transformer
from .serializer import SerializerFactory

class PromptMLTransformer(Transformer):
    """
    A class for transforming the parsed PromptML tree into a Python dictionary.
    """

    def start(self, items):
        """ Extract the start section content."""
        prompt = {}
        vars_ = {}
        for item in items:
            if item["type"] == "vars":
                vars_ = item["data"]
            elif item["type"] == "prompt":
                prompt = item["data"]

        # context seems to be a keyword in Python, so we'll use context_ instead
        context_ = prompt["context"]
        objective = prompt["objective"]

        # Replace variables in context and objective with values
        for k,v in vars_.items():
            context_ = context_.replace(r'$' + k, v.replace("'", '').replace('"', ''))
            objective = objective.replace(r'$' + k, v.replace("'", '').replace('"', ''))

        prompt["context"] = context_
        prompt["objective"] = objective

        return prompt

    def block(self, items):
        """ Extract the block content."""
        return items[0]

    def category(self, items):
        """ Extract the category content."""
        return {"category": items[0].strip()}

    def prompt(self, items):
        """ Extract the prompt content."""
        sections = {}
        for child in items:
            if hasattr(child, "data") and child.data == "section":
                data = child.children[0]
                sections.update(data)
            else:
                sections.update(child)

        return {"type": "prompt", "data": sections}

    def context(self, items):
        """ Extract the context section content."""
        return {"context": items[0].strip()}

    def objective(self, items):
        """ Extract the objective section content."""
        return {"objective": items[0].strip()}

    def instructions(self, items):
        """ Extract the instructions section content."""
        steps = [item.value.strip() for item in items]
        return {"instructions": steps}

    def instruction(self, items):
        """ Extract the instruction content."""
        return items[0]

    def examples(self, items):
        """ Extract the examples section content."""
        examples = list(items)
        return {"examples": examples}

    def example(self, items):
        """ Extract the example content."""
        input_text = items[0].children[0].strip()
        output_text = items[1].children[0].strip()
        return {"input": input_text, "output": output_text}

    def constraints(self, items):
        """ Extract the constraints section content."""
        constraints = {}
        for item in items:
            constraints.update(item.children[0])

        return {"constraints": constraints}

    def length(self, items):
        """ Extract the length constraint content."""
        min_length = int(items[0])
        max_length = int(items[1])
        return {"length": {"min": min_length, "max": max_length}}

    def tone(self, items):
        """ Extract the tone constraint content."""
        return {"tone": items[0].strip()}

    def difficulty(self, items):
        """ Extract the difficulty constraint content."""
        return {"difficulty": items[0].strip()}

    def var_block(self, items):
        """ Extract the variable block content."""
        var_map = {}

        for item in items:
            var_symbol = item.children[0].strip()
            var_value = item.children[1].strip()
            var_map[var_symbol] = var_value

        return {"type": "vars", "data": var_map}

    def metadata(self, items):
        """
        Extracts the metadata section content.

        Args:
            items (list): A list of items representing the metadata section content.

        Returns:
            dict: A dictionary containing the extracted metadata section content.
        """
        metadata = {}

        for item in items:
            key = item.children[0].strip()
            if key:
                prop_type = item.children[1].type
                value = item.children[1].strip()

                if prop_type == "NUMBER":
                    try:
                        value = int(value)
                    except ValueError:
                        value = float(value)
                elif prop_type == "STRING":
                    value = value.strip("\"").strip("\'")

                metadata[key] = value

        return {"metadata": metadata}

    def text(self, items):
        """ Extract the text content."""
        return items[0]


class PromptParser:
    """A class for parsing prompt markup language code and extract information.
    """
    transformer = PromptMLTransformer()

    # Define the grammar for the prompt markup language.
    def __init__(self, code: str):
        promptml_grammar = None
        # get current directory
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with open(f'{dir_path}/grammar.lark', 'r', encoding="utf-8") as f:
            promptml_grammar = f.read()

        self.code = code
        self.prompt = {}
        self.parser = Lark(promptml_grammar)
        self.xml_serializer = SerializerFactory.create_serializer("xml")
        self.json_serializer = SerializerFactory.create_serializer("json")
        self.yaml_serializer = SerializerFactory.create_serializer("yaml")

    def parse(self):
        """
        Parse the DSL code and extract the prompt information.

        Returns:
            dict: A dictionary containing the prompt information.
        """
        self._parse_prompt()
        return self.prompt

    def _parse_prompt(self):
        """
        Parse the prompt section of the DSL code and extract the prompt content.
        """
        tree = self.parser.parse(self.code)
        self.prompt = PromptParser.transformer.transform(tree)
        return self.prompt

    def to_json(self, indent=None):
        """ Serialize the prompt data to JSON.
        """
        return self.json_serializer.serialize(self.prompt, indent=indent)

    def to_yaml(self):
        """ Serialize the prompt data to YAML.
        """
        return self.yaml_serializer.serialize(self.prompt)

    def to_xml(self):
        """ Serialize the prompt data to XML.
        """
        return self.xml_serializer.serialize(self.prompt)

class PromptParserFromFile(PromptParser):
    """
    A subclass of PromptParser that reads DSL code from a file.
    """
    def __init__(self, file_path: str):
        """
        Initializes the PromptParserFromFile object by reading the DSL code from the specified file path
        and passing it to the parent class constructor.

        Args:
            file_path (str): The path to the DSL code file.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            dsl_code = f.read()
        super().__init__(dsl_code)
