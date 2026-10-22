"""Reina Explains AI — pipeline satu perintah.

  python run.py check  episodes/epXX.py                 # validasi + render semua keyframe (cepat)
  python run.py stage1 episodes/epXX.py                 # storyboard.md + gambar scene + prompt VO + zip
  python run.py stage2 episodes/epXX.py suara.zip       # potong jeda, sinkron, SFX, render video + zip final
        opsi stage2: --preview 8   (render 8 detik pertama saja untuk cek cepat)
                     --speed 1.10  --cap 0.20  (tempo & maks jeda di dalam baris)

Jalankan dari folder kit (folder yang berisi run.py). Output ke out/epXX/.
"""
import os, sys, json, glob, shutil, subprocess, zipfile, time, re, textwrap, argparse
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import reina as RE
import docs, sfx as SFX

def P(sz, w='Bold'): return ImageFont.truetype(os.path.join(RE.A, 'fonts', f'Poppins-{w}.ttf'), sz)

def load(ep_file): return RE.load_episode(ep_file, ROOT)

def outdir(E):
    d = os.path.join(ROOT, 'out', E.tag); os.makedirs(d, exist_ok=True); return d

# ---------------- checks ----------------
def validate(E):
    m = E.m; errs = []
    for s in E.shots:
        sid = s['id']
        if sid not in m.POSE: errs.append(f'{sid}: tidak ada di POSE')
        elif m.POSE[sid] not in RE.POSES['poses']: errs.append(f"{sid}: pose '{m.POSE[sid]}' tidak ada (pilihan: {', '.join(RE.POSES['poses'])})")
        sp = m.spec(sid)
        for k in ('goal', 'obj', 'anim', 'text', 'sfx', 'qa'):
            if k not in sp: errs.append(f'{sid}: spec tanpa {k}')
        for c in sp.get('sfx', []):
            if c[1] not in SFX.LIB: errs.append(f"{sid}: SFX '{c[1]}' tidak dikenal (pilihan: {', '.join(SFX.LIB)})")
    used = sorted({li for _, _, _, ls, _, _ in m.SHOTS for li in ls})
    if used != list(range(1, len(m.LINES) + 1)): errs.append(f'baris dipakai {used} ≠ 1..{len(m.LINES)} (tiap baris harus dipakai tepat sekali, berurutan)')
    for l in E.lines:
        if len(l['text']) > 140: errs.append(f"{l['id']}: baris terlalu panjang ({len(l['text'])} karakter) — pecah jadi 2 baris")
    return errs

# ---------------- images ----------------
def keyframes(E, d):
    kd = os.path.join(d, 'keyframes'); os.makedirs(kd, exist_ok=True)
    for s in E.shots: E.frame(E.keys[s['id']]).save(os.path.join(kd, f"{s['id']}.png"))
    return kd
