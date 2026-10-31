"""Retime animated WebP ANMF headers without decoding/re-encoding any artwork."""
import argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('destination',type=Path);p.add_argument('--speed',type=float,required=True);a=p.parse_args()
assert a.speed>0
b=bytearray(a.source.read_bytes());assert b[:4]==b'RIFF' and b[8:12]==b'WEBP'
pos=12;old_total=0;new_total=0;frames=0
while pos+8<=len(b):
 kind=b[pos:pos+4];size=int.from_bytes(b[pos+4:pos+8],'little')
 if kind==b'ANMF':
  at=pos+8+12;old=int.from_bytes(b[at:at+3],'little');old_total+=old
  duration=round(old_total/a.speed)-new_total;assert 0<duration<2**24
  b[at:at+3]=duration.to_bytes(3,'little');new_total+=duration;frames+=1
 pos+=8+size+(size%2)
assert pos==len(b) and frames>0
a.destination.write_bytes(b)
print(f'{frames} frames: {old_total}ms → {new_total}ms at {a.speed:g}× speed; compressed artwork unchanged')
