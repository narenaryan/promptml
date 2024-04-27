"""
This module provides a PromptParser class for parsing DSL code and extracting prompt information.

The PromptParser class can parse DSL code and extract sections such as context, objective, instructions,
examples, constraints, and metadata from the code. It uses regular expressions to search for specific
patterns in the DSL code and extract the corresponding content.

Example usage:
    dsl_code = '''
        @prompt
        @context
        This is the context section.
        @end

        @objective
        This is the objective section.
        @end

        @instructions
        These are the instructions.
        @end

        @examples
        @example
        @input
        Input example 1
        @end
        @output
        Output example 1
        @end
        @end
        @end

        @constraints
        @length min: 1 max: 10
        @end

        @metadata
        @domain
        Domain example
        @end
        @difficulty
        Difficulty example
        @end
        @end
    '''

    parser = PromptParser(dsl_code)
    prompt = parser.parse()

    print(prompt)
    # Output: {
    #     'context': 'This is the context section.',
    #     'objective': 'This is the objective section.',
    #     'instructions': 'These are the instructions.',
    #     'examples': [
    #         {'input': 'Input example 1', 'output': 'Output example 1'}
    #     ],
    #     'constraints': {'length': {'min': 1, 'max': 10}},
    #     'metadata': {'domain': 'Domain example', 'difficulty': 'Difficulty example'}
    # }
"""

import json
import os


from lark import Lark, Transformer

class PromptMLTransformer(Transformer):
    """
    A class for transforming the parsed PromptML code into a structured format.
    """
    def prompt(self, items):
        sections = {}
        tree = items[0]
        for child in tree.children:
            if child.data == "section":
                data = child.children[0]
                sections.update(data)

        return sections

    def context(self, items):
        return {"context": items[0].strip()}

    def objective(self, items):
        return {"objective": items[0].strip()}

    def instructions(self, items):
        steps = [item.value.strip() for item in items]
        return {"instructions": steps}

    def instruction(self, items):
        return items[0]

    def examples(self, items):
        examples = [example for example in items]
        return {"examples": examples}

    def example(self, items):
        input_text = items[0].children[0].strip()
        output_text = items[1].children[0].strip()
        return {"input": input_text, "output": output_text}

    def constraints(self, items):
        constraints = {}
        for item in items:
            constraints.update(item.children[0])

        return {"constraints": constraints}

    def length(self, items):
        min_length = int(items[0])
        max_length = int(items[1])
        return {"length": {"min": min_length, "max": max_length}}

    def tone(self, items):
        return {"tone": items[0].strip()}

    def metadata(self, items):
        metadata = {}
        for item in items:
            child = item.children[0]

            for k,v in child.items():
                metadata[k] = v.strip()

        return {"metadata": metadata}

    def domain(self, items):
        return {"domain": items[0]}

    def difficulty(self, items):
        return {"difficulty": items[0]}

    def text(self, items):
        return items[0]

class PromptParser:
    transformer = PromptMLTransformer()
    """
    A class for parsing prompt markup language code and extract information.
    """
    # Define the grammar for the prompt markup language.
    def __init__(self, dsl_code):
        promptml_grammar = None
        # get current directory
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with open(f'{dir_path}/grammar.lark', 'r', encoding="utf-8") as f:
            promptml_grammar = f.read()

        self.dsl_code = dsl_code
        self.prompt = {}
        self.parser = Lark(promptml_grammar, start="prompt")

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
        tree = self.parser.parse(self.dsl_code)
        self.prompt = PromptParser.transformer.transform(tree)
        return self.prompt

    def serialize_json(self, indent=None):
        """ Serialize the prompt data to JSON.
        """
        return json.dumps(self.prompt, indent=indent)

    def deserialize_json(self, serialized_data):
        """ Deserialize the prompt data from JSON.
        """
        self.prompt = json.loads(serialized_data)

class PromptParserFromFile(PromptParser):
    """
    A subclass of PromptParser that reads DSL code from a file.
    """
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            dsl_code = f.read()
        super().__init__(dsl_code)
