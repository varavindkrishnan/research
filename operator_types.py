operators = ("EXTENDS", "MULS", "CCAST", "ASSIGN", "ADD", "SUB", "AND", "OR", "NEGATE", "ASSIGNDLY", "SHIFTL", "SHIFTR",
    "ASSIGNW", "EQ", "XOR", "NEQ", "LT", "LTE", "GT", "GTE", "COND", "NOT", "ASSIGNPRE", "ASSIGNPOST", "ARRAYSEL")

terminals = ("CONST", "VARREF")

assigns = ("ASSIGN", "ASSIGNDLY", "ASSIGNW", "ASSIGNPRE", "ASSIGNPOST")

assigns_blocking = ("ASSIGN", "ASSIGNDLY", "ASSIGNW", "ASSIGNPRE", "ASSIGNPOST")

single_operand = ("CCAST", "NEGATE", "NOT", "EXTENDS")

two_operand = ("MULS", "ASSIGN", "ADD", "SUB", "AND", "OR", "ASSIGNDLY", "SHIFTL", "SHIFTR",
    "ASSIGNW", "EQ", "XOR", "NEQ", "LT", "LTE", "GT", "GTE", "ASSIGNPRE", "ASSIGNPOST", "ARRAYSEL")

three_operand = ("COND")

cover = "COVERINC"

inversions = ("EQ", "NEQ", "LT", "GT", "LTE", "GTE")

invert = {}
invert["EQ"] = "NEQ"
invert["NEQ"] = "EQ"
invert["LT"] = "GTE"
invert["GTE"] = "LT"
invert["GT"] = "LTE"
invert["LTE"] = "GT"

transform ={}
transform["ASSIGN"] = "=="
transform["ASSIGNDLY"] = "=="
transform["ASSIGNPRE"] = "=="
transform["ASSIGNPOST"] = "=="
transform["EQ"] = "=="
transform["NEQ"] = "!="
transform["GT"] = ">"
transform["GTE"] = ">="
transform["LT"] = "<"
transform["LTE"] = "<="
transform["ADD"] = "+"
transform["SUB"] = "-"
transform["MUL"] = "*"
transform["SHIFTL"] = "<<"
transform["SHIFTR"] = ">>"
transform["NEGATE"] = "~"
transform["XOR"] = '^'
transform["AND"] = "&"
transform["OR"] = "||"
transform["NOT"] = "~"

comparators = ("ASSIGN", "ASSIGNPRE", "ASSIGNPOST", "ASSIGNDLY", "EQ", "NEQ", "GT", "GTE", "LT", "LTE")
