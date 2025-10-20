# -------- MINI COMPILER IN PYTHON --------
# This code performs lexical, syntax, semantic, and code generation phases.

# ----- Lexical Analysis -----
def lexical_analyzer(code):
    tokens = []
    keywords = {"if", "else", "while", "for", "int", "float", "print"}
    operators = {"+", "-", "*", "/", "=", "==", ">", "<"}
    delimiters = {"(", ")", "{", "}", ";"}
    
    words = code.replace(";", " ;").replace("(", " ( ").replace(")", " ) ") \
                .replace("{", " { ").replace("}", " } ").split()
    
    for word in words:
        if word in keywords:
            tokens.append(("KEYWORD", word))
        elif word in operators:
            tokens.append(("OPERATOR", word))
        elif word in delimiters:
            tokens.append(("DELIMITER", word))
        elif word.isdigit():
            tokens.append(("NUMBER", word))
        elif word.isidentifier():
            tokens.append(("IDENTIFIER", word))
        else:
            raise ValueError(f"Lexical Error: Unknown symbol '{word}'")
    return tokens


# ----- Syntax Analysis -----
def syntax_analyzer(tokens):
    identifiers = set()
    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]
        if token_value == "int" or token_value == "float":
            # Expect variable declaration
            if i + 1 < len(tokens) and tokens[i + 1][0] == "IDENTIFIER":
                identifiers.add(tokens[i + 1][1])
                i += 2
            else:
                raise SyntaxError("Syntax Error: Invalid variable declaration")
        elif token_value == "print":
            if i + 2 < len(tokens) and tokens[i + 1][1] == "(" and tokens[i + 2][0] == "IDENTIFIER":
                i += 4  # skip print, (, var, )
            else:
                raise SyntaxError("Syntax Error: Invalid print statement")
        elif token_value == "if":
            # Simplified if structure
            if i + 4 < len(tokens) and tokens[i + 1][1] == "(" and tokens[i + 3][1] == ")" and tokens[i + 4][1] == "{":
                i += 5
            else:
                raise SyntaxError("Syntax Error: Invalid if condition")
        else:
            i += 1
    return identifiers


# ----- Semantic Analysis -----
def semantic_analyzer(tokens, identifiers):
    for i in range(len(tokens) - 1):
        token_type, token_value = tokens[i]
        if token_type == "IDENTIFIER" and token_value not in identifiers:
            raise NameError(f"Semantic Error: Variable '{token_value}' not declared")
    return True


# ----- Intermediate Code Generation -----
def generate_intermediate_code(tokens):
    intermediate_code = []
    temp_count = 1
    for i in range(len(tokens) - 2):
        if tokens[i][0] == "IDENTIFIER" and tokens[i + 1][1] == "=":
            exp = f"{tokens[i][1]} = {tokens[i + 2][1]}"
            intermediate_code.append(exp)
            temp_count += 1
    return intermediate_code


# ----- Machine Code Generation (Simplified) -----
def generate_machine_code(intermediate_code):
    machine_code = []
    for line in intermediate_code:
        parts = line.split("=")
        var = parts[0].strip()
        val = parts[1].strip()
        machine_code.append(f"LOAD {val}")
        machine_code.append(f"STORE {var}")
    return machine_code


# ----- MAIN FUNCTION -----
def main():
    print("------ MINI COMPILER ------")
    print("Example input:")
    print("int a ; a = 5 ; print ( a )")
    print("---------------------------")
    
    code = input("Enter your code: ")

    try:
        # 1. Lexical Analysis
        tokens = lexical_analyzer(code)
        print("\nTokens:")
        for t in tokens:
            print(t)

        # 2. Syntax Analysis
        identifiers = syntax_analyzer(tokens)
        print("\nIdentifiers:", identifiers)

        # 3. Semantic Analysis
        if semantic_analyzer(tokens, identifiers):
            print("\nSemantic Analysis Passed")

        # 4. Intermediate Code
        intermediate = generate_intermediate_code(tokens)
        print("\nIntermediate Code:")
        for line in intermediate:
            print(line)

        # 5. Machine Code Generation
        machine = generate_machine_code(intermediate)
        print("\nMachine Code:")
        for line in machine:
            print(line)

    except Exception as e:
        print("\nCompilation Error:", e)


# Run the compiler
main()
