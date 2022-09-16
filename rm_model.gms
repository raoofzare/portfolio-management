option MINLP = baron;
option optcr = 0;
option resLim = 10;

set
    i
    t;

parameter
    r(i, t)
    r1(t)
    c
    l
    u;

*$onText
$gdxIn %gdxincname%
$load i, t, r, r1, c, l, u
$gdxIn
*$offText

variable z;
binary variable delta(i);
variable x(i);
variable y(t), y1(t);

equation obj, error, mse, ceiling, wholeness, lower_bound, upper_bound, obj_lb, mse_lb;

obj..
    z =e= sum(t, y1(t));
    
obj_lb..
    sum(t, y1(t)) =g= 0;

error(t)..
    y(t) =e= (sum(i, r(i, t) * x(i)) - r1(t));
    
mse(t)..
    y1(t) =e= y(t) * y(t);
    
mse_lb(t)..
    y(t) * y(t) =g= 0;
    
ceiling..
    sum(i, delta(i)) =e= c;

wholeness..
    sum(i, x(i)) =e= 1;

lower_bound(i)..
    l * delta(i) =l= x(i);

upper_bound(i)..
    u * delta(i) =g= x(i);

model index_tracking /obj, error, mse, ceiling, wholeness, lower_bound, upper_bound, mse_lb, obj_lb/;
solve index_tracking using MINLP minimizing z;
*ms = index_tracking.modelstat;
*ss = index_tracking.solvestat;
display z.l, x.l, delta.l;
