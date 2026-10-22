"""Efek suara sintetis (numpy, 48 kHz, mono). Tanpa file eksternal, bebas lisensi.
Pakai key di LIB pada spec shot: (t_relatif_shot, key, durasi_s, gain_dB_relatif_VO, fungsi)."""
import numpy as np
SR = 48000

def _t(d): return np.arange(int(SR * d)) / SR
def _env(n, a=0.004, rel=None):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    if rel: e *= np.exp(-np.arange(n) / (rel * SR))
    return e
def _sweep(f0, f1, d, shape='sine'):
    t = _t(d); f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) if shape == 'sine' else np.sign(np.sin(ph)) * 0.6
def _tone(f, d, harm=(1,), rel=0.3):
    t = _t(d); y = sum(np.sin(2 * np.pi * f * h * t) / (i + 1) for i, h in enumerate(harm)); return y * _env(len(t), 0.003, rel)
def _noise(d, seed=0): return np.random.default_rng(seed).standard_normal(int(SR * d))
def _bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def _norm(y): m = np.abs(y).max(); return y / m if m > 0 else y

def pop(d=0.15, up=0):
    k = 2 ** (up / 12); y = _sweep(500 * k, 1100 * k, 0.09) * _env(int(0.09 * SR), 0.002, 0.03); return y
def pop_hi(d=0.15): return pop(d, 4)
def ding(d=0.4): return _tone(1568, max(d, 0.4), (1, 2.76, 5.4), 0.18)
def chime(d=0.6): return np.concatenate([_tone(1047, 0.12, (1, 2), 0.08), _tone(1319, 0.12, (1, 2), 0.08), _tone(1568, max(0.2, d - 0.24), (1, 2, 3), 0.2)])
def buzz(d=0.25): t = _t(d); return _sweep(180, 140, d, 'square') * _env(len(t), 0.005, d / 2)
def whoosh(d=0.4):
    n = _bp(_noise(d, 1), 400, 5000); t = _t(d); return n * np.sin(np.pi * t / d) ** 2 * 0.6
def coin(d=0.5):
    a = _tone(1976, 0.08, (1, 2), 0.05); b = _tone(2637, max(0.2, d - 0.08), (1, 2, 3), 0.15); return np.concatenate([a, b])
def coins(d=0.8):
    y = np.zeros(int(SR * d)); rng = np.random.default_rng(3)
    for i in range(max(2, int(d / 0.12))):
        c = _tone(rng.uniform(2200, 3400), 0.12, (1, 2.3), 0.04); s = int(i * 0.11 * SR)
        if s + len(c) < len(y): y[s:s + len(c)] += c * rng.uniform(0.5, 1)
    return y
def kaching(d=0.5): return np.concatenate([_bp(_noise(0.04, 2), 2000, 8000) * 0.5, coin(d - 0.04)])
def snip(d=0.15):
    n = _bp(_noise(0.05, 4), 2500, 9000) * _env(int(0.05 * SR), 0.001, 0.008); return np.concatenate([n, np.zeros(int(0.03 * SR)), n * 0.8])
def snips(d=0.5):
    y = np.zeros(int(SR * d)); s = snip()
    for i in range(int(d / 0.1)):
        o = int(i * 0.1 * SR)
        if o + len(s) < len(y): y[o:o + len(s)] += s
    return y
def click(d=0.08):
    n = _bp(_noise(0.02, 5), 1500, 7000) * _env(int(0.02 * SR), 0.0005, 0.004); return n
def clicks(d=0.8):
    y = np.zeros(int(SR * d)); c = click()
    for i in range(3):
        o = int(i * d / 3 * SR); y[o:o + len(c)] += c
    return y
def tick(d=1.5):
    y = np.zeros(int(SR * d)); c = click() * 0.6
    for i in range(int(d / 0.07)):
        o = int(i * 0.07 * SR)
        if o + len(c) < len(y): y[o:o + len(c)] += c
    return y * np.linspace(0.6, 1, len(y))
def sparkle(d=1.0):
    y = np.zeros(int(SR * d)); rng = np.random.default_rng(7)
    for i in range(int(d / 0.09)):
        c = _tone(rng.uniform(2500, 4200), 0.15, (1,), 0.05) * rng.uniform(0.3, 0.8); o = int(i * 0.09 * SR)
        if o + len(c) < len(y): y[o:o + len(c)] += c
    return y
