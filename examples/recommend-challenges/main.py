from promptml.parser import PromptParserFromFile
from jinja2 import Environment, FileSystemLoader


def main():
    template_loader = FileSystemLoader(searchpath="./")
    template_env = Environment(loader=template_loader)
    template_file = "recommend.jinja2"
    template = template_env.get_template(template_file)

    # Parse PromptML code and generate context
    prompt_parser = PromptParserFromFile('recommend.pml')
    prompt = prompt_parser.parse()

    # Render the template with the prompt context
    template_output = template.render(prompt=prompt)
    print(template_output)

if __name__ == '__main__':
    main()
