import os,json,time,urllib.request as u
U=os.environ["MAKEFUN_ENV_URL"]
def P(p,b):return json.load(u.urlopen(u.Request(U+p,json.dumps(b).encode(),{"content-type":"application/json"})))
V=dict(zip('.pnbrqk',(0,100,320,330,500,900,0)))
Z=dict(zip('pnbrqk',(1,3,2,0,1,-2)))
W=[(7-abs(i%8*2-7))*(7-abs(i//8*2-7))//4 for i in range(64)]
N=[(a,c)for a in(-2,-1,1,2)for c in(-2,-1,1,2)if abs(a)!=abs(c)]
R=[(0,1),(0,-1),(1,0),(-1,0)]
B=[(1,1),(1,-1),(-1,1),(-1,-1)]
K=R+B
def sq(s):return ord(s[0])-105+8*int(s[1])
def fen(f):
 b=[]
 for r in f.split()[0].split('/')[::-1]:
  for c in r:b+=['.']*int(c)if c<'A'else[c]
 return b+[-1]
def mv(b,m,e,w):
 f,t=m[0],m[1];p=b[f];l=p.lower();b[f]='.';b[64]=-1
 if l=='p':
  if b[t]=='.'and(t-f)%8:b[t-8+16*(1-w)]='.'
  if abs(t-f)==16:b[64]=f+t>>1
 b[t]=(m[2].upper()if w else m[2])if len(m)>2 else p
 if l=='k'and abs(t-f)==2:r=t+(1 if t>f else -2);b[f+t>>1]=b[r];b[r]='.'
 return b
def at(b,k,w):
 f,r=k%8,k//8;d=1 if w else -1
 for D,t in((N,'n'),(R,'rq'),(B,'bq')):
  for y,x in D:
   F,G,s=f+x,r+y,D!=N
   while 0<=F<8 and 0<=G<8:
    p=b[F+8*G]
    if p!='.':
     l=p.lower()
     if(p>'Z')==w and(l in t or s and(l=='k'or l=='p'and D==B and y==d)):return 1
     break
    if D==N:break
    F+=x;G+=y;s=0
 return 0
def chk(b,w):return at(b,b.index('kK'[w]),w)
def gen(b,w,e,c):
 o=[];e=max(e,b[64])
 for i in range(64):
  p=b[i]
  if p=='.'or(p<'a')!=w:continue
  l=p.lower();f,r=i%8,i//8
  if l=='p':
   d=8 if w else -8;j=i+d;Q=j//8 in(0,7)
   if b[j]=='.':
    o+=[(i,j,x)for x in'qrbn']if Q else[(i,j)]
    if r==(1 if w else 6)and b[j+d]=='.':o+=[(i,j+d)]
   for x in(-1,1):
    j=i+d+x
    if 0<=f+x<8 and(b[j]!='.'and(b[j]<'a')!=w or j==e):o+=[(i,j,y)for y in'qrbn']if Q else[(i,j)]
  else:
   for y,x in{'n':N,'r':R,'b':B}.get(l,K):
    F,G=f+x,r+y
    while 0<=F<8 and 0<=G<8:
     j=F+8*G;q=b[j]
     if q=='.'or(q<'a')!=w:o+=[(i,j)]
     if q!='.'or l in'nk':break
     F+=x;G+=y
 for k,q,F,x in((4,7,'K',5),(4,0,'Q',3),(60,63,'k',61),(60,56,'q',59)):
  if F in c and(F<'a')==w and b[k]+b[q]==('KR'if w else'kr')and all(b[j]=='.'for j in range(min(k,q)+1,max(k,q)))and not(at(b,k,w)or at(b,x,w)):o+=[(k,2*x-k)]
 return o
def ev(b):
 s=0
 for i in range(64):
  p=b[i]
  if p>'.':
   l=p.lower();j=i if p<'a'else 63-i;v=V[l]+W[i]*Z[l]+(l=='p')*(j//8)**2*2
   s+=v if p<'a'else -v
 return s
def og(b,w,e):return sorted(gen(b,w,e,'-'),key=lambda m:V[b[m[0]].lower()]-10*V[b[m[1]].lower()]-800*(len(m)>2))
n=[0,0,0]
def qs(b,w,a,z,q):
 n[0]+=1;s=ev(b)*(1 if w else -1)
 if s>=z or q<1:return s
 a=max(a,s)
 for m in og(b,w,-1):
  if b[m[1]]=='.'and len(m)<3:continue
  c=mv(b[:],m,-1,w)
  if chk(c,w):continue
  v=-qs(c,not w,-z,-a,q-1);s=max(s,v);a=max(a,v)
  if a>=z:break
 return s
def ab(b,w,d,a,z,p):
 n[0]+=1
 if n[0]>n[1]or time.time()>n[2]:raise StopIteration
 if d<1:return qs(b,w,a,z,6)
 s=-99999
 for m in og(b,w,-1):
  c=mv(b[:],m,-1,w)
  if chk(c,w):continue
  v=-ab(c,not w,d-1,-z,-a,p+1);s=max(s,v);a=max(a,v)
  if a>=z:break
 return s if s>-99999 else p-30000 if chk(b,w)else 0
def pick(f,L,ms):
 S=f.split();b=fen(f);w=S[1]=='w';e=sq(S[3])if S[3]!='-'else-1
 M=[(s,(sq(s[:2]),sq(s[2:4]))+tuple(s[4:]))for s in L];best=L[0]
 n[:]=0,300000,time.time()+min(ms/2500,8)
 try:
  for d in range(5):
   a=-99999;T=[]
   for s,m in M:
    v=-ab(mv(b[:],m,e,w),not w,d,-99999,-a,1);T+=[(v,s,m)]
    if v>a:a=v;best=s
   M=[x[1:]for x in sorted(T,key=lambda x:-x[0])]
   if a>29000:break
 except StopIteration:pass
 return best
g=P('/game',{})
while g.get('status')!='done':
 try:
  if g.get('status')=='your_move':P('/move',{'game':g['game'],'move':pick(g['fen'],g['legal_moves'],g.get('move_limit_ms',9000))})
  else:time.sleep(.2)
 except Exception:time.sleep(.5)
 g=P('/game',{})
