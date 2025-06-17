# Midterm solution: interpreter and translation

# Data types for the extended lambda calculus
import sys
sys.setrecursionlimit(100000)

class term:
    ctag = ""
    def __str__(self):
        return f"term({self.ctag})"

class term_int(term):
    def __init__(self, n):
        self.arg1 = n
        self.ctag = "TMint"
    def __str__(self):
        return f"TMint({self.arg1})"

class term_btf(term):
    def __init__(self, b):
        self.arg1 = b
        self.ctag = "TMbtf"
    def __str__(self):
        return f"TMbtf({self.arg1})"

class term_var(term):
    def __init__(self, name):
        self.arg1 = name
        self.ctag = "TMvar"
    def __str__(self):
        return f"TMvar({self.arg1})"

class term_lam(term):
    def __init__(self, x, body):
        self.arg1 = x
        self.arg2 = body
        self.ctag = "TMlam"
    def __str__(self):
        return f"TMlam({self.arg1};{self.arg2})"

class term_app(term):
    def __init__(self, f, a):
        self.arg1 = f
        self.arg2 = a
        self.ctag = "TMapp"
    def __str__(self):
        return f"TMapp({self.arg1};{self.arg2})"

class term_opr(term):
    def __init__(self, opr, args):
        self.arg1 = opr
        self.arg2 = args
        self.ctag = "TMopr"
    def __str__(self):
        return f"TMopr({self.arg1};{self.arg2})"

class term_if0(term):
    def __init__(self, cnd, thn, els):
        self.arg1 = cnd
        self.arg2 = thn
        self.arg3 = els
        self.ctag = "TMif0"
    def __str__(self):
        return f"TMif0({self.arg1};{self.arg2};{self.arg3})"

class term_fix(term):
    def __init__(self, f, x, body):
        self.arg1 = f
        self.arg2 = x
        self.arg3 = body
        self.ctag = "TMfix"
    def __str__(self):
        return f"TMfix({self.arg1};{self.arg2};{self.arg3})"

class term_tup(term):
    def __init__(self, t1, t2):
        self.arg1 = t1
        self.arg2 = t2
        self.ctag = "TMtup"

class term_fst(term):
    def __init__(self, t):
        self.arg1 = t
        self.ctag = "TMfst"

class term_snd(term):
    def __init__(self, t):
        self.arg1 = t
        self.ctag = "TMsnd"

class term_let(term):
    def __init__(self, x, t1, t2):
        self.arg1 = x
        self.arg2 = t1
        self.arg3 = t2
        self.ctag = "TMlet"

# value classes
class tval:
    ctag = ""

class tval_int(tval):
    def __init__(self, n):
        self.arg1 = n
        self.ctag = "TVint"

class tval_btf(tval):
    def __init__(self, b):
        self.arg1 = b
        self.ctag = "TVbtf"

class tval_clo(tval):
    def __init__(self, lam, env):
        self.arg1 = lam
        self.arg2 = env
        self.ctag = "TVclo"

class tval_tup(tval):
    def __init__(self, v1, v2):
        self.arg1 = v1
        self.arg2 = v2
        self.ctag = "TVtup"

# environment
class xenv:
    ctag = ""

class xenv_nil(xenv):
    def __init__(self):
        self.ctag = "EVnil"

class xenv_cons(xenv):
    def __init__(self, x, v, env):
        self.arg1 = x
        self.arg2 = v
        self.arg3 = env
        self.ctag = "EVcons"

# lookup helper

def xenv_search(env, x):
    if isinstance(env, xenv_nil):
        return None
    if isinstance(env, xenv_cons):
        if env.arg1 == x:
            return env.arg2
        return xenv_search(env.arg3, x)
    raise TypeError(env)

# evaluation

