from src.promptml.parser import PromptParser

promptml_code = '''
@vars
    conditionVar = "true"
@end

@prompt
    @title
        "Conditional Prompt Example"
    @end
    @context 
        This is a sampl context.
    @end
    @objective 
        Achieve this objective based on the condition.
    @end

    @if conditionVar == "ABC" {
        @objective 
            Achieve this objective based on the condition.
        @end
    }
    @else {
        "This is a sample context."
    }
@end
'''
parser = PromptParser(promptml_code)
prompt = parser.parse()

print(prompt)