"""
Part 2: Interpreter for the Extended Lambda Calculus (Task 2)
"""

import sys
sys.setrecursionlimit(10000)

# datatype term =
# | TMint of int
# | TMbtf of bool
# | TMvar of strn
# | TMlam of (strn, term)
# | TMapp of (term, term)
# | TMopr of (strn(*opr*), list(term))
# | TMif0 of (term, term, term)
# | TMfix of (strn(*f*), strn(*x*), term)

class term:
    ctag = ""
    def __str__(self):
        return ("term(" + self.ctag + ")")
# end-of-class(term)

class term_int(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMint"
    def __str__(self):
        return ("TMint(" + str(self.arg1) + ")")
# end-of-class(term_int(term))

class term_btf(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMbtf"
    def __str__(self):
        return ("TMbtf(" + str(self.arg1) + ")")
# end-of-class(term_btf(term))

class term_var(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMvar"
    def __str__(self):
        return ("TMvar(" + self.arg1 + ")")
# end-of-class(term_var(term))

class term_lam(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMlam"
    def __str__(self):
        return ("TMlam(" + self.arg1 + ";" + str(self.arg2) + ")")
# end-of-class(term_lam(term))

class term_app(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMapp"
    def __str__(self):
        return ("TMapp(" + str(self.arg1) + ";" + str(self.arg2) + ")")
# end-of-class(term_app(term))

##################################################################

class term_opr(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMopr"
    def __str__(self):
        return ("TMopr(" + self.arg1 + ";" + str(self.arg2) + ")")
# end-of-class(term_opr(term))

class term_if0(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMif0"
    def __str__(self):
        return ("TMif0(" + str(self.arg1) + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")
# end-of-class(term_if0(term))

class term_fix(term):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "TMfix"
    def __str__(self):
        return ("TMfix(" + self.arg1 + ";" + self.arg2 + ";" + str(self.arg3) + ")")
# end-of-class(term_fix(term))

# === New for extended lambda ===

class term_tup(term):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TMtup"
    def __str__(self):
        return ("TMtup(" + str(self.arg1) + "," + str(self.arg2) + ")")

class term_fst(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMfst"
    def __str__(self):
        return ("TMfst(" + str(self.arg1) + ")")

class term_snd(term):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TMsnd"
    def __str__(self):
        return ("TMsnd(" + str(self.arg1) + ")")

class term_let(term):
    def __init__(self, x, t1, t2):
        self.arg1 = x
        self.arg2 = t1
        self.arg3 = t2
        self.ctag = "TMlet"
    def __str__(self):
        return ("TMlet(" + self.arg1 + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")


##################################################################

# datatype tval =
# | TVint of int
# | TVbtf of bool
# | TVclo of (term, xenv)

class tval:
    ctag = ""
    def __str__(self):
        return ("tval(" + self.ctag + ")")
# end-of-class(tval)

class tval_int(tval):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TVint"
    def __str__(self):
        return ("TVint(" + str(self.arg1) + ")")
# end-of-class(tval_int(tval))

class tval_btf(tval):
    def __init__(self, arg1):
        self.arg1 = arg1
        self.ctag = "TVbtf"
    def __str__(self):
        return ("TVbtf(" + str(self.arg1) + ")")
# end-of-class(tval_btf(tval))

class tval_clo(tval):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TVclo"
    def __str__(self):
        return ("TVclo(" + str(self.arg1) + ";" + str(self.arg2) + ")")
# end-of-class(tval_clo(tval))

##ADDED new tval class
class tval_tup(tval):
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.ctag = "TVtup"
    def __str__(self):
        return ("TVtup(" + str(self.arg1) + "," + str(self.arg2) + ")")


##################################################################

# datatype xenv =
# | EVnil of ()
# | EVcons of (strn, tval, xenv)

class xenv:
    ctag = ""
    def __str__(self):
        return ("xenv(" + self.ctag + ")")
# end-of-class(xenv)

class xenv_nil(xenv):
    def __init__(self):
        self.ctag = "EVnil"
    def __str__(self):
        return ("EVnil(" + ")")
# end-of-class(xenv_nil(xenv))

class xenv_cons(xenv):
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.ctag = "EVcons"
    def __str__(self):
        return ("EVcons(" + self.arg1 + ";" + str(self.arg2) + ";" + str(self.arg3) + ")")
# end-of-class(xenv_cons(xenv))

##################################################################

term_add = lambda a1, a2: term_opr("+", [a1, a2])
term_sub = lambda a1, a2: term_opr("-", [a1, a2])
term_mul = lambda a1, a2: term_opr("*", [a1, a2])
term_div = lambda a1, a2: term_opr("/", [a1, a2])
term_mod = lambda a1, a2: term_opr("%", [a1, a2])

term_lt0 = lambda a1, a2: term_opr("<", [a1, a2])
term_gt0 = lambda a1, a2: term_opr(">", [a1, a2])
term_eq0 = lambda a1, a2: term_opr("=", [a1, a2])
term_lte = lambda a1, a2: term_opr("<=", [a1, a2])
term_gte = lambda a1, a2: term_opr(">=", [a1, a2])
term_neq = lambda a1, a2: term_opr("!=", [a1, a2])
term_cmp = lambda a1, a2: term_opr("cmp", [a1, a2])

##################################################################


def term_eval00(tm0):
    return term_eval01(tm0, builtins_env())

##################################################################

def xenv_search(env, x00):
    if env.ctag == "EVnil":
        return None
    if env.ctag == "EVcons":
        if env.arg1 == x00:
            return env.arg2
        else:
            return xenv_search(env.arg3, x00)
    raise TypeError(env) # HX-2025-06-03: deadcode!

##################################################################
        
def term_eval01(tm0, env):
    # print("term_eval01: tm0 = " + str(tm0))
    if (tm0.ctag == "TMint"):
        return tval_int(tm0.arg1)
    if (tm0.ctag == "TMbtf"):
        return tval_btf(tm0.arg1)
    if (tm0.ctag == "TMlam"):
        return tval_clo(tm0, env)
    if (tm0.ctag == "TMfix"):
        return tval_clo(tm0, env)
    if (tm0.ctag == "TMvar"):
        tv0 = xenv_search(env, tm0.arg1)
        assert tv0 is not None
        return tv0
    if (tm0.ctag == "TMopr"):
        pnm = tm0.arg1
        ags = tm0.arg2 # list of arguments
        if (pnm == "+"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            # print("TMopr: tv1 = " + str(tv1))
            # print("TMopr: tv2 = " + str(tv2))
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_int(tv1.arg1 + tv2.arg1)
        if (pnm == "-"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_int(tv1.arg1 - tv2.arg1)
        if (pnm == "*"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_int(tv1.arg1 * tv2.arg1)
        if (pnm == "%"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_int(tv1.arg1 % tv2.arg1)
        if (pnm == "/"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_int(tv1.arg1 // tv2.arg1)
        if (pnm == "<"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_btf(tv1.arg1 < tv2.arg1)
        if (pnm == ">"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_btf(tv1.arg1 > tv2.arg1)
        if (pnm == "="):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_btf(tv1.arg1 == tv2.arg1)
        if (pnm == "<="):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_btf(tv1.arg1 <= tv2.arg1)
        if (pnm == ">="):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_btf(tv1.arg1 >= tv2.arg1)
        if (pnm == "&&"):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVbtf"
            assert tv2.ctag == "TVbtf"
            return tval_btf(tv1.arg1 and tv2.arg1)
        if (pnm == "!="):
            assert len(ags) == 2
            tv1 = term_eval01(ags[0], env)
            tv2 = term_eval01(ags[1], env)
            assert tv1.ctag == "TVint"
            assert tv2.ctag == "TVint"
            return tval_btf(tv1.arg1 != tv2.arg1)
        if (pnm == "print_board"):
            assert len(ags) == 1
            tv_bd = term_eval01(ags[0], env)
            print_board(tv_bd)
            return tval_int(0)
        raise TypeError(pnm) # HX-2025-06-03: unsupported!
    if (tm0.ctag == "TMapp"):
        tm1 = tm0.arg1
        tv1 = term_eval01(tm1, env)
        assert tv1.ctag == "TVclo"
        tm2 = tm0.arg2
        tv2 = term_eval01(tm2, env)
        tmf = tv1.arg1
        env = tv1.arg2
        if tmf.ctag == "TMlam":
            x01 = tmf.arg1
            env = xenv_cons(x01, tv2, env)
            return term_eval01(tmf.arg2, env)
        if tmf.ctag == "TMfix":
            f00 = tmf.arg1
            env = xenv_cons(f00, tv1, env)
            x01 = tmf.arg2
            env = xenv_cons(x01, tv2, env)
            return term_eval01(tmf.arg3, env)
        raise TypeError(tmf) # HX-2025-06-03: type error!
    if (tm0.ctag == "TMif0"):
        tm1 = tm0.arg1
        tv1 = term_eval01(tm1, env)
        assert tv1.ctag == "TVbtf"
        if tv1.arg1:
            return term_eval01(tm0.arg2, env) # then
        else:
            return term_eval01(tm0.arg3, env) # else
        ###Added- to Handle New Terms
    if tm0.ctag == "TMtup":
        tv1 = term_eval01(tm0.arg1, env)
        tv2 = term_eval01(tm0.arg2, env)
        return tval_tup(tv1, tv2)

    if tm0.ctag == "TMfst":
        tv0 = term_eval01(tm0.arg1, env)
        assert tv0.ctag == "TVtup"
        return tv0.arg1

    if tm0.ctag == "TMsnd":
        tv0 = term_eval01(tm0.arg1, env)
        assert tv0.ctag == "TVtup"
        return tv0.arg2

    if tm0.ctag == "TMlet":
        x = tm0.arg1
        t1 = tm0.arg2
        t2 = tm0.arg3
        v1 = term_eval01(t1, env)
        return term_eval01(t2, xenv_cons(x, v1, env))

    raise TypeError(tm0) # HX-2025-05-27: should be deadcode!    

##################################################################

var_x = term_var("x")
var_y = term_var("y")
var_f = term_var("f")
var_n = term_var("n")
int_0 = term_int( 0 )
int_1 = term_int( 1 )
int_5 = term_int( 5 )
btf_t = term_btf(True)
btf_f = term_btf(False)

##################################################################

# Builtin environment providing primitive functions like [abs]
def builtins_env():
    env = xenv_nil()
    x = term_var("x")
    abs_body = TMif0(
        TMopr("<", [x, TMint(0)]),
        TMopr("-", [TMint(0), x]),
        x,
    )
    abs_val = term_eval01(TMlam("x", abs_body), env)
    env = xenv_cons("abs", abs_val, env)
    return env

def tup_to_list(tv, n):
    res = []
    cur = tv
    for _ in range(n):
        assert cur.ctag == "TVtup"
        assert cur.arg1.ctag == "TVint"
        res.append(cur.arg1.arg1)
        cur = cur.arg2
    return res

def print_board(tv_bd):
    cols = tup_to_list(tv_bd, 8)
    for r in range(8):
        j = cols[r]
        line = ". " * j + "Q " + ". " * (8 - j - 1)
        print(line)
    print()

##################################################################

# print("eval(int_1) = " + str(term_eval00(int_1)))
# print("eval(btf_t) = " + str(term_eval00(btf_t)))
# print("eval(int_1 + int_1) = " + str(term_eval00(term_add(int_1, int_1))))
# print("eval(int_1 - int_1) = " + str(term_eval00(term_sub(int_1, int_1))))
# print("eval(int_1 <= int_1) = " + str(term_eval00(term_lte(int_1, int_1))))

##################################################################

term_dbl = term_lam("x", term_add(var_x, var_x))
# print("eval(term_dbl(int_1)) = " + str(term_eval00(term_app(term_dbl, int_1))))

##################################################################


##################################################################

# HX-2025-06-04:
# Doing arithmetic in pure lambda-calculus
# What is 'two'?
# It means applying a function to its argument twice?
# What is 'three'?
# It means applying a function to its argument thrice?
# two: lam f.lam x.f(f(x)); three: lam f.lam x.f(f(f(x)))
# A 'numeral' means the representation of a number
# For instance, Roman numerals; MMXXV = 2025
# Church numeral for zero: lam f.lam x.x
# Church numeral for one: lam f.lam x.f(x)
# Church numeral for two: lam f.lam x.f(f(x))
# Church numeral for three: lam f.lam x.f(f(f(x)))

var_x = term_var("x")
var_f = term_var("f")
CHNUM0 = term_lam("f", term_lam("x", var_x))
CHNUM1 = term_lam("f", term_lam("x", term_app(var_f, var_x)))
CHNUM2 = term_lam("f", term_lam("x", term_app(var_f, term_app(var_f, var_x))))
CHNUM3 = term_lam("f", term_lam("x", term_app(var_f, term_app(var_f, term_app(var_f, var_x)))))

term_suc = term_lam("n", term_add(var_n, int_1))
def chnum_toint(chnum):
    res = term_eval00(term_app(term_app(chnum, term_suc), int_0))
    assert res.ctag == "TVint"
    return res.arg1
# print("CHNUM3 = " + str(CHNUM3))
# print("CHNUM3 = " + str(chnum_toint(CHNUM3)))

def int_tochnum(n0):
    assert n0 >= 0
    res = var_x
    while (n0 >= 1):
        n0 -= 1
        res = term_app(var_f, res)
    return term_lam("f", term_lam("x", res))

# print("CHNUM1000 = " + str(chnum_toint(int_tochnum(1000))))

##################################################################

# HX-2025-06-04:
# Handling booleans (true and false) in pure lambda-calculus
# TMif0(tm1, tm2, tm3) = tm1(tm2)(tm3)

var_x = term_var("x")
var_y = term_var("y")
chtru = term_lam("x", term_lam("y", var_x)) # for representing true
chfls = term_lam("x", term_lam("y", var_y)) # for representing false

def church_if0(tm1, tm2, tm3):
    return \
      term_app(term_app(
        term_app(tm1, term_lam("", tm2)), term_lam("", tm3)), chtru)

##################################################################
#
# chnum_suc = lam n.(lam f.lam x.n(f)(f(x)))
#
chnum_suc = \
    term_lam("n", \
      term_lam("f", \
        term_lam("x", \
          term_app(term_app(var_n, var_f), term_app(var_f, var_x)))))
#

CHNUM4 = term_app(chnum_suc, CHNUM3)
# print("CHNUM4 = " + str(chnum_toint(CHNUM4)))

# def myadd(x, y):
#     if x==0:
#         return y
#     else:
#         return 1 + myadd(x-1, y)


var_m = term_var("m")
var_n = term_var("n")

#
# chnum_add =
# lam m.lam n.(lam f.lam x.m(f)(n(f)(x)))
#
chnum_add = \
  term_lam("m", term_lam("n", \
    term_lam("f", term_lam("x", \
        term_app(term_app(var_m, var_f), \
          term_app(term_app(var_n, var_f), var_x))))))

CHNUM7 = \
  term_app(\
    term_app(chnum_add, CHNUM3), CHNUM4)
# print("CHNUM7 = " + str(chnum_toint(CHNUM7)))

# chnum_mul =
# lam m.lam n.(lam f.lam x.m(n(f))(x))
chnum_mul = \
  term_lam("m", term_lam("n", \
    term_lam("f", term_lam("x", \
      term_app(term_app(var_m, term_app(var_n, var_f)), var_x)))))

CHNUM49 = \
  term_app(\
    term_app(chnum_mul, CHNUM7), CHNUM7)
# print("CHNUM49 = " + str(chnum_toint(CHNUM49)))

# HX-2025-06-04:
# This is what [pre_helper] does:
# (0, 0) -> (1, 0) -> (2, 1) -> (3, 2) -> ...

var_p = term_var("p")
var_t = term_var("t")

def chpair(x, y):
    return term_lam("t", term_app(term_app(var_t, x), y))

def f_chnum_pre():
    chnum_pre_helper = \
      term_lam("p", \
        chpair(term_app(chnum_suc, term_app(var_p, chtru)), term_app(var_p, chtru)))
    return \
      term_lam("n", term_app(term_app(term_app(var_n, chnum_pre_helper), chpair(CHNUM0, CHNUM0)), chfls))

chnum_pre = f_chnum_pre()

CHNUM0 = term_app(chnum_pre, CHNUM0)
# print("CHNUM0 = " + str(chnum_toint(CHNUM0)))
CHNUM0 = term_app(chnum_pre, CHNUM1)
# print("CHNUM0 = " + str(chnum_toint(CHNUM0)))
CHNUM1 = term_app(chnum_pre, CHNUM2)
# print("CHNUM1 = " + str(chnum_toint(CHNUM1)))
CHNUM6 = term_app(chnum_pre, CHNUM7)
# print("CHNUM6 = " + str(chnum_toint(CHNUM6)))
CHNUM5 = term_app(chnum_pre, CHNUM6)
# print("CHNUM5 = " + str(chnum_toint(CHNUM5)))
#
# HX-2025-06-05:
# This one takes forever!!!
# CHNUM48 = term_app(chnum_pre, CHNUM49)
# print("CHNUM48 = " + str(chnum_toint(CHNUM48)))
#

chnum_gtz = \
  term_lam("n", \
    term_app(term_app(var_n, term_lam("", chtru)), chfls))

def lambda_fix(f00, x01, tmx):
    f = term_var("f")
    x = term_var("x")
    y = term_var("y")
    fxxy = \
      term_lam("x", term_lam("y", \
        term_app(term_app(f, term_app(x, x)), y)))
    Yval = term_lam("f", term_app(fxxy, fxxy))
    return term_app(Yval, term_lam(f00, term_lam(x01, tmx)))

chnum_fact = \
  lambda_fix("f", "n", \
    church_if0(term_app(chnum_gtz, var_n), \
      term_app(term_app(chnum_mul, var_n), \
        term_app(var_f, term_app(chnum_pre, var_n))), CHNUM1))

# print("chnum_fact(0) = " + str(chnum_toint(term_app(chnum_fact, CHNUM0))))
# print("chnum_fact(3) = " + str(chnum_toint(term_app(chnum_fact, CHNUM3))))
# print("chnum_fact(5) = " + str(chnum_toint(term_app(chnum_fact, CHNUM5))))
# print("chnum_fact(7) = " + str(chnum_toint(term_app(chnum_fact, CHNUM7))))

##################################################################
# end of [CS391-2025-Summer/lectures/lecture-06-03/lambda1.py]
##################################################################
"""

PART 1 -

"""


TMint = term_int
TMbtf = term_btf
TMvar = term_var
TMlam = term_lam
TMapp = term_app
TMfix = term_fix
TMopr = term_opr
TMif0 = term_if0
TMtup = term_tup
TMfst = term_fst
TMsnd = term_snd
TMlet = term_let
TMBtf = tval_btf 
"""
Part 1: Eight Queens Puzzle encoded in LAMBDA (Task 1)
"""

def proj(bd, idx):
    t = bd
    for _ in range(idx):
        t = TMsnd(t)
    if idx == 7:
        return t
    else:
        return TMfst(t)

def board_tuple(elems):
    assert len(elems) == 8
    t = elems[7]
    for k in range(6, -1, -1):
        t = TMtup(elems[k], t)
    return t

def make_board_get():
    bd = TMvar("bd")
    i = TMvar("i")
    body = TMint(-1)
    for idx in reversed(range(8)):
        body = TMif0(TMopr("=", [i, TMint(idx)]), proj(bd, idx), body)
    return TMlam("bd", TMlam("i", body))

board_get = make_board_get()

def make_board_set():
    bd = TMvar("bd")
    i = TMvar("i")
    j = TMvar("j")
    vals = [proj(bd, k) for k in range(8)]
    body = board_tuple(vals)
    for idx in reversed(range(8)):
        temp = vals.copy()
        temp[idx] = j
        body = TMif0(TMopr("=", [i, TMint(idx)]), board_tuple(temp), body)
    return TMlam("bd", TMlam("i", TMlam("j", body)))

board_set = make_board_set()

safety_test1 = TMlam("i0",
    TMlam("j0",
    TMlam("i",
    TMlam("j",
        TMopr("&&", [
            TMopr("!=", [TMvar("j0"), TMvar("j")]),
            TMopr("!=", [
                TMapp(TMvar("abs"), TMopr("-", [TMvar("i0"), TMvar("i")])),
                TMapp(TMvar("abs"), TMopr("-", [TMvar("j0"), TMvar("j")]))
            ])
        ])
    ))))

def make_safety_test2():
    i0 = TMvar("i0")
    j0 = TMvar("j0")
    bd = TMvar("bd")
    i = TMvar("i")
    f = TMvar("safety_test2")
    body = TMif0(
        TMopr(">=", [i, TMint(0)]),
        TMif0(
            TMapp(TMapp(TMapp(TMapp(safety_test1, i0), j0), i),
                  TMapp(TMapp(board_get, bd), i)),
            TMapp(TMapp(TMapp(TMapp(f, i0), j0), bd),
                  TMopr("-", [i, TMint(1)])),
            TMbtf(False)
        ),
        TMbtf(True)
    )
    fix = TMfix("safety_test2", "i", body)
    return TMlam("i0", TMlam("j0", TMlam("bd", fix)))

safety_test2 = make_safety_test2()

def make_search():
    bd = TMvar("bd")
    i = TMvar("i")
    j = TMvar("j")
    nsol = TMvar("nsol")
    f = TMvar("search")

    test = TMapp(TMapp(TMapp(TMapp(safety_test2, i), j), bd),
                 TMopr("-", [i, TMint(1)]))

    bd1 = TMapp(TMapp(TMapp(board_set, bd), i), j)

    then_branch = TMlet("bd1", bd1,
        TMif0(TMopr("=", [TMopr("+", [i, TMint(1)]), TMint(8)]),
            TMlet("_", TMopr("print_board", [TMvar("bd1")]),
                TMapp(TMapp(TMapp(TMapp(f, bd), i), TMopr("+", [j, TMint(1)])),
                     TMopr("+", [nsol, TMint(1)]))
            ),
            TMapp(TMapp(TMapp(TMapp(f, TMvar("bd1")), TMopr("+", [i, TMint(1)])), TMint(0)), nsol)
        ))

    when_j_lt = TMif0(test, then_branch,
        TMapp(TMapp(TMapp(TMapp(f, bd), i), TMopr("+", [j, TMint(1)])), nsol))

    else_branch = TMif0(TMopr(">", [i, TMint(0)]),
        TMapp(TMapp(TMapp(TMapp(f, bd), TMopr("-", [i, TMint(1)])),
              TMopr("+", [TMapp(TMapp(board_get, bd), TMopr("-", [i, TMint(1)])), TMint(1)])), nsol),
        nsol)

    body = TMif0(TMopr("<", [j, TMint(8)]), when_j_lt, else_branch)

    fix = TMfix("search", "bd", TMlam("i", TMlam("j", TMlam("nsol", body))))
    return fix

search = make_search()

def empty_board():
    xs = [TMint(0) for _ in range(8)]
    return board_tuple(xs)

initial_board = empty_board()

solver = TMlet("board_get", board_get,
    TMlet("board_set", board_set,
    TMlet("safety_test1", safety_test1,
    TMlet("safety_test2", safety_test2,
    TMlet("search", search,
        TMapp(TMapp(TMapp(TMapp(TMvar("search"), initial_board), TMint(0)), TMint(0)), TMint(0))
    )))))

if __name__ == "__main__":
    print("Starting solver...\n")
    result = term_eval00(solver)
    print("\nFinished. Number of solutions found:", result.arg1)
