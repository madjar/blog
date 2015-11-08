Title: Garçon, there's a catamorphism in my Python
Date: 2015-11-08 19:00

I've got a little project where I want to build a document from a
template, and some data that are stored in a JSON (or YAML) file. This
is pretty straighforward, but I've got an additional requirement: I
want to make documents in multiple languages, and I want to specify
the various translations of a string in the JSON file itself, like so:

```
{ "en": "This is a sentence in english",
  "fr": "Ceci est une phrase en français"}
```

This seems quite easier, so I started coding straight away, and I
arrived to this result:

```python
def localize(lang, data):
    if isinstance(data, list):  # If this is a list, recurse into the list
        return [localize(lang, x) for x in data]
    if isinstance(data, dict):  # If this is a dict, do what we must
        if lang in data:
            return data[lang]
        else:                   # Otherwise, do nothing
            return data
    return data
```

Can you see the problem with this? I failed to recurse in the case of
the dict. Of course, this is easily fixable: just replace the first
`return data` with `return {k: localize(lang, v) for (k, v) in
data.items()}`. But this is a common mistake, and it stems from the
fact that we mixed our traversal code, and the actual transformation
we wanted to make. Would it be possible to write our code in a way
where no mistakes can be made?

## Complicated words to the rescue!

I've been spending quite some time with haskell lately, and I recently
learned about recursion schemes: a generic way to handle recursive
data structure. In python, we have a generic way to handle iterative
data structure: iterators. They let you handle a list, a tree, or
anything with elements the same way: with a `for` loop. Recursion
schemes are the same idea, but for recursive data.

A recursive data type is a type where one value might contain another
value of the same type. For example, a JSON value is recursive,
because it can contain another JSON value (in a list or as the
attribute of an object).

In haskell, if a type can contain something (whatever it is), you call
it a functor, and you give it a function called `fmap`, which execute
a given function on all contained items. Let's implement it for our
JSON values!

```python
def fmap(f, data):
    if isinstance(data, list):
        return [f(x) for x in data]
    if isinstance(data, dict):
        return {k: f(v) for (k, v) in data.items()}
    return data
```

Now that JSON values have a `fmap` function, we can use it to
implement our generic recursive traversal. We want to traverse our
data to build a new value along the way: this particular kind of
recursion is called a catamorphism. Fear not, it's a rather simple
implementation for a complicated word.

```python
def cata(f, data):
    # First, we recurse inside all the values in data
    cata_on_f = lambda x: cata(f, x)
    recursed = fmap(cata_on_f, data)

    # Then, we apply f to the result
    return f(recursed)
```

When you pass a function `f` to cata, it is called at each level of
the recursion, and is passed a copied version of the data where each
contained value `x` is replaced with `cata(f, x)`. It means that `f`
doesn't have to worry about the recursion, when `f` is called, the
recursion has already been done.

For example, say we want the sum of all the integers in a tree (which
we model as a nested list of lists). We need to write a function that
only sums one level, since the recursion is done by `cata`. The
function receives either a value that is not a list, and just returns
it, or a list were values have already been summed.

```python
def sum_one_level(data):
    if isinstance(data, list):
        return sum(data)
    return data
```

Now, we can call `cata(sum_one_level, [[[1, 2], [3]], [4]])`, and the
result is `10`.

## Back to the localization

So, we now have a `cata` function that does the recursion for us, and
does it well. To recreate our localization function, we need to define
a function that only localizes one level. It takes a JSON value, and
localize it (but without any recursion, since the recursion is handled
by `cata`).

```python
def localize_one_level(lang, data):
    if isinstance(data, dict) and lang in data:
        return data[lang]
    return data
```

We can then define our new `localize` using this function.

```python
def localize2(lang, data):
    localize_one_level_on_lang = lambda x: localize_one_level(lang, x)
    return cata(localize_one_level_on_lang, data)
```

Here we go! I've defined a function to recurse into JSON data in a
generic way, and I'll never have to write a recursive function for
JSON data ever again. I'll just need to define functions that work on
one level, and that's it. And I can do that for any other recursive
data type: I'll just need to create another `fmap` implementation for
them.