def term_eval(tm, env=None):
    if env is None:
        env = xenv_nil()
    if isinstance(tm, term_int):
        return tval_int(tm.arg1)
    if isinstance(tm, term_btf):
        return tval_btf(tm.arg1)
    if isinstance(tm, term_var):
        val = xenv_search(env, tm.arg1)
        if val is None:
            raise RuntimeError(f"unbound variable {tm.arg1}")
        return val
    if isinstance(tm, term_lam):
        return tval_clo(tm, env)
    if isinstance(tm, term_fix):
        return tval_clo(tm, env)
    if isinstance(tm, term_app):
        v1 = term_eval(tm.arg1, env)
        v2 = term_eval(tm.arg2, env)
        assert isinstance(v1, tval_clo)
        lam = v1.arg1
        if isinstance(lam, term_lam):
            env1 = xenv_cons(lam.arg1, v2, v1.arg2)
            return term_eval(lam.arg2, env1)
        if isinstance(lam, term_fix):
            env1 = xenv_cons(lam.arg2, v2, v1.arg2)
            env1 = xenv_cons(lam.arg1, v1, env1)
            return term_eval(lam.arg3, env1)
        raise TypeError(lam)
    if isinstance(tm, term_opr):
        args = [term_eval(a, env) for a in tm.arg2]
        if tm.arg1 == "+":
            return tval_int(args[0].arg1 + args[1].arg1)
        if tm.arg1 == "-":
            return tval_int(args[0].arg1 - args[1].arg1)
        if tm.arg1 == "*":
            return tval_int(args[0].arg1 * args[1].arg1)
        if tm.arg1 == "<":
            return tval_btf(args[0].arg1 < args[1].arg1)
        if tm.arg1 == "<=":
            return tval_btf(args[0].arg1 <= args[1].arg1)
        if tm.arg1 == ">":
            return tval_btf(args[0].arg1 > args[1].arg1)
        if tm.arg1 == ">=":
            return tval_btf(args[0].arg1 >= args[1].arg1)
        if tm.arg1 == "=":
            return tval_btf(args[0].arg1 == args[1].arg1)
        if tm.arg1 == "!=":
            return tval_btf(args[0].arg1 != args[1].arg1)
        raise Exception("unknown operator" + tm.arg1)
    if isinstance(tm, term_if0):
        c = term_eval(tm.arg1, env)
        assert isinstance(c, tval_btf)
        if c.arg1:
            return term_eval(tm.arg2, env)
        else:
            return term_eval(tm.arg3, env)
    if isinstance(tm, term_tup):
        v1 = term_eval(tm.arg1, env)
        v2 = term_eval(tm.arg2, env)
        return tval_tup(v1, v2)
    if isinstance(tm, term_fst):
        p = term_eval(tm.arg1, env)
        assert isinstance(p, tval_tup)
        return p.arg1
    if isinstance(tm, term_snd):
        p = term_eval(tm.arg1, env)
        assert isinstance(p, tval_tup)
        return p.arg2
    if isinstance(tm, term_let):
        v1 = term_eval(tm.arg2, env)
        env1 = xenv_cons(tm.arg1, v1, env)
        return term_eval(tm.arg3, env1)
    raise TypeError(tm)

# Helper constructors

def t_int(n):
    return term_int(n)

def t_bool(b):
    return term_btf(b)

def t_var(x):
    return term_var(x)

def t_add(a,b):
    return term_opr("+", [a,b])

def t_sub(a,b):
    return term_opr("-", [a,b])

def t_mul(a,b):
    return term_opr("*", [a,b])

def t_lt(a,b):
    return term_opr("<", [a,b])

def t_le(a,b):
    return term_opr("<=", [a,b])

def t_gt(a,b):
    return term_opr(">", [a,b])

def t_ge(a,b):
    return term_opr(">=", [a,b])

def t_eq(a,b):
    return term_opr("=", [a,b])

def t_neq(a,b):
    return term_opr("!=", [a,b])

def t_let(x,t1,t2):
    return term_let(x,t1,t2)

# boolean helpers
var_a = t_var("a")
var_b = t_var("b")

bool_and = term_lam("a", term_lam("b", term_if0(var_a, var_b, t_bool(False))))

bool_or = term_lam("a", term_lam("b", term_if0(var_a, t_bool(True), var_b)))

# --------------------------------------------------------------------
#  translation of the 8-queens puzzle
# --------------------------------------------------------------------

# The board is represented as a function from row index to column index
# board_set returns a new board where row i holds column j

const_N = t_int(8)

var_bd = t_var("bd")
var_i = t_var("i")
var_j = t_var("j")
var_k = t_var("k")

board_get = term_lam("bd", term_lam("i", term_app(var_bd, var_i)))

