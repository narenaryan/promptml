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
import re

class PromptParser:
    """
    A class for parsing prompt markup language code and extract information.
    """
    def __init__(self, dsl_code):
        self.dsl_code = dsl_code
        self.prompt = {}

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
        prompt_pattern = re.compile(r'@prompt\s*(.*?)(@end(?!.*@end))', re.DOTALL | re.MULTILINE)
        match = prompt_pattern.search(self.dsl_code)

        # (@end(?!.*@end)): This is a positive lookahead assertion that matches the string @end only if it is not followed by another occurrence of @end.
        # The (?!.*@end) part is a negative lookahead assertion that asserts that there should not be another @end after the current one.
        if match:
            prompt_content = match.group(1)
            self.prompt = self.parse_sections(prompt_content)

    def parse_sections(self, content):
        """
        Parse the sections of the prompt content and extract the section content.

        Args:
            content (str): The content of the prompt section.

        Returns:
            dict: A dictionary containing the parsed sections of the prompt.
        """
        sections = {}
        section_patterns = {
            'context': r'@context\s*(.*?)\s*@end',
            'objective': r'@objective\s*(.*?)\s*@end',
            'instructions': self.parse_instructions,
            'examples': self.parse_examples,
            'constraints': self.parse_constraints,
            'metadata': self.parse_metadata,
        }

        for section, pattern in section_patterns.items():
            if callable(pattern):
                sections[section] = pattern(content)
            else:
                section_pattern = re.compile(pattern, re.DOTALL)
                match = section_pattern.search(content)
                if match:
                    sections[section] = match.group(1).strip()

        return sections

    def parse_instructions(self, content):
        """ Parse the instructions section of the prompt content and extract the instructions."""
        instructions_pattern = re.compile(
            r'@instructions\s*(.*?)\s*(@end(?!.*@end))',
            re.DOTALL | re.MULTILINE
        )

        match = instructions_pattern.search(content)
        if match:
            instructions_content = match.group(1)
            steps = []
            step_pattern = re.compile(r'@step\s*(.*?)\s*@end', re.DOTALL | re.MULTILINE)
            matches = step_pattern.finditer(instructions_content)
            for step_match in matches:
                step = step_match.group(1).strip()
                steps.append(step)
            return steps
        return []

    def parse_examples(self, content):
        """
        Parse the examples section of the prompt content and extract the examples.

        Args:
            content (str): The content of the examples section.

        Returns:
            list: A list of dictionaries containing the parsed examples.
        """
        examples = []
        example_pattern = re.compile(r'@example\s*(.*?)\s*(@end(?!.*@end))', re.DOTALL | re.MULTILINE)
        matches = example_pattern.finditer(content)
        for match in matches:
            example_content = match.group(1)
            input_pattern = re.compile(r'@input\s*(.*?)\s*@end', re.DOTALL | re.MULTILINE)
            output_pattern = re.compile(r'@output\s*(.*?)\s*@end', re.DOTALL | re.MULTILINE)
            input_match = input_pattern.search(example_content)
            output_match = output_pattern.search(example_content)
            if input_match and output_match:
                example = {
                    'input': input_match.group(1).strip(),
                    'output': output_match.group(1).strip(),
                }
                examples.append(example)
        return examples

    def parse_constraints(self, content):
        """
        Parse the constraints section of the prompt content and extract the constraints.

        Args:
            content (str): The content of the constraints section.

        Returns:
            dict: A dictionary containing the parsed constraints.
        """
        constraints = {}
        length_pattern = re.compile(r'@length\s*min:\s*(\d+)\s*max:\s*(\d+)\s*@end', re.DOTALL)
        tone_pattern = re.compile(r'@tone\s*(.*?)\s*@end', re.DOTALL)
        length_match = length_pattern.search(content)
        tone_match = tone_pattern.search(content)
        if length_match:
            constraints['length'] = {
                'min': int(length_match.group(1)),
                'max': int(length_match.group(2)),
            }
        if tone_match:
            constraints['tone'] = tone_match.group(1).strip()
        return constraints

    def parse_metadata(self, content):
        """
        Parse the metadata section of the prompt content and extract the metadata.

        Args:
            content (str): The content of the metadata section.

        Returns:
            dict: A dictionary containing the parsed metadata.
        """
        metadata = {}
        domain_pattern = re.compile(r'@domain\s*(.*?)\s*@end', re.DOTALL | re.MULTILINE)
        difficulty_pattern = re.compile(r'@difficulty\s*(.*?)\s*@end', re.DOTALL | re.MULTILINE)
        domain_match = domain_pattern.search(content)
        difficulty_match = difficulty_pattern.search(content)
        if domain_match:
            metadata['domain'] = domain_match.group(1).strip()
        if difficulty_match:
            metadata['difficulty'] = difficulty_match.group(1).strip()
        return metadata

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