def sheets(E, d):
    kd = os.path.join(d, 'keyframes'); PW, PH, PAD = 432, 768, 40; files = []
    for sc in sorted(E.m.SCENES):
        shots = [s for s in E.shots if s['scene'] == sc]
        if not shots: continue
        Wd = max(1180, PAD + len(shots) * (PW + PAD)); im = Image.new('RGB', (Wd, 1168), '#F6F1E7'); dr = ImageDraw.Draw(im)
        dr.text((PAD, 34), f'SCENE {sc} — {E.m.SCENES[sc]}', font=P(50), fill='#1E2A4A')
        a, b = shots[0]['start'], shots[-1]['end']
        dr.text((PAD, 104), f'{RE.tc(a)[3:]} – {RE.tc(b)[3:]}  ·  {b - a:.1f} s  ·  Reina Explains AI Ep.{E.ep:02d}', font=P(26, 'Medium'), fill='#5A6684')
        for i, s in enumerate(shots):
            x = PAD + i * (PW + PAD); y = 150
            k = Image.open(os.path.join(kd, f"{s['id']}.png")).resize((PW, PH), Image.LANCZOS)
            dr.rounded_rectangle([x - 4, y - 4, x + PW + 3, y + PH + 3], 14, outline='#1E2A4A', width=4); im.paste(k, (x, y))
            yy = y + PH + 16
            dr.text((x, yy), s['id'], font=P(38), fill='#3F6FC9')
            dr.text((x + 100, yy + 10), f"{RE.tc(s['start'])[3:]}–{RE.tc(s['end'])[3:]} ({s['end'] - s['start']:.1f}s)", font=P(22, 'Medium'), fill='#5A6684')
            dr.text((x, yy + 58), f"keyframe t={E.keys[s['id']]:.2f}s · {', '.join(s['lines']) or '-'}", font=P(20, 'Regular'), fill='#5A6684')
            for j, l in enumerate(textwrap.wrap(s['title'], 32)[:2]): dr.text((x, yy + 90 + j * 32), l, font=P(26, 'Medium'), fill='#1E2A4A')
        fn = re.sub(r'[^a-z0-9]+', '_', E.m.SCENES[sc].lower()).strip('_')
        p = os.path.join(d, f'{E.tag}_scene{sc}_{fn}.png'); im.save(p); files.append(p)
    return files

def write_docs(E, d, final):
    sb = os.path.join(d, f'{E.tag}_storyboard.md'); open(sb, 'w').write(docs.storyboard_md(E, final))
    vp = os.path.join(d, f'{E.tag}_vo_prompt.md'); open(vp, 'w').write(docs.vo_prompt_md(E))
    return sb, vp

def pack(E, d, name, files, ep_file):
    z = os.path.join(d, name)
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in files: zf.write(f, os.path.relpath(f, d))
        for f in sorted(glob.glob(os.path.join(d, 'keyframes', '*.png'))): zf.write(f, os.path.relpath(f, d))
        zf.write(ep_file, f'episode/{os.path.basename(ep_file)}')
    return z

# ---------------- audio ----------------
def _load_wav(p):
    """Baca audio apa pun (wav/mp3/m4a) → mono float 48k via ffmpeg."""
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '48000', '-f', 's16le', '-'])
    return np.frombuffer(raw, np.int16).astype(float) / 32768
def _save_wav(p, x, sr=48000):
    import wave
    w = wave.open(p, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
def _db(x, hop):
    n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-12)

