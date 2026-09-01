import json
import re
import subprocess
from pathlib import Path

SRC=Path('Mystery_Case_001_Final_Update.mp4')
OUT=Path('Mystery_Case_001_PRODUCTION_LOCKED_FINAL.mp4')
URL='https://github.com/jaytreeranch/JayTreeBooks/releases/download/mystery-case-001-qc/Mystery_Case_001_Final_Update.mp4'
EXPECTED='ff2c90c8ee38e93b296dc365c9021913cca6c893952e83f351504993c8c176e2'


def run(cmd,capture=False,check=True):
    print('+',' '.join(map(str,cmd)),flush=True)
    return subprocess.run(cmd,text=True,stdout=subprocess.PIPE if capture else None,stderr=subprocess.PIPE if capture else None,check=check)

run(['curl','-L','--fail','--retry','3','-o',str(SRC),URL])
sha=run(['sha256sum',str(SRC)],capture=True).stdout.split()[0]
assert sha==EXPECTED,(sha,EXPECTED)

p=run(['ffmpeg','-hide_banner','-nostats','-i',str(SRC),'-vn','-af','acompressor=threshold=-18dB:ratio=2:attack=20:release=250,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture=True,check=False)
blocks=re.findall(r'\{\s*"input_i".*?\}',p.stderr,re.S)
if not blocks: raise RuntimeError('No loudnorm JSON')
m=json.loads(blocks[-1])
Path('master_pass1.json').write_text(json.dumps(m,indent=2)+'\n')
flt=('acompressor=threshold=-18dB:ratio=2:attack=20:release=250,'
     'loudnorm=I=-16:TP=-1.5:LRA=11:'
     f'measured_I={m["input_i"]}:measured_LRA={m["input_lra"]}:'
     f'measured_TP={m["input_tp"]}:measured_thresh={m["input_thresh"]}:'
     f'offset={m["target_offset"]}:linear=true:print_format=summary')
run(['ffmpeg','-y','-i',str(SRC),'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',flt,'-c:a','aac','-b:a','320k','-movflags','+faststart',str(OUT)])

p=run(['ffmpeg','-hide_banner','-nostats','-i',str(OUT),'-filter_complex','ebur128=peak=true','-f','null','-'],capture=True,check=False)
Path('final_loudness_full.txt').write_text(p.stderr)
Path('final_loudness.txt').write_text('\n'.join(p.stderr.splitlines()[-30:])+'\n')
probe=run(['ffprobe','-v','error','-show_entries','format=filename,duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels,channel_layout','-of','json',str(OUT)],capture=True).stdout
Path('final_ffprobe.json').write_text(probe)
Path('final_sha256.txt').write_text(run(['sha256sum',str(OUT)],capture=True).stdout)

mi=re.search(r'Integrated loudness:\s*\n\s*I:\s*([-0-9.]+) LUFS',p.stderr)
mt=re.search(r'True peak:\s*\n\s*Peak:\s*([-0-9.]+) dBFS',p.stderr)
if not (mi and mt): raise RuntimeError('Could not parse final EBU report')
i=float(mi.group(1)); tp=float(mt.group(1))
print('FINAL I',i,'FINAL TP',tp)
if not (-16.4 <= i <= -15.6): raise RuntimeError(f'Integrated loudness out of range: {i}')
if tp > -0.9: raise RuntimeError(f'True peak too hot: {tp}')
