# PromptML
A simple, yet elegant markup language for defining AI Prompts as Code (APaC). Built to be used by AI agents to automatically prompt for other AI systems

## Why PromptML ?
PromptML is built to provide a way for prompt engineers to define the AI prompts in a deterministic way. This is a Domain Specific Language (DSL) which defines characteristics of a prompt including context, instructions and it's metadata.

## How PromptML looks ?
The language is simple. You start blocks with `@` section annotation. A section ends with `@end` marker. Comments are started with `#` key.

```pml
@prompt
    @context
    # Add your context
    @end
    @objective
    # Add your objective
    @end
    @instructions
        @step
        # Add your step
        @end
    @end
    @examples
        @example
            @input
            # Add your input
            @end
            @output
            # Add your output
            @end
        @end
    @end
@end
```
