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

    def if_else_block(self, items):
        condition_var = items[0]
        block_if = items[1:]
        block_else = items[3:]

        if condition_var.children[1] == "true":
            return self.transform_block(block_if)
        else:
            return self.transform_block(block_else)

    def transform_block(self, block_items):
        transformed = {}
        for item in block_items:
            if hasattr(item, "data"):
                transformed.update(item.data)
            elif item:
                transformed.update({"condition_true": item})
        return transformed

    def var_block(self, items):
        """ Extract the variable block content."""
        var_map = {}

        for item in items:
            var_symbol = item.children[0].strip()
            var_value = item.children[1].strip()
            var_map[var_symbol] = var_value

        # Store the variables globally
        globals()['vars_'] = var_map  # Using global so it can be accessed in other methods

        return {"type": "vars", "data": var_map}

    def prompt(self, items):
        """ Extract the prompt content."""
        sections = {}
        title = ""
        for child in items:
            if hasattr(child, "data") and child.data == "section":
                data = child.children[0]
                if hasattr(child.children[0], "data"):
                    key = child.children[0].data
                    if key == "title":
                        title = child.children[0].children[0].strip()
                else:
                    sections.update(data)
            else:
                sections.update(child)

        return {"type": "prompt", "data": sections, "title": title}

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

    def text(self, items):
        """ Extract the text content."""
        return items[0]


class PromptParser:
    """A class for parsing prompt markup language code and extract information.
    """
    transformer = PromptMLTransformer()

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

    
