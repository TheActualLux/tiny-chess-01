import os,json,sys,urllib.request as u
U=os.environ["MAKEFUN_ENV_URL"]
def P(p,b):
 r=u.Request(U+p,json.dumps(b).encode(),{"content-type":"application/json"});return json.load(u.urlopen(r))
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':0}
W=[0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,5,5,10,15,15,10,5,5,0,0,5,10,10,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
N=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
K=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
R=[(0,1),(0,-1),(1,0),(-1,0)]
B=[(1,1),(1,-1),(-1,1),(-1,-1)]
def sq(s):return ord(s[0])-97+8*(int(s[1])-1)
def fen(f):
 b=['.']*64
 for i,r in enumerate(f.split()[0].split('/')):
  x=0
  for c in r:
   if c.isdigit():x+=int(c)
   else:b[x+8*(7-i)]=c;x+=1
 return b
def mv(b,m,epf,w):
 f,t=m[0],m[1];p=b[f];b[f]='.'
 if p.lower()=='p' and b[t]=='.' and abs(t-f) in(7,9):j=t+(-8 if w else 8);b[j if 0<=j<64 else f]='.'
 b[t]=m[2] if len(m)>2 else p
 if p.lower()=='k' and abs(t-f)==2:
  r=t+(1 if t>f else -2);d=t+(-1 if t>f else 1);b[d]=b[r];b[r]='.'
 return b
def gen(b,w,epf,c):
 o=[]
 for i in range(64):
  p=b[i]
  if p=='.' or p.isupper()!=w:continue
  l=p.lower();f,r=i%8,i//8
  if l=='p':
   d=1 if w else -1;j=i+8*d
   if 0<=j<64 and b[j]=='.':
    if r+d in(0,7):o+=[(i,j,x) for x in'qrbn']
    else:o.append((i,j))
    if r in(1,6) and 0<=i+16*d<64 and b[i+16*d]=='.':o.append((i,i+16*d))
   for x in(-1,1):
    if 0<=f+x<8 and 0<=r+d<8:
     j=(r+d)*8+f+x
     if (b[j]!='.' and b[j].isupper()!=w) or j==epf:
      if r+d in(0,7):o+=[(i,j,y) for y in'qrbn']
      else:o.append((i,j))
  elif l in'nk':
   for dr,df in(N if l=='n' else K):
    f2,r2=f+df,r+dr
    if 0<=f2<8 and 0<=r2<8:
     j=f2+8*r2
     if b[j]=='.' or b[j].isupper()!=w:o.append((i,j))
  else:
   for dr,df in(R if l=='r' else B if l=='b' else R+B):
    f2,r2=f+df,r+dr
    while 0<=f2<8 and 0<=r2<8:
     j=f2+8*r2
     if b[j]!='.':
      if b[j].isupper()!=w:o.append((i,j))
      break
     o.append((i,j));f2+=df;r2+=dr
 if w and b[4]=='K' and b[7]=='R' and b[5]==b[6]=='.' and 'K' in c:o.append((4,6))
 if w and b[4]=='K' and b[0]=='R' and b[1]==b[2]==b[3]=='.' and 'Q' in c:o.append((4,2))
 if not w and b[60]=='k' and b[63]=='r' and b[61]==b[62]=='.' and 'k' in c:o.append((60,62))
 if not w and b[60]=='k' and b[56]=='r' and b[57]==b[58]==b[59]=='.' and 'q' in c:o.append((60,58))
 return o
def ev(b):
 s=0
 for i,p in enumerate(b):
  if p!='.':
   v=V[p.lower()]+W[i if p.isupper() else 63-i]
   s+=v if p.isupper() else -v
 return s
def chk(b,w):
 k=b.index('K' if w else 'k')
 return any(m[1]==k for m in gen(b,not w,-1,'-'))
nt=[0]
def qs(b,w,epf,c,a,be,q):
 s=ev(b)
 if q<1 or s>=be:return s
 if s>a:a=s
 for m in gen(b,w,epf,c):
  if b[m[1]]=='.' and len(m)<3:continue
  nb=mv(b[:],m,epf,w)
  if chk(nb,w):continue
  v=-qs(nb,not w,-1,c,-be,-a,q-1)
  if v>s:s=v
  if s>a:a=s
  if a>=be:break
 return s
def ab(b,w,epf,c,d,a,be):
 nt[0]+=1
 if d<1 or nt[0]>150000:return qs(b,w,epf,c,a,be,2)
 sc=-99999
 for m in gen(b,w,epf,c):
  nb=mv(b[:],m,epf,w)
  if chk(nb,w):continue
  v=-ab(nb,not w,-1,c,d-1,-be,-a)
  if v>sc:sc=v
  if sc>a:a=sc
  if a>=be:break
 return sc
def pick(f,lm):
 b=fen(f);w=f.split()[1]=='w'
 epf=sq(f.split()[3]) if f.split()[3]!='-' else -1;c=f.split()[2]
 best=lm[0];bs=-99999
 for s in lm:
  m=(sq(s[:2]),sq(s[2:4]))+((s[4],) if len(s)>4 else ())
  v=-ab(mv(b[:],m,epf,w),not w,-1,c,2,-99999,99999)
  if v>bs:bs=v;best=s
 return best
g=P('/game',{})
while g.get('status')!='done':
 if g.get('status')=='your_move':P('/move',{'game':g['game'],'move':pick(g['fen'],g['legal_moves'])})
 g=P('/game',{})