board_set = term_lam("bd",
    term_lam("i",
        term_lam("j",
            term_lam("k",
                term_if0(
                    t_eq(var_k, var_i),
                    var_j,
                    term_app(var_bd, var_k)
                )))))

# safety_test1: check if a queen at (i0,j0) is safe with respect to (i,j)
var_i0 = t_var("i0")
var_j0 = t_var("j0")

safety_test1 = term_lam("i0",
    term_lam("j0",
        term_lam("i",
            term_lam("j",
                term_app(
                    term_app(bool_and,
                        t_neq(var_j0, var_j)),
                    t_neq(
                        t_mul(t_sub(var_i0, var_i), t_sub(var_i0, var_i)),
                        t_mul(t_sub(var_j0, var_j), t_sub(var_j0, var_j))
                    )
                )))))

# safety_test2: recursively test the safety of queen (i0,j0)
var_bd2 = t_var("bd2")
var_idx = t_var("idx")

safety_test2 = term_fix("st2", "i0",
    term_lam("j0",
        term_lam("bd2",
            term_lam("idx",
                term_if0(
                    t_ge(var_idx, t_int(0)),
                    term_if0(
                        term_app(
                            term_app(
                                term_app(
                                    term_app(safety_test1, var_i0), var_j0),
                                var_idx),
                            term_app(term_app(board_get, var_bd2), var_idx)
                        ),
                        term_app(
                            term_app(
                                term_app(
                                    term_app(term_var("st2"), var_i0), var_j0),
                                var_bd2),
                            t_sub(var_idx, t_int(1))
                        ),
                        t_bool(False)
                    ),
                    t_bool(True)
                )))))

# search function
var_bd3 = t_var("bd3")
var_j3 = t_var("j3")
var_i3 = t_var("i3")
var_nsol = t_var("nsol")

search = term_fix("search", "bd3",
    term_lam("i3",
        term_lam("j3",
            term_lam("nsol",
                term_if0(
                    t_lt(var_j3, const_N),
                    t_let(
                        "test",
                        term_app(
                            term_app(
                                term_app(
                                    term_app(safety_test2, var_i3), var_j3),
                                var_bd3),
                            t_sub(var_i3, t_int(1))
                        ),
                        term_if0(
                            t_var("test"),
                            t_let(
                                "bd1",
                                term_app(
                                    term_app(
                                        term_app(board_set, var_bd3), var_i3),
                                    var_j3
                                ),
                                term_if0(
                                    t_eq(t_add(var_i3, t_int(1)), const_N),
                                    term_app(
                                        term_app(
                                            term_app(
                                                term_app(term_var("search"), var_bd3),
                                                var_i3),
                                            t_add(var_j3, t_int(1))),
                                        t_add(var_nsol, t_int(1))
                                    ),
                                    term_app(
                                        term_app(
                                            term_app(
                                                term_app(term_var("search"), t_var("bd1")),
                                                t_add(var_i3, t_int(1))),
                                            t_int(0)),
                                        var_nsol
                                    )
                                )
                            ),
                            term_app(
                                term_app(
                                    term_app(
                                        term_app(term_var("search"), var_bd3), var_i3),
                                    t_add(var_j3, t_int(1))),
                                var_nsol
                            )
                        )
                    ),
                    term_if0(
                        t_gt(var_i3, t_int(0)),
                        term_app(
                            term_app(
                                term_app(
                                    term_app(term_var("search"), var_bd3),
                                    t_sub(var_i3, t_int(1))),
                                t_add(
                                    term_app(
                                        term_app(board_get, var_bd3),
                                        t_sub(var_i3, t_int(1))),
                                    t_int(1)
                                )),
                            var_nsol
                        ),
                        var_nsol
                    )
                )
            ))))

if __name__ == "__main__":
    # simple check of board functions
    const0 = term_lam("_", t_int(0))
    bd1 = term_app(term_app(term_app(board_set, const0), t_int(2)), t_int(3))
    res = term_eval(term_app(term_app(board_get, bd1), t_int(2)))
    print("test board_get:", res.arg1)

    # Full search:
    
    start = term_app(
         term_app(
             term_app(
                 term_app(search, const0),
                 t_int(0)),
             t_int(0)),
         t_int(0))
    result = term_eval(start)
    print("number of solutions:", result.arg1)
    
