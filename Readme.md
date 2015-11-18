#Toy Template Engine

##Introduction

This is a toy project for learning how to write a template engine. I made it just for fun. It will be updated continually. The basic part of this project is mainly consulted [This](http://alexmic.net/building-a-template-engine/) blog post and [Jinja2](http://jinja.pocoo.org/) template engine.


##Grammar Design

The template grammar contains two type of tags.

+ `{{ ... }}` for *Expression*
+ `{% ... %}` for *Statement*

###Expression

**Literals:** all literals of pythonn is valid. For example:

+ string: `"Hello world"`
+ number: `43`, `3.14159`
+ list: `[1, 2, 3]`
+ dict: `{'key': value}`
+ tuple: `(12, 33)`
+ boolean: `True`, `False`

**Math** The following operators is supported:
`+`, `-`, `*`, `/`, `**`, `%`, `//`

**Comparisons** The following operators is supported:
`==`, `>=`, `<=`, `!=`, `>`, `<`

**Logic** The following operators is supported:
`and`, `or`, `not`, `()`

**Other** The following operators is supported:
`in`, `is`,

`[]` for getting an attribute of an object,

`~` for string concatenates,

`()` for calling a callable object.

###Statement

**If statement:** The if statement is similar to python. `elif` and `else` are optional. For example:

```
{% if condition1 %}
    branch 1
{% elif condition2 %}
    branch 2
{% else %}
    branch else
{% endif %}
```

**For statement:** The for statement is just like below:

```
{% for item in items%}
    The item in items is {{item}}.
{% end for%}
```