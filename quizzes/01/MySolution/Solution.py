# Final Submission for quizz 1

# Helper term constructors (from lecture code)
class term:
    ctag = ""
    def __str__(self): return "term(" + self.ctag + ")"

class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMvar"
    def __str__(self): return "TMvar(" + self.arg1 + ")"

class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMlam"
    def __str__(self): return "TMlam(" + self.arg1 + "," + str(self.arg2) + ")"

class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMapp"
    def __str__(self): return "TMapp(" + str(self.arg1) + "," + str(self.arg2) + ")"


#Aditional Casses for Question 3

class term_int(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMint"
    def __str__(self): return "TMint(" + str(self.arg1) + ")"

class term_btf(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMbtf"
    def __str__(self): return "TMbtf(" + str(self.arg1) + ")"

class term_if0(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMif0"
    def __str__(self): return "TMif0(" + str(self.arg1) + ";" + str(self.arg2) + ";" + str(self.arg3) + ")"

class term_opr(term):
    def __init__(self, opr, args):
        self.arg1 = opr
        self.arg2 = args
        self.ctag = "TMopr"
    def __str__(self): return "TMopr(" + self.arg1 + ";[" + ", ".join(str(t) for t in self.arg2) + "])"


# Shortcuts for constructing terms
def TMvar(x): return term_var(x)
def TMlam(x, body): return term_lam(x, body)
def TMapp(f, x): return term_app(f, x)
def TMint(n): return term_int(n)
def TMbtf(b): return term_btf(b)
def TMif0(c, t1, t2): return term_if0(c, t1, t2)
def TMopr(op, args): return term_opr(op, args)

# Helper ops
def TMadd(a, b): return TMopr("+", [a, b])
def TMsub(a, b): return TMopr("-", [a, b])
def TMmul(a, b): return TMopr("*", [a, b])
def TMdiv(a, b): return TMopr("/", [a, b])
def TMmod(a, b): return TMopr("%", [a, b])
def TMlte(a, b): return TMopr("<=", [a, b])
def TMgt(a, b): return TMopr(">", [a, b])
def TMeq(a, b): return TMopr("=", [a, b])
def TMneq(a, b): return TMopr("!=", [a, b])

# Y combinator
Y = TMlam("f", TMapp(
    TMlam("x", TMapp(TMvar("f"), TMapp(TMvar("x"), TMvar("x")))),
    TMlam("x", TMapp(TMvar("f"), TMapp(TMvar("x"), TMvar("x"))))
))

# QUESTION 1

x = TMvar("x")
f = TMvar("f")

F_fibo = TMlam("f", TMlam("x",
    TMif0(
        TMlte(x, TMint(1)),
        x,
        TMadd(
            TMapp(f, TMsub(x, TMint(1))),
            TMapp(f, TMsub(x, TMint(2)))
        )
    )
))

fibo_term = TMapp(Y, F_fibo)


# QUESTION 2. isPrime

# Part 1, python 
def isPrime(n):
    if n <= 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

# Part 2, Lambda calculus representation
n = TMvar("n")
f = TMvar("f")

inner_checker = TMlam("i",
    TMif0(
        TMgt(TMmul(TMvar("i"), TMvar("i")), n),
        TMbtf(True),
        TMif0(
            TMeq(TMmod(n, TMvar("i")), TMint(0)),
            TMbtf(False),
            TMapp(f, TMadd(TMvar("i"), TMint(1)))
        )
    )
)

F_prime = TMlam("f", TMlam("n",
    TMif0(
        TMlte(n, TMint(1)),
        TMbtf(False),
        TMapp(inner_checker, TMint(2))
    )
))

isPrime_term = TMapp(Y, F_prime)

# QUESTION 3: term_subst update

def termlist_subst(lst, x00, sub):
    return [term_subst(t, x00, sub) for t in lst]

def term_subst(tm0, x00, sub):
    def subst(t): return term_subst(t, x00, sub)

    if tm0.ctag == "TMvar":
        x01 = tm0.arg1
        return sub if x00 == x01 else tm0

    elif tm0.ctag == "TMlam":
        x01 = tm0.arg1
        tm1 = tm0.arg2
        return tm0 if x00 == x01 else term_lam(x01, subst(tm1))

    elif tm0.ctag == "TMapp":
        tm1 = tm0.arg1
        tm2 = tm0.arg2
        return term_app(subst(tm1), subst(tm2))

    elif tm0.ctag == "TMint" or tm0.ctag == "TMbtf":
        return tm0

    elif tm0.ctag == "TMif0":
        cond = subst(tm0.arg1)
        then_branch = subst(tm0.arg2)
        else_branch = subst(tm0.arg3)
        return term_if0(cond, then_branch, else_branch)

    elif tm0.ctag == "TMopr":
        op = tm0.arg1
        args = tm0.arg2
        return term_opr(op, termlist_subst(args, x00, sub))

    else:
        raise TypeError(f"Unknown term: {tm0}")


# Test Cases:

if __name__ == "__main__":
    x = term_var("x")
    y = term_var("y")
    z = term_var("z")
    lam_x = term_lam("x", x)  # λx. x

    print("Substitute x with y in x:", term_subst(x, "x", y))
    print("Substitute x with y in λx. x:", term_subst(lam_x, "x", y))
    print("Substitute x with y in λz. x:", term_subst(term_lam("z", x), "x", y))

    opr_term = term_opr("+", [x, z])
    print("Substitute x with y in TMopr('+', [x, z]):", term_subst(opr_term, "x", y))