def collect_voice(src, E):
    """Kembalikan {L01: path,...}. Terima zip / folder berisi L01.wav… atau satu file utuh (dipecah otomatis per jeda)."""
    work = os.path.join(E.audio_dir, 'src'); shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
    if os.path.isfile(src) and src.lower().endswith('.zip'):
        zipfile.ZipFile(src).extractall(work); base = work
    elif os.path.isdir(src): base = src
    else: base = None
    n = len(E.lines); found = {}
    if base:
        for p in glob.glob(os.path.join(base, '**', '*'), recursive=True):
            mm = re.search(r'(?:^|[^0-9])L(\d{2})[^0-9]*\.(wav|mp3|m4a|ogg|flac)$', os.path.basename(p), re.I)
            if mm and os.path.isfile(p): found[f'L{int(mm.group(1)):02d}'] = p
        if len(found) >= n: return {k: found[k] for k in sorted(found) if int(k[1:]) <= n}
        singles = [p for p in glob.glob(os.path.join(base, '**', '*'), recursive=True) if re.search(r'\.(wav|mp3|m4a|ogg|flac)$', p, re.I)]
        if len(singles) != 1: raise SystemExit(f'Butuh L01..L{n:02d} (ketemu {len(found)}) atau satu file audio utuh.')
        src = singles[0]
    # satu file utuh: potong di N-1 jeda terpanjang
    x = _load_wav(src); hop = 480; db = _db(x, hop); sp = db > -40
    runs = []; s = None
    for j, v in enumerate(sp):
        if not v and s is None: s = j
        if v and s is not None: runs.append((s, j)); s = None
    first = np.argmax(sp); last = len(sp) - np.argmax(sp[::-1])
    runs = [r for r in runs if r[0] > first and r[1] < last]
    if len(runs) < n - 1: raise SystemExit(f'Hanya ketemu {len(runs) + 1} potongan suara, butuh {n}. Kirim per baris (L01.wav…).')
    cuts = sorted(sorted(runs, key=lambda r: r[1] - r[0], reverse=True)[:n - 1])
    bounds = [0] + [(a + b) // 2 for a, b in cuts] + [len(sp)]; out = {}
    for i in range(n):
        p = os.path.join(work, f'L{i + 1:02d}.wav'); _save_wav(p, x[bounds[i] * hop:bounds[i + 1] * hop]); out[f'L{i + 1:02d}'] = p
    print('  file utuh dipecah jadi', n, 'baris (cek subtitle vs suara di preview!)')
    return out

def prep_voice(files, E, speed=1.10, cap=0.20):
    """Per baris: buang hening awal/akhir, jeda internal maks `cap` s, lalu atempo `speed`."""
    durs = {}; sr = 48000; hop = sr // 100
    for lid, p in files.items():
        x = _load_wav(p); db = _db(x, hop); sp = db > -40; idx = np.where(sp)[0]
        if not len(idx): raise SystemExit(f'{lid}: tidak ada suara')
        a = max(0, idx[0] - 4); b = min(len(sp), idx[-1] + 6); runs = []; s = None
        for j in range(a, b):
            if not sp[j] and s is None: s = j
            if sp[j] and s is not None: runs.append((s, j)); s = None
        cur = a; segs = []
        for s0, s1 in runs:
            if (s1 - s0) / 100 > cap: mcap = int(cap * 100 / 2); segs.append((cur, s0 + mcap)); cur = s1 - mcap
        segs.append((cur, b)); fade = int(0.008 * sr); parts = []
        for s0, s1 in segs:
            seg = x[s0 * hop:s1 * hop].copy(); rmp = np.linspace(0, 1, fade); seg[:fade] *= rmp; seg[-fade:] *= rmp[::-1]; parts.append(seg)
        tmp = os.path.join(E.audio_dir, f'{lid}_trim.wav'); _save_wav(tmp, np.concatenate(parts))
        outp = os.path.join(E.audio_dir, f'{lid}.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-filter:a', f'atempo={speed}', '-ar', '48000', '-ac', '1', outp], check=True)
        durs[lid] = len(_load_wav(outp)) / sr
        print(f'  {lid}: {len(x) / sr:.2f}s → {durs[lid]:.2f}s')
    json.dump(durs, open(os.path.join(E.audio_dir, 'durs.json'), 'w'), indent=1)
    return durs

def build_audio(E):
    """VO di posisi timeline + SFX dari spec → mix.wav; env.json untuk lip sync (dari VO saja)."""
    SR = 48000; y = np.zeros(int((E.total + 1.5) * SR))
    for l in E.lines:
        x = _load_wav(os.path.join(E.audio_dir, f"{l['id']}.wav")); a = int(l['start'] * SR); y[a:a + len(x)] += x
    pk = np.abs(y).max(); y = y / pk * 0.89 if pk > 0 else y
    hop = SR // 100; env = _db(y, hop)
    json.dump(dict(env_db=np.maximum(env, -120).round(2).tolist(), hop=0.01), open(os.path.join(E.audio_dir, 'env.json'), 'w'))
    cues = []
    for s in E.shots:
        for tt, key, dur, db, _ in E.m.spec(s['id'])['sfx']: cues.append((s['start'] + max(0, tt), key, dur, db))
    fx = SFX.render(cues, E.total)[:len(y)]
    mix = y + fx; pk = np.abs(mix).max(); mix = mix / pk * 0.95 if pk > 0.95 else mix
    mix = mix[:int(E.total * SR)]
    p = os.path.join(E.audio_dir, 'mix.wav'); _save_wav(p, mix); return p, len(cues)

