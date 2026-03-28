import re


def repl_call(m):
    preq = m.group(1)
    qbody = m.group(2)
    qbody = re.sub(r'"', '\\\"', qbody)
    return preq + '"' + qbody + '"'


def escape_unescaped_quotes(json_string):
    return re.sub(r'([:\[,{]\s*)"(.*?)"(?=\s*[:,\]}])', repl_call, json_string)
