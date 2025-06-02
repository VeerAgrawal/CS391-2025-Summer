#Assignment 1, Lambda1.py Final Sumbission file
#Veer Agrawal, veer1@bu.edu

# TERM DATATYPE AND HELPERS
#CODE from Lecture + my code from quiz1

class term:
    ctag = ""
    def __str__(self): return self._to_str()

class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMvar"
    def _to_str(self): return f"TMvar({self.arg1})"

class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMlam"
    def _to_str(self): return f"TMlam({self.arg1};{self.arg2})"

class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMapp"
    def _to_str(self): return f"TMapp({self.arg1};{self.arg2})"

class term_int(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMint"
    def _to_str(self): return f"TMint({self.arg1})"

class term_btf(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMbtf"
    def _to_str(self): return f"TMbtf({self.arg1})"

class term_if0(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMif0"
    def _to_str(self): return f"TMif0({self.arg1};{self.arg2};{self.arg3})"

class term_opr(term):
    def __init__(self, opr, args):
        self.arg1 = opr
        self.arg2 = args  # list of terms
        self.ctag = "TMopr"
    def _to_str(self):
        inner = ", ".join(str(t) for t in self.arg2)
        return f"TMopr({self.arg1};[{inner}])"

# Shortcuts for constructing terms
def TMvar(x): return term_var(x)
def TMlam(x, body): return term_lam(x, body)
def TMapp(f, x): return term_app(f, x)
def TMint(n): return term_int(n)
def TMbtf(b): return term_btf(b)
def TMif0(c, t1, t2): return term_if0(c, t1, t2)
def TMopr(op, args): return term_opr(op, args)

# Helper ops for arithmetic and comparison
def TMadd(a, b): return TMopr("+", [a, b])
def TMsub(a, b): return TMopr("-", [a, b])
def TMmul(a, b): return TMopr("*", [a, b])
def TMdiv(a, b): return TMopr("/", [a, b])
def TMmod(a, b): return TMopr("%", [a, b])
def TMlt(a, b): return TMopr("<", [a, b])
def TMgt(a, b): return TMopr(">", [a, b])
def TMeq(a, b): return TMopr("=", [a, b])
def TMlte(a, b): return TMopr("<=", [a, b])
def TMgte(a, b): return TMopr(">=", [a, b])
def TMneq(a, b): return TMopr("!=", [a, b])

# Y combinator (for recursion)
Y = TMlam("f", TMapp(
    TMlam("x", TMapp(TMvar("f"), TMapp(TMvar("x"), TMvar("x")))),
    TMlam("x", TMapp(TMvar("f"), TMapp(TMvar("x"), TMvar("x"))))
))



# 1) Term_print
# adapted from Lecture code lambda1.dats

def term_print(tm0):
    def aux(t):
        tag = t.ctag
        if tag == "TMint":
            return f"TMint({t.arg1})"
        if tag == "TMbtf":
            return f"TMbtf({t.arg1})"
        if tag == "TMvar":
            return f"TMvar({t.arg1})"
        if tag == "TMlam":
            return f"TMlam({t.arg1};{aux(t.arg2)})"
        if tag == "TMapp":
            return f"TMapp({aux(t.arg1)};{aux(t.arg2)})"
        if tag == "TMopr":
            inner = ", ".join(aux(x) for x in t.arg2)
            return f"TMopr({t.arg1};[{inner}])"
        if tag == "TMif0":
            return f"TMif0({aux(t.arg1)};{aux(t.arg2)};{aux(t.arg3)})"
        raise TypeError(f"Unknown term tag: {tag}")
    print(aux(tm0))


# 2) Substitution (termlist_subst + term_subst)
# Also adapted from lecture + Quiz1 code 

def termlist_subst(lst, x00, sub):
    return [term_subst(t, x00, sub) for t in lst]

def term_subst(tm0, x00, sub):
    def S(t): return term_subst(t, x00, sub)

    tag = tm0.ctag
    if tag == "TMint" or tag == "TMbtf":
        return tm0
    if tag == "TMvar":
        return sub if tm0.arg1 == x00 else tm0
    if tag == "TMlam":
        x1, body = tm0.arg1, tm0.arg2
        return tm0 if x1 == x00 else TMlam(x1, S(body))
    if tag == "TMapp":
        return TMapp(S(tm0.arg1), S(tm0.arg2))
    if tag == "TMopr":
        return TMopr(tm0.arg1, termlist_subst(tm0.arg2, x00, sub))
    if tag == "TMif0":
        return TMif0(S(tm0.arg1), S(tm0.arg2), S(tm0.arg3))
    raise TypeError(f"Unknown term in term_subst: {tag}")


# 3) Interpreter (call-by-name)
#Python version of ML code from lecture

def term_interp(tm0):
    tag = tm0.ctag
    if tag == "TMint" or tag == "TMbtf":
        return tm0
    if tag == "TMvar" or tag == "TMlam":
        return tm0

    if tag == "TMapp":
        f = term_interp(tm0.arg1)
        if f.ctag == "TMlam":
            # substitute and continue
            return term_interp(term_subst(f.arg2, f.arg1, tm0.arg2))
        return TMapp(f, term_interp(tm0.arg2))

    if tag == "TMopr":
        op = tm0.arg1
        a1, a2 = tm0.arg2
        v1 = term_interp(a1)
        v2 = term_interp(a2)
        i1 = v1.arg1 if v1.ctag == "TMint" else None
        i2 = v2.arg1 if v2.ctag == "TMint" else None

        if op == "+":
            return TMint(i1 + i2)
        if op == "-":
            return TMint(i1 - i2)
        if op == "*":
            return TMint(i1 * i2)
        if op == "/":
            return TMint(i1 // i2)
        if op == "%":
            return TMint(i1 % i2)
        if op == "<":
            return TMbtf(i1 < i2)
        if op == ">":
            return TMbtf(i1 > i2)
        if op == "=":
            return TMbtf(i1 == i2)
        if op == "<=":
            return TMbtf(i1 <= i2)
        if op == ">=":
            return TMbtf(i1 >= i2)
        if op == "!=":
            return TMbtf(i1 != i2)
        raise ValueError(f"Unknown operator: {op}")

    if tag == "TMif0":
        cond = term_interp(tm0.arg1)
        if cond.ctag != "TMbtf":
            raise ValueError("Condition did not evaluate to boolean")
        return term_interp(tm0.arg2 if cond.arg1 else tm0.arg3)

    raise TypeError(f"Unknown term in term_interp: {tag}")



# 4) Library Terms (combinators, numerals, etc)

x = TMvar("x")
y = TMvar("y")
z = TMvar("z")

I     = TMlam("x", x)
K     = TMlam("x", TMlam("y", x))
S     = TMlam("x", TMlam("y", TMlam("z",
             TMapp(TMapp(x, z), TMapp(y, z)))))
K1    = TMlam("x", TMlam("y", y))
omega = TMlam("x", TMapp(x, x))
Omega = TMapp(omega, omega)

# Church numerals 1 and 2
f = TMvar("f")
xx = TMvar("x")
TMone = TMlam("f", TMlam("x", TMapp(f, xx)))
TMtwo = TMlam("f", TMlam("x", TMapp(f, TMapp(f, xx))))

# Arithmetic lambdas
TMdbl = TMlam("x", TMadd(x, x))
TMtpl = TMlam("x", TMadd(x, TMadd(x, x)))
TMsqr = TMlam("x", TMmul(x, x))
TMcbr = TMlam("x", TMmul(x, TMmul(x, x)))

# Y combinator
f = TMvar("f")
xx = TMvar("x")
fomega = TMlam("x", TMapp(f, TMapp(xx, xx)))
Y = TMlam("f", TMapp(fomega, fomega))

# Factorial
x = TMvar("x")
F_body = TMlam("f", TMlam("x",
             TMif0(TMlte(x, TMint(0)),
                   TMint(1),
                   TMmul(x, TMapp(f, TMsub(x, TMint(1)))))))
TMfact = TMapp(Y, F_body)


# 5) Tests For check - Same from Lecture - lambda1.dats)

if __name__ == "__main__":
    for name, tm in [
        ("I", I), ("K", K), ("S", S), ("K1", K1),
        ("omega", omega), ("Omega", Omega),
        ("TMone", TMone), ("TMtwo", TMtwo),
        ("TMdbl", TMdbl), ("TMtpl", TMtpl),
        ("TMsqr", TMsqr), ("TMcbr", TMcbr)
    ]:
        print(f"{name} = ", end=""); term_print(tm)

    print("TMdbl 10 →", term_interp(TMapp(TMdbl, TMint(10))).arg1)
    print("TMsqr 10 →", term_interp(TMapp(TMsqr, TMint(10))).arg1)
    print("TMtwo(TMtpl) 10 →",
          term_interp(TMapp(TMapp(TMtwo, TMtpl), TMint(10))).arg1)
    print("Factorial 5 →", term_interp(TMapp(TMfact, TMint(5))).arg1)
