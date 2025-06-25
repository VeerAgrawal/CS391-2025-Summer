
## Final Project: Lambda-to-Python Compiler

Veer Agrawal
CS391 — Summer 2025

### Contents

* `finexam.py`: Complete compiler implementation including term extensions, compiler logic, and Python emitter.
* `README.txt`: This file.
* `midterm.py`: My midterm solution file with the 8-Queens puzzle lambda-term(used for testing)


### What I Implemented

This compiler extends the base lambda calculus interpreter taught in class and supports:

* Compilation of all 11 binary operators (`+`, `-`, `*`, `<`, `>`, `<=`, `>=`, `=`, `!=`, `cmp`)
* Tuple construction and projection (`TMtup`, `TMfst`, `TMsnd`)
* Let bindings (`TMlet`)
* Python code emission (`tcmp_pyemit`) that supports all constructs

### Testing

#### **Main Test: 8-Queens Puzzle**

This is the primary test. It checks whether the compiler correctly handles higher-order functions, recursion, tuples, and control flow. 

**Steps:**

1. Make sure both `finexam.py` and `midterm.py` are in the same directory.
2. Run `finexam.py`:

3. You should see the following output:

```
=== COMPILING 8-QUEEN LAMBDA TERM ===
=== COMPILED STACK-IR PROGRAM (tcmp) ===
=== GENERATED PYTHON CODE ===
=== EXECUTING GENERATED CODE ===
Generated solver output: 92
```

#### **Other Tests**

* 1) Binary Operator Support: Verified that the compiler handles all the binary operators
 - +, -, *, <, <=, >, >=, =, !=, cmp
* 2) Tuple creation and projection
* 3) Let-binding
* 4) Lambda + application
* 5) Nested let + tuple

All these tests are implemented via print statements at the bottom of the finexam.py file

To execute tests run finexam.py 


### Notes

* Compiler is implemented by extending the posted `lambda3.py` skeleton.
* Code adheres to the environment model (`cenv`), instruction set (`tins`), and type-driven term compilation from lecture.
* All of my code is clearly marked with `# MY CODE TASK 1` and `# MY CODE TASK 2`.

