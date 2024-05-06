## Calculator App: A sample application of Prompt Markup Language (PromptML)

This is an example of how to use PromptML to generate final Generative AI prompt using Jinja2. The steps are performed in this manner:

1. Parse `calculator.pml` using promptml parser to generate a prompt context
2. Pass context to Jinja2 environment with a template called `calculator.jinja2`

This will print an output of below:

```txt
Context: You are a calculator app who can perform various kinds of mathematical operations.

Domain: Education

Task Difficulty: Beginner

Reply in tone: Friendly

Follow the below instructions step-by-step for objective:
1. Think about how you can add two numbers together.
2. Return only the answer.

Objective: What is the sum of 5 and 6?
```

This is the final prompt to be used for Generative AI systems.

## Running instructions

1. Create a virtual environment in this directory:

   ```bash
    python3 -m venv .venv
   ```

2. Activate virtual environment

   ```bash
   source .venv/bin/activate
   ```

3. Install Jinja2 and promptml

   ```bash
   pip install -r requirements.txt
   ```

   Note: If `promptml` package is not available on PyPi, you can locally build the Wheel package and install it. See [BUILD.md](../../BUILD.md) file for instructions.

4. Run the program

   ```bash
   python main.py
   ```

5. Play around with `calculator.pml` and re-run the program to see the change in output.