def boing(d=0.3):
    t = _t(d); f = 220 + 160 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 6); return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(len(t), 0.003, d / 2.5)
def clunk(d=0.3):
    y = _tone(110, d, (1, 2.1, 3.3), 0.06); n = _bp(_noise(0.03, 8), 200, 1500); y[:len(n)] += n * 0.5; return y
def hum(d=2.0):
    t = _t(d); y = (np.sin(2 * np.pi * 110 * t) + 0.5 * np.sin(2 * np.pi * 220 * t) + 0.2 * _bp(_noise(d, 9), 100, 600))
    e = np.ones(len(t)); fa = int(0.3 * SR); e[:fa] = np.linspace(0, 1, fa); e[-fa:] = np.linspace(1, 0, fa); return y * e * 0.5
def blip(d=0.2): return np.concatenate([_sweep(660, 660, 0.06, 'square') * 0.5, _sweep(990, 990, 0.08, 'square') * 0.5]) * 0.8
def scratch(d=0.3):
    t = _t(d); return _bp(_noise(d, 10), 300, 3000) * np.abs(np.sin(2 * np.pi * 7 * t)) * _env(len(t), 0.002, d / 2)
def stack(d=0.8):
    y = np.zeros(int(SR * d)); p = _bp(_noise(0.05, 11), 800, 4000) * _env(int(0.05 * SR), 0.001, 0.01)
    for i in range(int(d / 0.11)):
        o = int(i * 0.11 * SR)
        if o + len(p) < len(y): y[o:o + len(p)] += p
    return y
def jingle(d=0.6): return np.concatenate([_tone(784, 0.18, (1, 2), 0.1), _tone(1175, max(0.25, d - 0.18), (1, 2, 3), 0.2)])
def stinger(d=1.2):
    return np.concatenate([_tone(659, 0.15, (1, 2), 0.1), _tone(784, 0.15, (1, 2), 0.1), _tone(1047, max(0.4, d - 0.3), (1, 2, 3), 0.35)])
def swipe(d=0.3): t = _t(d); return _bp(_noise(d, 12), 1500, 6000) * np.sin(np.pi * t / d) * 0.5

LIB = {   # key: (fungsi, deskripsi untuk storyboard)
    'pop': (pop, 'pop pendek'), 'pop_hi': (pop_hi, 'pop nada tinggi'), 'ding': (ding, 'ding (benar/info)'),
    'chime': (chime, 'chime 3 nada naik'), 'buzz': (buzz, 'buzz (salah)'), 'whoosh': (whoosh, 'whoosh'),
    'coin': (coin, 'koin cling'), 'coins': (coins, 'koin gemerincing'), 'kaching': (kaching, 'ka-ching kecil'),
    'snip': (snip, 'gunting snip'), 'snips': (snips, 'snip beruntun'), 'click': (click, 'klik'), 'clicks': (clicks, 'klik x3'),
    'tick': (tick, 'tick-tick counter'), 'sparkle': (sparkle, 'sparkle/twinkle'), 'boing': (boing, 'boing kecil'),
    'clunk': (clunk, 'clunk berat'), 'hum': (hum, 'hum mesin halus'),
    'blip': (blip, 'blip arcade 8-bit'), 'scratch': (scratch, 'record scratch'), 'stack': (stack, 'tumpukan kertas'),
    'jingle': (jingle, 'jingle brand 2 nada'), 'stinger': (stinger, 'stinger penutup 3 nada'), 'swipe': (swipe, 'swipe/marker'),
}

def render(cues, total, vo_peak=0.89):
    """cues: list (t_absolut, key, dur, dB). Return array mono SR panjang total."""
    y = np.zeros(int((total + 1.5) * SR))
    for t, key, dur, db in cues:
        fn = LIB[key][0]; s = _norm(np.asarray(fn(dur), float)) * vo_peak * 0.75 * 10 ** (db / 20)
        fo = min(len(s), int(0.01 * SR)); s[-fo:] *= np.linspace(1, 0, fo)
        a = int(t * SR); b = min(len(y), a + len(s)); y[a:b] += s[:b - a]
    return y
