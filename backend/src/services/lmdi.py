import math
from src.services.periods import quantities
def log_mean(a,b):
 if not math.isfinite(a) or not math.isfinite(b) or a<0 or b<0:raise ValueError("LMDI仅接受有限非负量")
 if a==0 or b==0:return 0.0
 if a==b:return a
 relative=(a-b)/b
 denominator=math.log1p(relative) if math.isfinite(relative) and relative>-1 else math.log(a)-math.log(b)
 return (a-b)/denominator
def log_ratio(a,b):
 relative=(a-b)/b
 return math.log1p(relative) if math.isfinite(relative) and relative>-1 else math.log(a)-math.log(b)
def lmdi(before,after,zones):
 q0=quantities(before);q1=quantities(after);zone_rows=[]
 for i,z in enumerate(zones):
  a=q1[i];b=q0[i]
  weight=log_mean(a,b)
  scale=weight*log_ratio(after["scale"],before["scale"])
  structure=weight*log_ratio(after["structure"][i],before["structure"][i])
  if a==0 and b==0:intensity=0.0
  elif b==0:intensity=a
  elif a==0:intensity=-b
  else:intensity=weight*log_ratio(after["intensity"][i],before["intensity"][i])
  zone_rows.append({"zone":z,"scale":scale,"structure":structure,"intensity":intensity})
 values={f:math.fsum(row[f] for row in zone_rows) for f in ("scale","structure","intensity")}
 return {"contributions":values,"residual":math.fsum(q1)-math.fsum(q0)-math.fsum(values.values()),"zones":zone_rows,"method":"按分区用水对数均值加权的加法LMDI；零用水取零极限，不添加微小量"}
