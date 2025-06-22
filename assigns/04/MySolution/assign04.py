
##################################################################
# Assignment 4 - Task 1
#C implementation of f91 using boxed data 
# Code is in the string, can copy to C for testing.
##################################################################

'''

#include "../../../lectures/lecture-06-16/runtime.h"

extern
void*
mymalloc(size_t n) {
  void* p0;
  p0 = malloc(n);
  if (p0 != 0) return p0;
  fprintf(stderr, "myalloc failed!!!\n");
  exit(1);
}


extern
lamval1
LAMVAL_print(lamval1 x)
{
  int tag;
  tag = x->tag;
  switch( tag )
  {
    case TAGcfp:
      printf("<lamval1_cfp>"); break;
    case TAGint:
      printf("%i", ((lamval1_int)x)->data); break;
    case TAGstr:
      printf("%s", ((lamval1_str)x)->data); break;
    default: printf("Unrecognized tag = %i", tag);
  }
}


#fun f91(x: int): int =
  #if x > 100 then x-10 else f91(f91(x+11))


extern
lamval1
f91(lamval1 arg1)
{
  lamval1 ret0;
  lamval1 tmp1, tmp2, tmp3;

  tmp1 = LAMOPR_igt(arg1, LAMVAL_int(100));
  if (((lamval1_int)tmp1)->data) {
    tmp2 = LAMOPR_sub(arg1, LAMVAL_int(10));
    ret0 = tmp2;
  } else {
    tmp2 = LAMOPR_add(arg1, LAMVAL_int(11));
    tmp3 = f91(tmp2);
    ret0 = f91(tmp3);
  }

  return ret0;
}

int main() {
  LAMVAL_print(f91(LAMVAL_int(87))); printf("\n"); return 0;
}


'''

##################################################################
# Assignment 4 - Task 2
# Manual translation of isPrime 
##################################################################

def isPrime_helper(arg1, env1):
    """Helper function for isPrime.

    arg1 : int (Current divisor `p`)
    env1 : int (original number `n` passed to isPrime)
    """

    tmp1 = arg1 * arg1
    tmp2 = (tmp1 > env1)
    if tmp2:
        ret0 = True
    else:
        tmp3 = env1 % arg1
        tmp4 = (tmp3 == 0)
        if tmp4:
            ret0 = False
        else:
            tmp5 = arg1 + 1
            ret0 = isPrime_helper(tmp5, env1)
    return ret0


def isPrime(arg1):
    """Finds whether arg1 is prime number or not"""
    tmp1 = (arg1 >= 2)
    if tmp1:
        tmp2 = isPrime_helper(2, arg1)
        ret0 = tmp2
    else:
        ret0 = False
    return ret0

# Simple tests
print(isPrime(2))
print(isPrime(11))
print(isPrime(12))
print(isPrime(97))

