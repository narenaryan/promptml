## How to build `promptml` package locally ?

We are in process of publishing this package to PyPi, until then you can build a Wheel package locally with below commands:

From project root, in a command-line shell, run:

```bash
pip install -r requirements_dev.txt

hatch build
```

Once hatch command is executed, you will see a `dist/` directory with a `.whl` file. With your activated Python environment, run the following command to install the package:

```bash
 pip install dist/promptml-x.y.z-py3-none-any.whl
```
were x.y.z is the version specified in `src/promptml/__about__.py` file.

This will install promptml package to your Python environment. To uninstall, run command:

```bash
pip uninstall promptml
```
