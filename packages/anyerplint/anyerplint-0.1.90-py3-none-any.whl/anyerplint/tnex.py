"""tnex - Trivial Nested EXpressions.

Easier to read/write than s-expr's I guess

"""
import re
from typing import Union


def tokenize(s: str) -> list[str]:
    # negative lookbehind for \ escaping, split to parts separated by ; ( ) "
    tokens = re.split(r"((?<!\\)[\(\)\";])", s)
    return list(filter(None, tokens))


def _parse_string(toks: list[str]) -> tuple[str, int]:
    assert toks[0] == '"'
    # eat up tokens to produce just one str
    end_token_index = toks.index('"', 1)
    stringparts = toks[0 : end_token_index + 1]
    value = "".join(stringparts)
    return value, len(stringparts)


def _parse_accessor(toks: list[str]) -> tuple[str, int]:
    if len(toks) > 1 and toks[1] == '"':
        s, moved = _parse_string(toks[1:])
        return toks[0] + s, moved + 1

    return toks[0], 1


RecursiveList = list[Union[str, "RecursiveList"]]


def emit_nested_sequence(parts: list[str]) -> tuple[RecursiveList, int]:
    res: RecursiveList = []
    i = 0
    while i < len(parts):
        it = parts[i]
        if it == '"':
            s, moved = _parse_string(parts[i:])
            res.append(s)
            i += moved
        elif it == ";":
            i += 1
        elif it == ")":
            i += 1
            break
        elif it == "(":
            nested, moved = emit_nested_sequence(parts[i + 1 :])
            nested.insert(0, parts[i - 1])
            res = res[0:-1]
            res.append(nested)
            i += moved
        elif it.startswith(","):
            # actually call previous output with "nesting" output
            previous = res.pop()
            s, moved = _parse_accessor(parts[i:])
            res.append([s, previous])
            i += moved

        # special foo,"hello" accessor that accesses property of foo.
        # lexer breaks it because of " char, so reassemble it here
        elif it.endswith(","):
            s, moved = _parse_accessor(parts[i:])
            res.append(s)
            i += moved
        else:
            res.append(it)
            i += 1

    return (res, i + 1)


def removequote(s: str) -> str:
    return s.removeprefix('"').removesuffix('"')


def translate_str(s: str) -> str:
    parsed = parse(s)
    return translate(parsed[0])


SIMPLE_FUNCS = {"F,ROWCOUNT": "rowcount", "F,CURSORINDEX": "cursorindex"}


def translate(tree: str | RecursiveList) -> str:
    """Convert to pretty mostly-infix notation."""
    # only lists cause translation
    if not isinstance(tree, list):
        return str(tree)

    match tree:
        case ["F,EVAL", obj, operation, comp, iftrue, iffalse]:
            return f"({translate(obj)} {removequote(translate(operation))} {translate(comp)} ? {translate(iftrue)} : {translate(iffalse)})"
        case ["F,EXISTS", obj, key]:
            return f"({key} in {translate(obj)})"
        case ["F,EXISTS", obj]:
            return f"(exists {translate(obj)})"

        case ["F,REPLACE", src, frome, toe]:
            return f"{translate(src)}.replace({translate(frome)} -> {translate(toe)})"
        case ["F,LOWER", exp]:
            return f"{translate(exp)}.lower()"
        case ["F,UPPER", exp]:
            return f"{translate(exp)}.upper()"
        case ["F,TRIM", exp]:
            return f"{translate(exp)}.trim()"
        case ["F,NVL", exp, default]:
            return "(" + translate(exp) + " ?? " + translate(default) + ")"

        case ["F,TONUMBER", exp, '"."']:
            return f"num({translate(exp)})"
        case ["F,TONUMBER", exp, sep]:
            return f"num({translate(exp)} - {translate(sep)})"
        case ["F,COMBINE", *parts]:
            translated = [translate(part) for part in parts]
            return "(" + " & ".join(translated) + ")"
        case ["F,GETDATA", ds, key]:
            return f"{translate(ds)}[{translate(key)}]"
        case ["F,SETDATA", ds, key, value]:
            return f"{translate(ds)}[{translate(key)}] := {translate(value)}"
        case ["F,IF", src, op, tgt]:
            return f"if {translate(src)} {removequote(translate(op))} {translate(tgt)}"
        case ["F,LEN", o]:
            return f"len({translate(o)})"
        case ["F,CALC", *parts]:
            return "(" + " ".join(translate(part) for part in parts) + ")"
        case ["F,NOT", exp]:
            return "not " + translate(exp)
        case ["F,AND", *conds]:
            translated = [translate(part) for part in conds]
            return "(" + " && ".join(translated) + ")"
        case ["F,OR", *conds]:
            translated = [translate(part) for part in conds]
            return "(" + " || ".join(translated) + ")"
        case [str(func), param] if func.startswith(","):
            return f"{translate(param)}.pipe({func})"
        case [str(func), *rest]:
            newname = SIMPLE_FUNCS.get(func)
            if not newname:
                print("UNK_FUN", func)
                newname = func.removeprefix("F,")
            return f"{newname}(" + ";".join(translate(r) for r in rest) + ")"
        case [*parts]:
            print("UNKNOWN PATTERN", parts)
            return str(parts)

    s = f"Unmatched pattern {tree}"
    raise Exception(s)


def parse(s: str, expand_entities: bool = True) -> RecursiveList:
    if expand_entities:
        s = expand_xml_entities(s)
    tokens = tokenize(s)
    parsed, _ = emit_nested_sequence(tokens)
    return parsed


def expand_xml_entities(xml_string: str) -> str:
    entity_pattern = re.compile(r"&([^;]+);")

    def replace_entity(match: re.Match[str]) -> str:
        entity = match.group(1)
        if entity == "lt":
            return "<"
        elif entity == "gt":
            return ">"
        elif entity == "amp":
            return "&"
        elif entity == "quot":
            return '"'
        else:
            return match.group(0)

    return entity_pattern.sub(replace_entity, xml_string)
