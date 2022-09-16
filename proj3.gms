option MINLP=BARON;

set      i
         t

scalar
         l 'lower bound' /0.01/
         u 'upper bound' /0.3/
         C /15/
parameter
r(i,t)
rp(t)
;

$GDXIN %gdxincname%
$LOAD i, t, r, rp
$GDXIN

*display i, t, r, rp;

variable z;
binary variable delta(i);
nonnegative variable x(i);

equation
obj
const1
const2
const3
const4
;

obj..
         z =e= sum((t), (sum((i), r(i,t)*x(i)) - rp(t))*(sum((i), r(i,t)*x(i)) - rp(t)));

const1..
         sum((i), delta(i)) =e= C;

const2..
         sum((i), x(i)) =e= 1;

const3(i)..
         x(i) =l= u*delta(i);

const4(i)..
         x(i) =g= l*delta(i);


option optcr=0;
Option reslim=1000;
model proj3 /all/;
solve proj3 using MINLP minimizing z;
display delta.l,x.l,z.l;
