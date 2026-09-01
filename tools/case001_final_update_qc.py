import json
import os
import re
import subprocess
from pathlib import Path

SRC = Path('Mystery_Case_001_Final_Update.mp4')
OUT = Path('Mystery_Case_001_PRODUCTION_LOCKED_FINAL.mp4')
URL = 'https://github.com/jaytreeranch/JayTreeBooks/releases/download/mystery-case-001-qc/Mystery_Case_001_Final_Update.mp4'
EXPECTED = 'ff2c90c8ee38e93b296dc365c9021913cca6c893952e83f351504993c8c176e2'


def run(cmd, capture=False, check=True):
    print('+', ' '.join(map(str, cmd)), flush=True)
    if capture:
        p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)
        return p
    return subprocess.run(cmd, check=check)


run(['curl','-L','--fail','--retry','3','--retry-delay','2','-o',str(SRC),URL])
sha = run(['sha256sum', str(SRC)], capture=True).stdout.split()[0]
Path('source_sha256.txt').write_text(f'{sha}  {SRC.name}\n')
assert sha == EXPECTED, (sha, EXPECTED)

probe = run(['ffprobe','-v','error','-show_entries','format=filename,duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels,channel_layout','-of','json',str(SRC)], capture=True).stdout
Path('source_ffprobe.json').write_text(probe)
info = json.loads(probe)
duration = float(info['format']['duration'])

p = run(['ffmpeg','-hide_banner','-nostats','-i',str(SRC),'-filter_complex','ebur128=peak=true','-f','null','-'], capture=True, check=False)
Path('source_loudness_full.txt').write_text(p.stderr)
Path('source_loudness.txt').write_text('\n'.join(p.stderr.splitlines()[-30:])+'\n')

run(['ffmpeg','-y','-i',str(SRC),'-vf','scale=960:-2','-c:v','libx264','-preset','veryfast','-crf','30','-an','Mystery_Case_001_QC_PROXY.mp4'])
run(['ffmpeg','-y','-i',str(SRC),'-vf','fps=1/30,scale=480:-2,tile=4x3:padding=4:margin=4','-frames:v','1','full_contact_sheet.jpg'])
start = max(0.0, duration - 65.0)
run(['ffmpeg','-y','-ss',f'{start:.3f}','-i',str(SRC),'-vf','fps=1/5,scale=640:-2,tile=4x4:padding=4:margin=4','-frames:v','1','final_65s_contact_sheet.jpg'])
run(['ffmpeg','-y','-ss',f'{start:.3f}','-i',str(SRC),'-vf','fps=1/2,scale=960:-2','-q:v','3','endframe_%03d.jpg'])

with open('final_ocr.txt','w',encoding='utf-8') as out:
    for f in sorted(Path('.').glob('endframe_*.jpg')):
        out.write(f'===== {f.name} =====\n')
        q = subprocess.run(['tesseract',str(f),'stdout'],text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        out.write(q.stdout+'\n')

pass1_filter = 'acompressor=threshold=-18dB:ratio=2:attack=20:release=250,loudnorm=I=-16:TP=-1:LRA=11:print_format=json'
p = run(['ffmpeg','-hide_banner','-nostats','-i',str(SRC),'-vn','-af',pass1_filter,'-f','null','-'], capture=True, check=False)
Path('loudnorm_pass1.txt').write_text(p.stderr)
blocks = re.findall(r'\{\s*"input_i".*?\}', p.stderr, re.S)
if not blocks:
    raise RuntimeError('Could not parse loudnorm pass 1 JSON')
m = json.loads(blocks[-1])
Path('loudnorm_measured.json').write_text(json.dumps(m,indent=2)+'\n')

master_filter = (
    'acompressor=threshold=-18dB:ratio=2:attack=20:release=250,'
    'loudnorm=I=-16:TP=-1:LRA=11:'
    f'measured_I={m["input_i"]}:measured_LRA={m["input_lra"]}:'
    f'measured_TP={m["input_tp"]}:measured_thresh={m["input_thresh"]}:'
    f'offset={m["target_offset"]}:linear=true:print_format=summary'
)
Path('master_filter.txt').write_text(master_filter+'\n')
run(['ffmpeg','-y','-i',str(SRC),'-map','0:v:0','-map','0:a:0','-c:v','copy','-af',master_filter,'-c:a','aac','-b:a','320k','-movflags','+faststart',str(OUT)])

probe2 = run(['ffprobe','-v','error','-show_entries','format=filename,duration,size,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels,channel_layout','-of','json',str(OUT)], capture=True).stdout
Path('mastered_ffprobe.json').write_text(probe2)
p = run(['ffmpeg','-hide_banner','-nostats','-i',str(OUT),'-filter_complex','ebur128=peak=true','-f','null','-'], capture=True, check=False)
Path('mastered_loudness_full.txt').write_text(p.stderr)
Path('mastered_loudness.txt').write_text('\n'.join(p.stderr.splitlines()[-30:])+'\n')
sha2 = run(['sha256sum',str(OUT)], capture=True).stdout
Path('mastered_sha256.txt').write_text(sha2)
print('QC/mastering complete')
