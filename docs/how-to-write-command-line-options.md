# clcoevt: How to write command-line options

## Option format
Option format has short option, and long option.

**Short option format** begins with a single hyphen (-) followed by a single
character (uppercase or lowercase).

    -a -B -c

The options without value is chainable.
The example above can be written as follows:

    -aBc

However, only the last option can have a value.
The following example is equivalent to `-a -b -c -d=efgh`; the `d` has `efgh`.

    -aBcd=efgh

**Long option format** begin with two hyphens (--), followed by two or more
characters (lowercase English letters and hyphens).

    --verbose --list-all

## Value specification
Value specification format has connected format, and separated format.

In the **connected format**, the name and value are connected by an equals
sign (=).

    --host=example.com

In the **separated format**, the name and value are separated.

    --host example.com

If you want to specify an empty string, use the escape syntax for your shell.
For example, in `bash`:

    --prefix ""

## Value type
Valid value types are string, integer, and boolean.

**String type** needs value.

**Integer type** needs value.  Specify the value in decimal.

**Boolean type**’s value is optional.
The option without value is `True`.

The following is `True`:
- `true`
- `t`
- `on`
- `yes`
- `1`

The following is `False`:
- `false`
- `f`
- `off`
- `no`
- `0`
- Empty string.

Any other string of one or more characters is `True`.
The value is case insensitive.
