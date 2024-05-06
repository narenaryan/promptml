## Poem Maker: A sample application of Prompt Markup Language (PromptML) to make poems with high prompt precision

This is an example of how to use PromptML to generate final Generative AI prompt using Jinja2. The steps are performed in this manner:

1. Parse `poem.pml` using promptml parser to generate a prompt context
2. Pass context to Jinja2 environment with a template called `poem.jinja2`

This will print an output of below:

```txt
Context: You are a master poem writer who is creative and imaginative. You identify the beauty in the world and express it through your words and use vivid imagery and descriptive language to create a poem.

Examples:

        input: Requiem
        output: Under the wide and starry sky,
                    Dig the grave and let me lie.
                Glad did I live and gladly die,
                    And I laid me down with a will.

                This be the verse you grave for me:
                    Here he lies where he longed to be;
                Home is the sailor, home from sea,
                    And the hunter home from the hill.

        input: My Heart Leaps Up
        output: My heart leaps up when I behold
                    A rainbow in the sky:
                So was it when my life began;
                So is it now I am a man;
                So be it when I shall grow old,
                    Or let me die!
                The Child is father of the Man;
                And I could wish my days to be
                Bound each to each by natural piety.

Task Difficulty: Beginner
Reply in tone: Melancholic

Objective: Write a poem that describes a boy who locked in castle leaving behind his family and friends.
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

5. Play around with `poem.pml` by giving different examples, and re-run the program to see the change in output.
