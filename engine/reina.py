"""Reina Explains AI — render engine (tema "clean": flat vector di atas latar kantor blur).

Setiap frame adalah fungsi murni dari waktu: frame(t) -> PIL.Image 1080x1920.
Episode ditulis sebagai file Python di episodes/epXX.py (lihat episodes/ep06.py) lalu dimuat
lewat load_episode(path). Semua helper gambar memakai koordinat PERSEN kanvas (0..100),
ukuran font/radius dalam px pada 1080x1920. Grafis digambar 2x (SS) lalu di-downsample.
"""
import os, json, math, re, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(KIT, 'assets')
W, H, FPS, SS = 1080, 1920, 30, 2

# ---------------- palette ----------------
F = dict(bg='#F6F1E7', bg2='#EDE5D6', ink='#1E2A4A', ink2='#5A6684', blue='#3F6FC9', blue2='#A9C1F2',
         coral='#FF7A59', yellow='#FFC94A', mint='#4FC3A1', lilac='#A993F2', white='#FFFFFF', red='#E5484D',
         green='#2FB37A', gray='#C9C2B4')
CHIPC = [F['blue'], F['coral'], F['yellow'], F['mint'], F['lilac']]
def rgba(h, a=255):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (int(max(0, min(255, a))),)

# ---------------- easing ----------------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def lerp(a, b, x): return a + (b - a) * x
def ease_out_cubic(x): return 1 - (1 - x) ** 3
def ease_inout_cubic(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def ease_out_back(x, s=1.70158): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2

# ---------------- fonts ----------------
_FC = {}
def font(size, w='Bold'):
    w = {'SemiBold': 'Medium'}.get(w, w); k = (size, w)
    if k not in _FC: _FC[k] = ImageFont.truetype(os.path.join(A, 'fonts', f'Poppins-{w}.ttf'), int(size * SS))
    return _FC[k]

# ---------------- 2x drawing primitives ----------------
def X(p): return p * W * SS / 100
def Y(p): return p * H * SS / 100
def canvas(): return Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
def rr(im, box, r=24, fill=None, outline=None, w=0, a=255):
    """Rounded rect. box=(x0,y0,x1,y1) in %."""
    d = ImageDraw.Draw(im); x0, y0, x1, y1 = box
    x0, x1 = sorted((X(x0), X(x1))); y0, y1 = sorted((Y(y0), Y(y1)))
    if x1 - x0 < 2 or y1 - y0 < 2: return
    rad = min(r * SS, (x1 - x0) / 2, (y1 - y0) / 2)
    d.rounded_rectangle([x0, y0, x1, y1], rad, fill=rgba(fill, a) if fill else None,
                        outline=rgba(outline, a) if outline else None, width=int(w * SS))
def card(im, box, fill=F['white'], r=28, a=255, shadow=True, outline=None):
    if shadow: rr(im, (box[0], box[1] + 0.45, box[2], box[3] + 0.45), r, F['ink'], a=a * 0.13)
    rr(im, box, r, fill, outline=outline, w=4 if outline else 0, a=a)
def circ(im, cx, cy, r, fill, a=255, outline=None, w=0):
    d = ImageDraw.Draw(im); R_ = r * SS
    d.ellipse([X(cx) - R_, Y(cy) - R_, X(cx) + R_, Y(cy) + R_], fill=rgba(fill, a) if fill else None,
              outline=rgba(outline, a) if outline else None, width=int(w * SS))
def ell(im, cx, cy, rx, ry, fill, a=255):
    ImageDraw.Draw(im).ellipse([X(cx) - rx * SS, Y(cy) - ry * SS, X(cx) + rx * SS, Y(cy) + ry * SS], fill=rgba(fill, a))
def txt(im, s, xy, size, fill=F['ink'], w='Bold', anchor='mm', a=255, spacing=10):
    ImageDraw.Draw(im).multiline_text((X(xy[0]), Y(xy[1])), s, font=font(size, w), fill=rgba(fill, a), anchor=anchor,
                                      align='center' if anchor[0] == 'm' else ('left' if anchor[0] == 'l' else 'right'),
                                      spacing=spacing * SS)
def tw_px(s, size, w='Bold'):
    b = font(size, w).getbbox(s); return (b[2] - b[0]) / SS
def line(im, x0, y0, x1, y1, col, w=6, a=255):
    ImageDraw.Draw(im).line([X(x0), Y(y0), X(x1), Y(y1)], fill=rgba(col, a), width=int(w * SS))
def arrow(im, x0, y0, x1, y1, k=1.0, col=F['ink'], w=7, a=255):
    if k <= 0: return
    xe, ye = lerp(x0, x1, k), lerp(y0, y1, k)
    line(im, x0, y0, xe, ye, col, w, a)
    ang = math.atan2(Y(ye) - Y(y0), X(xe) - X(x0)); L = 22 * SS
    pts = [(X(xe), Y(ye)), (X(xe) - L * math.cos(ang - 0.5), Y(ye) - L * math.sin(ang - 0.5)),
           (X(xe) - L * math.cos(ang + 0.5), Y(ye) - L * math.sin(ang + 0.5))]
    ImageDraw.Draw(im).polygon(pts, fill=rgba(col, a))
def poly(im, pts, fill, a=255):
    ImageDraw.Draw(im).polygon([(X(x), Y(y)) for x, y in pts], fill=rgba(fill, a))
def chip(im, s, cx, cy, col, size=40, a=255, tcol=None):
    """Pill berisi teks, lebar mengikuti teks. Return lebar dalam %."""
    wp = (tw_px(s, size) + 44) / W * 100; hp = (size * 1.55) / H * 100
    rr(im, (cx - wp / 2, cy - hp / 2 + 0.3, cx + wp / 2, cy + hp / 2 + 0.3), 18, F['ink'], a=a * 0.18)
    rr(im, (cx - wp / 2, cy - hp / 2, cx + wp / 2, cy + hp / 2), 18, col, a=a)
    txt(im, s, (cx, cy), size, tcol or (F['ink'] if col in (F['yellow'], F['blue2'], F['white']) else F['white']), 'Medium', a=a)
    return wp
def chip_row(im, pieces, cy, size=40, gap=1.6, k=1.0, a=255, x_mid=50, cols=None, spread=1.0):
    """Deretan chip. k 0..1 = progres muncul berurutan; spread 0 = rapat, 1 = terpisah."""
    ws = [(tw_px(p, size) + 44) / W * 100 for p in pieces]
    g = gap * spread; tot = sum(ws) + g * (len(ws) - 1); x = x_mid - tot / 2
    for i, (p, wp) in enumerate(zip(pieces, ws)):
        kk = clamp(k * len(pieces) - i)
        if kk > 0:
            col = (cols or CHIPC)[i % len(cols or CHIPC)]
            chip(im, p.strip() or '·', x + wp / 2, cy - (1 - ease_out_back(kk)) * 1.2, col, size, a * min(1, kk * 2))
        x += wp + g
def coin(im, cx, cy, r, a=255, label='TOKEN', squash=1.0, size=None):
    rx = max(2, r * abs(squash))
    ell(im, cx, cy + r * 0.10 / H * 100, rx, r, '#D99A1E', a)
    ell(im, cx, cy, rx, r, F['yellow'], a); ell(im, cx, cy, rx * 0.78, r * 0.78, '#FFD978', a)
    if abs(squash) > 0.45 and label: txt(im, label, (cx, cy), size or r * 0.36, '#9A6A10', 'Bold', a=a)
def coin_stack(im, cx, base_y, n, r=46, a=255):
    for i in range(n):
        y = base_y - i * (r * 0.42) / H * 100
        ell(im, cx, y + 0.35, r, r * 0.42, '#D99A1E', a); ell(im, cx, y, r, r * 0.42, F['yellow'], a)
def ai_box(im, cx, cy, s=1.0, a=255):
    hw, hh = 9 * s, 9 * s * W / H
    for i in range(4):
        o = (i - 1.5) * hw * 0.42
        rr(im, (cx + o - 0.6, cy - hh - 1.3, cx + o + 0.6, cy + hh + 1.3), 4, F['ink2'], a=a)
        rr(im, (cx - hw - 2.2, cy + o * W / H - 0.35, cx + hw + 2.2, cy + o * W / H + 0.35), 4, F['ink2'], a=a)
    rr(im, (cx - hw, cy - hh, cx + hw, cy + hh), 26, F['ink'], a=a)
    rr(im, (cx - hw * 0.62, cy - hh * 0.62, cx + hw * 0.62, cy + hh * 0.62), 16, F['blue'], a=a)
    txt(im, 'AI', (cx, cy), 64 * s, F['white'], 'Bold', a=a)
def bubble(im, box, s, who='u', a=255, size=34, tcol=None, fill=None, strike=False):
    fill = fill or (F['blue'] if who == 'u' else F['white'])
    card(im, box, fill, r=30, a=a, shadow=who != 'u')
    x0, y0, x1, y1 = box; tc = tcol or (F['white'] if who == 'u' else F['ink'])
    if s: txt(im, s, (x0 + 3.2, (y0 + y1) / 2), size, tc, 'Medium', anchor='lm', a=a)
    if strike: line(im, x0 + 2, (y0 + y1) / 2, x1 - 2, (y0 + y1) / 2, F['red'], 6, a)
def check(im, cx, cy, s=1.0, col=F['green'], a=255):
    circ(im, cx, cy, 34 * s, col, a)
    ImageDraw.Draw(im).line([(X(cx) - 15 * s * SS, Y(cy)), (X(cx) - 4 * s * SS, Y(cy) + 12 * s * SS),
                             (X(cx) + 16 * s * SS, Y(cy) - 12 * s * SS)], fill=rgba(F['white'], a), width=int(8 * s * SS), joint='curve')
def cross(im, cx, cy, s=1.0, col=F['red'], a=255):
    circ(im, cx, cy, 34 * s, col, a); d = 13 * s * SS; c = (X(cx), Y(cy))
    for sx in (1, -1):
        ImageDraw.Draw(im).line([(c[0] - d, c[1] - d * sx), (c[0] + d, c[1] + d * sx)], fill=rgba(F['white'], a), width=int(8 * s * SS))
def heart(im, cx, cy, s, col=F['coral'], a=255):
    d = ImageDraw.Draw(im); R_ = 16 * s * SS; x, y = X(cx), Y(cy); c = rgba(col, a)
    for sx in (-1, 1): d.ellipse([x + sx * R_ * 0.72 - R_, y - R_, x + sx * R_ * 0.72 + R_, y + R_], fill=c)
    d.polygon([(x - R_ * 1.62, y + R_ * 0.35), (x + R_ * 1.62, y + R_ * 0.35), (x, y + R_ * 2.1)], fill=c)
def badge(im, s, cx, cy, col=F['ink'], tcol=F['white'], size=26, a=255):
    wp = (tw_px(s, size, 'Medium') + 34) / W * 100; hp = size * 1.7 / H * 100
    rr(im, (cx - wp / 2, cy - hp / 2, cx + wp / 2, cy + hp / 2), 40, col, a=a)
    txt(im, s, (cx, cy), size, tcol, 'Medium', a=a)
_LOGO = {}
def logo(dark=True):
    """Logo utama Sakelar (toggle: pil hitam + bulatan mint, latar transparan). Parameter dark diabaikan (kompatibilitas)."""
    if 'main' not in _LOGO: _LOGO['main'] = Image.open(os.path.join(A, 'brand', 'sakelar_logo_main.png')).convert('RGBA')
    return _LOGO['main']
def wordmark(l, cx, cy, wpx=300, col=F['ink'], tsize=None):
    """Logo Sakelar (toggle) + tulisan 'Sakelar AI' di bawahnya. wpx = lebar blok (logo ±55% dari wpx)."""
    lg = logo(); lw = int(wpx * 0.55 * SS); lgr = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    l.alpha_composite(lgr, (int(X(cx) - lw / 2), int(Y(cy) - lgr.height / 2)))
    txt(l, 'Sakelar AI', (cx, cy + (lgr.height / SS) / H * 100 / 2 + 2.2), tsize or wpx * 0.2, col, 'Bold')
def comp(dst, lay, alpha=1.0, scale=1.0, anchor=(50, 25), dy=0.0, dx=0.0):
    """Tempel layer 2x ke dst dengan alpha grup, skala (di sekitar anchor %) dan offset %."""
    if alpha <= 0.003 or scale <= 0.01: return
    bb = lay.getbbox()
    if not bb: return
    crop = lay.crop(bb); ox, oy = bb[0], bb[1]
    if abs(scale - 1) > 1e-3:
        ax, ay = X(anchor[0]), Y(anchor[1])
        crop = crop.resize((max(1, int(crop.width * scale)), max(1, int(crop.height * scale))), Image.BICUBIC)
        ox = ax + (ox - ax) * scale; oy = ay + (oy - ay) * scale
    if alpha < 1: crop.putalpha(crop.getchannel('A').point(lambda v: int(v * alpha)))
    dst.alpha_composite(crop, (int(ox + X(dx)), int(oy + Y(dy))))
def appear(t, t0, d=0.35):
    """(alpha, scale) pop-in standar mulai t0: opacity 0→1 0.16 s, scale 0.90→1.00 easeOutBack 0.35 s."""
    if t < t0: return 0.0, 0.9
    k = clamp((t - t0) / d); return min(1, k * 2.2), lerp(0.9, 1.0, ease_out_back(k))

# ---------------- background (tema clean) ----------------
_BGI = {}
def background(t, header):
    if header not in _BGI:
        b = Image.open(os.path.join(A, 'bg', 'office.png')).convert('RGB').resize((W * SS, H * SS), Image.LANCZOS)
        b = Image.blend(b, Image.new('RGB', b.size, (20, 22, 40)), 0.18).convert('RGBA')
        lay = canvas(); rr(lay, (3, 6.4, 97, 47.6), 44, F['bg'], a=232); b.alpha_composite(lay)   # panel info krem
        badge(b, header, 50, 3.6, F['ink'], F['white'], 24)
        _BGI[header] = b
    return _BGI[header].copy()

# ---------------- Reina ----------------
POSES = json.load(open(os.path.join(A, 'poses', 'poses.json')))
MRATIO = POSES['mouth_ratio']
_PI = {}; _SPR = {}
def sprite(name):
    if name not in _SPR: _SPR[name] = Image.open(os.path.join(A, 'sprites', f'{name}.png')).convert('RGBA')
    return _SPR[name]
def pose_image(name, shape=None):
    """Pose asli; jika shape (sprite mulut) diberikan: area mulut asli di-inpaint lalu sprite ditempel."""
    key = (name, shape)
    if key not in _PI:
        meta = POSES['poses'][name]
        if shape is None or 'mouth' not in meta:
            im = Image.open(os.path.join(A, 'poses', f'{name}.png')).convert('RGBA')
        else:
            m = meta['mouth']
            im = Image.open(os.path.join(A, 'poses', f'{name}.png')).convert('RGBA').copy()
            im.paste(Image.open(os.path.join(A, 'mouth_patches', f'{name}.png')).convert('RGBA'), tuple(m['patch_box'][:2]))
            s = sprite(shape)
            mw = int(m['width'] * m['scale'] * MRATIO.get(shape, 1.0))
            s = s.resize((mw, max(1, int(s.height * mw / s.width))), Image.LANCZOS)
            if m['rot']: s = s.rotate(m['rot'], Image.BICUBIC, expand=True)
            cx, cy = m['center']; im.alpha_composite(s, (cx - s.width // 2, cy - s.height // 2))
        _PI[key] = im.crop((0, 0, im.width, im.getbbox()[3]))
    return _PI[key]
def has_lipsync(name): return 'mouth' in POSES['poses'][name]

# ---------------- episode / timeline ----------------
RATE = 6.4      # suku kata per detik (setara VO yang sudah dipercepat 1.10x)
def syl(s):
    return len(re.findall(r'(ai|au|oi|[aiueo])', re.sub(r'[^a-z]', ' ', s.lower())))
def est(s):
    return syl(s) / RATE + 0.12 * len(re.findall(r'[,.?!…]\s', s + ' ')) + 0.15
def snap(x): return round(x * FPS) / FPS
def tc(x):
    x = round(x * 1000) / 1000; h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h:02d}:{m:02d}:{s:06.3f}'

SH = {}; LN = {}; E = None   # diisi oleh load_episode (dict yang sama dipakai episode via import *)
def rel(lid, f=0.0):
    """Waktu (detik, absolut) pada fraksi f dari baris dialog lid. Pakai ini untuk sinkron visual ke kata."""
    l = LN[lid]; return l['start'] + f * (l['end'] - l['start'])
def r(sid, lid, f=0.0):
    """Sama seperti rel() tapi relatif terhadap awal shot sid (untuk storyboard)."""
    return round(rel(lid, f) - SH[sid]['start'], 3)

class Episode:
    def __init__(self, mod, workdir):
        self.m = mod; self.workdir = workdir
        self.ep = mod.EP; self.tag = f'ep{mod.EP:02d}'
        self.audio_dir = os.path.join(workdir, 'audio', self.tag)
        dp = os.path.join(self.audio_dir, 'durs.json')
        self.durs = json.load(open(dp)) if os.path.exists(dp) else None
        self.build_timeline()
        self.vo = None
        ap = os.path.join(self.audio_dir, 'env.json')
        if os.path.exists(ap) and self.durs:
            al = json.load(open(ap)); db = np.array(al['env_db']); sp = db[db > -38]
            th = np.percentile(sp, 55) if len(sp) else -20
            lv = np.where(db < -38, 0, np.where(db < th, 1, 2))
            lv = np.array([int(np.round(np.median(lv[max(0, i - 3): i + 4]))) for i in range(len(lv))])
            self.vo = dict(hop=al['hop'], lv=lv)
    def build_timeline(self):
        m = self.m; t = 0.0; shots = []; lines = []; gap = getattr(m, 'GAP', 0.25)
        for sid, sc, title, ls, lead, tail in m.SHOTS:
            s0 = t; t = snap(t + lead)
            for k, li in enumerate(ls):
                if k: t = snap(t + gap)
                lid = f'L{li:02d}'; txt_ = m.LINES[li - 1]
                d = self.durs[lid] + 1 / FPS if self.durs else est(txt_)
                a = t; t = snap(t + d)
                lines.append(dict(id=lid, shot=sid, start=a, end=t, text=txt_, dur=t - a, syl=syl(txt_)))
            t = snap(t + tail)
            shots.append(dict(id=sid, scene=sc, title=title, start=s0, end=t, lines=[f'L{x:02d}' for x in ls]))
        self.shots, self.lines, self.total = shots, lines, t
        SH.clear(); SH.update({s['id']: s for s in shots}); LN.clear(); LN.update({l['id']: l for l in lines})
        self.keys = {s['id']: (rel(s['lines'][-1], 0.9) if s['lines'] else s['start'] + 1.5) for s in shots}
    # --- lip sync ---
    def line_at(self, t):
        for l in self.lines:
            if l['start'] <= t < l['end']: return l
        return None
    def talking(self, t):
        if not self.line_at(t): return 0
        if self.vo is not None:
            i = int(t / self.vo['hop']); lv = self.vo['lv']
            return int(lv[i]) if 0 <= i < len(lv) else 0
        return [1, 2, 1, 0, 2, 1, 2, 0][(int(t * FPS) // 3) % 8]   # pola sementara sebelum ada VO
    def mouth(self, t, smile):
        k = self.talking(t)
        if smile: return 'mouth_smile_closed' if k == 0 else 'mouth_smile_talk'
        return [None, 'mouth_half', 'mouth_open_A'][k]
    # --- subtitle ---
    def sub_text(self, t):
        l = self.line_at(t)
        if not l: return None
        s = l['text']; lines = wrap(s)
        if len(lines) <= 2: return '\n'.join(lines)
        words = s.split(); n = math.ceil(len(lines) / 2); per = math.ceil(len(words) / n)
        chunks = ['\n'.join(wrap(' '.join(words[i:i + per]))) for i in range(0, len(words), per)]
        k = min(len(chunks) - 1, int((t - l['start']) / (l['end'] - l['start']) * len(chunks)))
        return chunks[k]
    def shot_at(self, t):
        for s in self.shots:
            if s['start'] <= t < s['end']: return s
        return self.shots[-1]
    # --- frame ---
    def frame(self, t):
        """Frame pada waktu t (detik). Fungsi murni dari t."""
        m = self.m; s = self.shot_at(t); sid = s['id']; u = t - s['start']
        i = self.shots.index(s); prev = self.shots[i - 1] if i else None
        enter = prev is None or prev['scene'] != s['scene'] or m.POSE[prev['id']] != m.POSE[sid]
        bg = background(t, f'REINA EXPLAINS AI  ·  EP {self.ep:02d}')
        pn = canvas(); m.panel(t, sid, pn); bg.alpha_composite(pn)
        base = bg.resize((W, H), Image.LANCZOS)
        name = m.POSE[sid]; smile = sid in getattr(m, 'SMILE', set())
        img = pose_image(name, self.mouth(t, smile) if has_lipsync(name) else None)
        meta = POSES['poses'][name]; w = int(W * meta['width_pct'] / 100)
        sy = 1 + 0.006 * (0.5 + 0.5 * math.sin(2 * math.pi * t / 3.0))     # napas
        rimg = img.resize((w, int(w * img.height / img.width * sy)), Image.LANCZOS)
        dy = (1 - ease_out_back(clamp(u / 0.35))) * 5 if enter else 0     # masuk saat pose/scene berganti
        base.alpha_composite(rimg, (int(W / 2 - w / 2), int(H - rimg.height + dy * H / 100)))
        st = self.sub_text(t)
        if st:
            ov = canvas(); subtitle(ov, st); base.alpha_composite(ov.resize((W, H), Image.LANCZOS))
        if t > self.total - 0.5:
            k = clamp((t - (self.total - 0.5)) / 0.5)
            base = Image.blend(base, Image.new('RGBA', (W, H), rgba(F['bg'])), k)
        return base.convert('RGB')

def wrap(s, n=32):
    words, lines, cur = s.split(), [], ''
    for w_ in words:
        if len(cur) + len(w_) + (1 if cur else 0) > n: lines.append(cur); cur = w_
        else: cur = (cur + ' ' + w_) if cur else w_
    if cur: lines.append(cur)
    return lines
def subtitle(im, s):
    lines = s.split('\n'); size = 40
    wmax = max(tw_px(l, size, 'Medium') for l in lines)
    hp = (len(lines) * size * 1.42 + 34) / H * 100; wp = (wmax + 70) / W * 100; cy = 52.0
    rr(im, (50 - wp / 2, cy - hp / 2 + 0.3, 50 + wp / 2, cy + hp / 2 + 0.3), 30, F['ink'], a=40)
    rr(im, (50 - wp / 2, cy - hp / 2, 50 + wp / 2, cy + hp / 2), 30, F['white'], a=245)
    txt(im, s, (50, cy), size, F['ink'], 'Medium', spacing=12)

def load_episode(path, workdir='.'):
    global E
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    E = Episode(mod, workdir); return E
