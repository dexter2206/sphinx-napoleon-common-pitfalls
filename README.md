# Common pitfalls occurring when using Sphinx with Napoleon

## What's this?

This repository demonstrates some common pitfalls which can be encountered when using Sphinx 
with Napoleon and autoapi extensions.

Inside you'll find:

- a dummy package `example` with some subpackage, and modules
  - the most important part of the package is `example.utils` module which contains three functions
    with incorrectly formatted docstrings:
   
    - `func_incorrect_1`
    - `func_incorrect_2`
    - `func_incorrect_3`
   
    All of these functions are identical, except some minor changes in the docstrings. 
  - The `example.utils` module also contains `func_correct` function, which is the same as the 
    incorrect ones, except its docstring is correct.  
- a docs folder with some basic Sphinx-based documentation. The only content of the docs is API 
  Reference of the `example` package (which is automatically generated).

Purposefully, this `conf.py` of docs sets `autoapi_keep_files = True`, so that the generated 
docs can be later inspected.

## How do I use it?

- Install needed dependencies (all sphinx related): `pip install -r requirements.txt`
- Go into `docs` directory: `cd docs`
- Make documentation in HTML format: `make html`
- Observe errors/warnings (there should be 5 of them total)
- Read below for their explanation.

## Before we explain errors....

Let's look at the correct docstring.

```python
def func_correct(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: :math:`|x + y| \\le |x| + |y|`

    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A new instance of A.
    """
    return A()
```

Of course, the docstring gets translated into ReStructuredText by Napoleon/autoapi, and you can 
preview it  in the `docs/source/api/example/utils/index.rst` (you first need to build the docs 
for the `api` directory to get created). This is what the generated ReST looks like:

```ReST
.. py:function:: func_correct(arg: B) -> example.subpackage.submodule.A

   Return fresh A, without using arg.

   Also, here's some math: :math:`|x + y| \le |x| + |y|`

   :param arg: some unused arg
               with multiline description

   :returns: A new instance of A.
```

Let's now look into each of the functions with incorrect docstring to see how their docstrings 
differ, and how those differences translate to the ReST.

## Explaining errors

### `func_incorrect_1`

#### Source code

```python
def func_incorrect_1(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: :math:`|x + y| \\le |x| + |y|`
    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A new instance of A.
    """
    return A()
```

#### Errors it gives rise to

The `func_incorrect_1` is responsible for the following warning.

```text
/home/dexter/Projects/sphinx-napoleon-common-pitfals/docs/source/api/example/utils/index.rst:59: ERROR: Unexpected indentation.
```

#### Generated ReST

```ReSt
.. py:function:: func_incorrect_1(arg: B) -> example.subpackage.submodule.A

   Return fresh A, without using arg.

   Also, here's some math: :math:`|x + y| \le |x| + |y|`
   :param arg: some unused arg
               with multiline description

   :returns: A new instance of A.
```

#### Explanation

We see that compared to the `func_correct`, we now don't have an empty line before the first
`:param:`.

Why is the message so cryptic? Parameter descriptions has to form a a 
[a field list](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#field-lists). 
Field lists are separated from the paragraphs with a blank line. Now this part:

```ReST
Also, here's some math: :math:`|x + y| \le |x| + |y|`
:param arg: some unused arg
```

does not contain a blank line and is therefore treated as a single paragraph. However, the next 
line is indented, which is unexpected, as the error says.

Further reading:

- [ReST Markup Specification](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html)


### `function_incorrect_2`

#### Source code

```python
def func_incorrect_2(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: :math:`|x + y| \\le |x| + |y|`

    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A: A new instance of A.
    """
    return A()
```

#### Warnings it gives rise to

```text
/home/dexter/Projects/sphinx-napoleon-common-pitfals/docs/source/api/example/utils/index.rst:64: WARNING: more than one target found for cross-reference 'A': example.subpackage.A, example.subpackage.submodule.A
```

#### Generated ReST

```ReST
.. py:function:: func_incorrect_2(arg: B) -> example.subpackage.submodule.A

   Return fresh A, without using arg.

   Also, here's some math: :math:`|x + y| \le |x| + |y|`

   :param arg: some unused arg
               with multiline description

   :returns: A new instance of A.
   :rtype: A
```

#### Explanation

As can be seen from the generated ReST, we now have an explicit `rtype` definition. However, it 
is not resolved to the `A` that is present in the `utils` module namespace, and there are 
multiple possible definitions of `A` it might refer to, because we reexport `A` in 
`subpackage`'s initialization file. 

Observe however, that the type in the type hint gets resolved correctly, and also renders 
correctly in the docs. The conclusion is: there is no point in specifying the return type 
explicitly in the docstring, it doesn't bring anything valuable to the table and might actually 
result in some errors.

Some more notes:

- the same effect occurs for the parameter types
- this effect does not occur if there is no ambiguity in referencing to the type. In our case, 
  if `A` wasn't available directly from `subpackage`, there would be no problem.
 
### `function_incorrect_2`

#### Source code

```python
def func_incorrect_3(arg: B) -> A:
    """Return fresh A, without using arg.

    Also, here's some math: |x + y| \\le |x| + |y|

    Args:
        arg: some unused arg
          with multiline description
    Returns:
        A new instance of A.
    """
    return A()
```

#### Warnings it gives rise to

```text
/home/dexter/Projects/sphinx-napoleon-common-pitfals/docs/source/api/example/utils/index.rst:81: ERROR: Undefined substitution referenced: "x + y".
/home/dexter/Projects/sphinx-napoleon-common-pitfals/docs/source/api/example/utils/index.rst:81: ERROR: Undefined substitution referenced: "x".
/home/dexter/Projects/sphinx-napoleon-common-pitfals/docs/source/api/example/utils/index.rst:81: ERROR: Undefined substitution referenced: "y".
```

#### Generated ReST

```ReST
.. py:function:: func_incorrect_3(arg: B) -> example.subpackage.submodule.A

   Return fresh A, without using arg.

   Also, here's some math: |x + y| \le |x| + |y|

   :param arg: some unused arg
               with multiline description

   :returns: A new instance of A.
```

#### Explanation

The `|something|` syntax is used to define 
[substitutions](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext. html#substitution-definitions),
unless it is enclosed in backticks. Hence, the parser actually wants to replace `|x|` with some 
text, and errors out because the substitution is not defined.

Note that it would be even worse, if for whatever reason you actually had a substitution definition 
for `x`, as the equation would probably get massacred but wouldn't raise any build-time errors.  
