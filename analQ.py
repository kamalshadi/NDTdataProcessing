import sqlite3 as sq
import math
import numpy as num

dF='CSV/ndt201401.db'
D=sq.connect(dF)
cur=D.cursor()
qq="""select m,v
from
(
select cAS,SPU,avg(dr) as m,avg(dr*dr)-avg(dr)*avg(dr) as v
from
(
select cAS,SPU,upload_rate as dr
from meta
where SPU not null and SPU!=-1
)
group by cAS,SPU
)"""
cur.execute(qq)
A=cur.fetchall()
cov=[]
for m,v in A:
	cov.append(math.sqrt(v)/m)
print num.median(cov)
print num.mean(cov)