# ---------------- video ----------------
_W = {}
def _init(ep_file): _W['E'] = load(ep_file)
def _job(i): return _W['E'].frame(i / RE.FPS).tobytes()
def render_video(E, ep_file, audio, out, seconds=None):
    from multiprocessing import Pool
    N = round((seconds or E.total) * RE.FPS); tmp = out + '.noaudio.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30',
                           '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    t0 = time.time()
    with Pool(os.cpu_count() or 2, initializer=_init, initargs=(ep_file,)) as p:
        for i, b in enumerate(p.imap(_job, range(N), chunksize=8)):
            ff.stdin.write(b)
            if i % 300 == 0: print(f'  frame {i}/{N}  {time.time() - t0:.0f}s', flush=True)
    ff.stdin.close(); ff.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', audio, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                    '-movflags', '+faststart', out], check=True)
    os.remove(tmp); print(f'  video selesai {time.time() - t0:.0f}s → {out}')

# ---------------- stages ----------------
def stage1(ep_file):
    E = load(ep_file); errs = validate(E)
    if errs: raise SystemExit('VALIDASI GAGAL:\n- ' + '\n- '.join(errs))
    d = outdir(E); shutil.rmtree(os.path.join(d, 'keyframes'), ignore_errors=True)
    print(f'{E.tag}: {len(E.shots)} shot, {len(E.lines)} baris, estimasi {E.total:.1f} s')
    keyframes(E, d); sh = sheets(E, d); sb, vp = write_docs(E, d, final=False)
    z = pack(E, d, f'{E.tag}_stage1_storyboard.zip', [sb, vp] + sh, ep_file)
    print('OUTPUT:', sb, vp, *sh, z, sep='\n  ')

def stage2(ep_file, voice, preview=None, speed=1.10, cap=0.20):
    E = load(ep_file); os.makedirs(E.audio_dir, exist_ok=True)
    files = collect_voice(voice, E); prep_voice(files, E, speed, cap)
    E = load(ep_file)                      # timeline ulang dari durasi rekaman
    mix, nfx = build_audio(E); E = load(ep_file)   # muat env.json untuk lip sync
    print(f'{E.tag}: durasi final {E.total:.2f} s, {nfx} SFX')
    d = outdir(E)
    if preview:
        out = os.path.join(d, f'reina_{E.tag}_preview.mp4'); render_video(E, ep_file, mix, out, preview); return
    shutil.rmtree(os.path.join(d, 'keyframes'), ignore_errors=True)
    keyframes(E, d); sh = sheets(E, d); sb, vp = write_docs(E, d, final=True)
    out = os.path.join(d, f'reina_{E.tag}.mp4'); render_video(E, ep_file, mix, out)
    z = pack(E, d, f'{E.tag}_final_pack.zip', [sb, vp] + sh, ep_file)
    print('OUTPUT:', out, z, sep='\n  ')

def check(ep_file):
    E = load(ep_file); errs = validate(E)
    d = outdir(E); keyframes(E, d); sheets(E, d)
    print('VALIDASI:', 'OK' if not errs else '\n- ' + '\n- '.join(errs)); print('keyframe & sheet →', d)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('episode'); ap.add_argument('voice', nargs='?')
    ap.add_argument('--preview', type=float); ap.add_argument('--speed', type=float, default=1.10); ap.add_argument('--cap', type=float, default=0.20)
    a = ap.parse_args(); a.episode = os.path.abspath(a.episode); a.voice = os.path.abspath(a.voice) if a.voice else None; os.chdir(ROOT)
    if a.cmd == 'stage1': stage1(a.episode)
    elif a.cmd == 'stage2': stage2(a.episode, a.voice, a.preview, a.speed, a.cap)
    elif a.cmd == 'check': check(a.episode)
    else: raise SystemExit(__doc__)
