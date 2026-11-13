import math
def prepare(rows,before,after):
 def period(name):
  selected=[r for r in rows if r.get("period")==name]
  if not selected:raise ValueError("月份没有观测："+name)
  zones=[];data={}
  for row in selected:
   for key in ("zone","period","scale","water"):
    if key not in row or row[key] is None:raise ValueError("存在缺测字段："+key+"；缺测不能用零值代替")
   zone=row["zone"]
   if zone in data:raise ValueError("月份内分区重复")
   try:scale=float(row["scale"]);water=float(row["water"])
   except (TypeError,ValueError):raise ValueError("规模与用水必须是数值")
   if not math.isfinite(scale) or scale<=0:raise ValueError("规模必须为有限正值，零值不能用epsilon替换")
   if not math.isfinite(water) or water<0:raise ValueError("用水必须为有限非负值；真实零值可用，缺测和负值拒绝")
   data[zone]={"zone":zone,"period":row["period"],"scale":scale,"water":water};zones.append(zone)
  return data
 a=period(before);b=period(after)
 if set(a)!=set(b):raise ValueError("两期分区不一致，禁止补零或静默丢弃分区")
 zones=sorted(a)
 def factors(data):
  total=math.fsum(r["scale"] for r in data.values())
  shares=[data[z]["scale"]/total for z in zones];intensities=[data[z]["water"]/data[z]["scale"] for z in zones]
  if not math.isfinite(total) or any(not math.isfinite(x) for x in shares+intensities):raise ValueError("量纲超出有限数值范围，请核查输入")
  return {"scale":total,"structure":shares,"intensity":intensities}
 return zones,factors(a),factors(b)
def quantities(factors):return [factors["scale"]*w*i for w,i in zip(factors["structure"],factors["intensity"])]
