"""Reina Tutorial — Episode 03: "Sekarang Bisa Chat AI Langsung di Web Sakelar!" (tutorial fitur Chat, tema putih polos).
Satu file = satu episode: naskah, shot, pose, posisi, visual panel(t), spec storyboard + SFX, arahan VO.
Jalankan:  python run.py stage1 episodes/tutorial03.py   lalu   python run.py stage2 episodes/tutorial03.py <zip_suara>"""
import math
from PIL import Image, ImageDraw
from reina import *

SERIES = 'Reina Tutorial'
EP = 3
TAG = 'tutorial03'
TITLE = 'Sekarang Bisa Chat AI Langsung di Web Sakelar!'
SCENES = {1: 'Hook', 2: 'Dulu vs sekarang', 3: 'Tutorial 4 langkah', 4: 'Satu dashboard', 5: 'Tips pilih model',
          6: 'Pantau pemakaian', 7: 'Closing', 8: 'End card'}
META = dict(
    tujuan='Tutorial fitur baru Chat di web Sakelar AI: cara pakai 4 langkah dari dashboard, plus tips memilih model; edukasi tetap berguna (model ringan vs besar, membandingkan jawaban).',
    konsep=('Hook: mau coba model AI tapi nggak bisa ngoding → fitur baru Chat → dulu harus nulis kode + API key + aplikasi → '
            'sekarang buka web langsung chat → 4 langkah: login, ketuk menu kanan atas, pilih Chat (di bawah Ringkasan), pilih model + ketik + kirim → '
            'jawaban muncul → semua di satu dashboard (Chat, Top up, API keys) → tips: tugas simpel = model ringan, tugas berat = model besar, '
            'bingung = tanya hal sama ke dua model → pantau di menu Pemakaian → developer tetap pakai API, yang mau coba tinggal chat → punchline "isi hati aku".'),
    fakta=['Dashboard Sakelar punya menu: Ringkasan, Chat, Top up, Shop, API keys, Model, Pemakaian, Log, Dokumentasi, FAQ, Pengaturan (dari screenshot user).',
           'Menu dibuka lewat tombol bulat ☰ di pojok kanan atas (tampilan HP); "Chat" ada tepat di bawah "Ringkasan".',
           'Pakai API AI biasanya perlu API key + kode/aplikasi.',
           'Base URL API Sakelar: api.sakelar.web.id/v1.',
           'Model kecil/ringan biasanya cukup untuk tugas simpel; model besar biasanya lebih kuat untuk tugas berat (diucapkan dengan "biasanya").'],
    asumsi=['Mockup layar HP digambar ulang flat (bukan screenshot asli) mengikuti layout screenshot user.',
            'Nama model di layar Chat memakai "Model A/B (contoh)" — bukan nama model asli.',
            'Grafik Pemakaian tanpa angka, diberi label "ilustrasi".',
            'Layar login digambar generik (email, password, tombol Masuk).'],
    konfirmasi=['Apakah di halaman Chat memang ada pilihan model? (L10 "pilih modelnya" & SH09). Kalau tidak ada, L10 diganti "ketik pertanyaan, terus kirim".',
                'Apakah pemakaian Chat memotong saldo/paket yang sama dan tercatat di menu Pemakaian? (L17). Kalau belum, L17 diganti.',
                'URL di end card pakai "sakelar.web.id" — ganti ke "app.sakelar.web.id" kalau dashboard ada di subdomain app.',
                'Halaman login: label tombol & field asli (sekarang "Masuk", email, password).'],
    softsell='Seluruh episode berbasis fitur (tutorial), tapi SH12–SH15 tetap tips umum memilih model.',
)
PRON = [('API', 'ei-pi-ai'), ('API key', 'ei-pi-ai ki'), ('AI', 'ei-ai'), ('Chat', 'chet'), ('Top up', 'top ap'),
        ('dashboard', 'desy-bord'), ('login', 'log-in'), ('developer', 'di-ve-lo-per'), ('Sakelar', 'sa-ke-lar')]
VO_DIR = {'L01': 'penasaran, nada tanya, tekan "nggak bisa ngoding"', 'L02': 'semangat, naik di "fitur baru", ceria di "Chat!"',
 'L03': 'bercerita, agak capek di "nulis kode dulu"', 'L04': 'cepat, ritmis tiga langkah, sedikit menghela di "baru deh"',
 'L05': 'jeda kecil setelah "Sekarang?", lalu ringan dan cepat', 'L06': 'percaya diri, tekan "empat langkah"',
 'L07': 'jelas, tempo sedang', 'L08': 'jelas, tekan "pojok kanan atas"', 'L09': 'jelas, tekan "Chat"',
 'L10': 'ritmis tiga ketukan: pilih — ketik — kirim', 'L11': 'puas, ringan, senyum', 'L12': 'nada "nah tahu nggak", tiga menu dibaca berirama',
 'L13': 'ramah, membuka tips', 'L14': 'santai, tanya lalu jawab', 'L15': 'santai, tekan "lebih besar"',
 'L16': 'nada ngasih trik, tekan "bandingin"', 'L17': 'informatif, tenang', 'L18': 'menyimpulkan, mantap',
 'L19': 'hangat, mengajak', 'L20': 'malu-malu manis, jeda sebelum "isi hati aku", senyum di akhir'}

# ---- naskah terkunci (1 item = 1 baris VO = L01, L02, ...) ----
LINES = [
 'Mau coba model AI, tapi nggak bisa ngoding?',
 'Tenang, sekarang Sakelar AI punya fitur baru: Chat!',
 'Dulu, buat pakai API AI, kamu harus nulis kode dulu.',
 'Bikin API key, pasang di aplikasi, baru deh bisa ngobrol sama modelnya.',
 'Sekarang? Cukup buka webnya, langsung chat.',
 'Aku tunjukin caranya, cuma empat langkah.',
 'Satu, login ke dashboard Sakelar.',
 'Dua, ketuk tombol menu di pojok kanan atas.',
 'Tiga, pilih menu Chat, tepat di bawah Ringkasan.',
 'Empat, pilih modelnya, ketik pertanyaan, terus kirim.',
 'Udah, jawabannya langsung muncul.',
 'Dan semuanya ada di satu dashboard: Chat, Top up, sampai API key.',
 'Nah, biar makin pas, ini tips milih model.',
 'Tugas simpel kayak ringkas teks? Pakai model yang ringan aja.',
 'Tugas berat kayak nulis kode? Model yang lebih besar biasanya lebih jago.',
 'Masih bingung? Tanya hal yang sama ke dua model, terus bandingin.',
 'Pemakaiannya bisa kamu pantau di menu Pemakaian.',
 'Jadi buat developer, API tetap jalan.',
 'Buat kamu yang cuma mau nyoba, sekarang tinggal chat.',
 'Gampang kan? Lebih gampang daripada nebak isi hati aku.',
]

# (id, scene, judul, [nomor baris], jeda_awal_s, jeda_akhir_s)
SHOTS = [
 ('SH01', 1, 'Nggak bisa ngoding?', [1], 0.5, 0.2),
 ('SH02', 1, 'Fitur baru: Chat', [2], 0.15, 0.4),
 ('SH03', 2, 'Dulu: kode + API key + aplikasi', [3, 4], 0.25, 0.2),
 ('SH04', 2, 'Sekarang: buka web, chat', [5], 0.15, 0.4),
 ('SH05', 3, 'Cuma 4 langkah', [6], 0.25, 0.15),
 ('SH06', 3, 'Langkah 1: login', [7], 0.1, 0.2),
 ('SH07', 3, 'Langkah 2: tombol menu', [8], 0.1, 0.2),
 ('SH08', 3, 'Langkah 3: menu Chat', [9], 0.1, 0.2),
 ('SH09', 3, 'Langkah 4: model, ketik, kirim', [10], 0.1, 0.2),
 ('SH10', 3, 'Jawaban muncul', [11], 0.1, 0.4),
 ('SH11', 4, 'Satu dashboard', [12], 0.25, 0.4),
 ('SH12', 5, 'Tips pilih model', [13], 0.25, 0.15),
 ('SH13', 5, 'Tugas simpel = model ringan', [14], 0.1, 0.2),
 ('SH14', 5, 'Tugas berat = model besar', [15], 0.1, 0.2),
 ('SH15', 5, 'Bandingin dua model', [16], 0.1, 0.4),
 ('SH16', 6, 'Menu Pemakaian', [17], 0.25, 0.4),
 ('SH17', 7, 'Developer API, kamu Chat', [18, 19], 0.25, 0.25),
 ('SH18', 7, 'Isi hati aku', [20], 0.1, 0.6),
 ('SH19', 8, 'End card', [], 0.0, 2.5),
]

POSE = {'SH01': 'arms34', 'SH02': 'wave', 'SH03': 'desk', 'SH04': 'phone', 'SH05': 'hands_on_hips',
        'SH06': 'point_up', 'SH07': 'point', 'SH08': 'point_up', 'SH09': 'thumbs_up', 'SH10': 'hands_on_hips',
        'SH11': 'arms34', 'SH12': 'point_up', 'SH13': 'thumbs_up', 'SH14': 'bust', 'SH15': 'arms34',
        'SH16': 'phone', 'SH17': 'hands_on_hips', 'SH18': 'shy_lean', 'SH19': 'wave'}
POS = {'SH01': 'kiri', 'SH02': 'closeup', 'SH03': 'tengah', 'SH04': 'kanan', 'SH05': 'tengah', 'SH06': 'kiri',
       'SH07': 'kanan', 'SH08': 'kiri', 'SH09': 'kanan', 'SH10': 'closeup', 'SH11': 'kiri', 'SH12': 'kanan',
       'SH13': 'kiri', 'SH14': 'closeup', 'SH15': 'kanan', 'SH16': 'kiri', 'SH17': 'kanan', 'SH18': 'closeup', 'SH19': 'tengah'}
SMILE = {'SH18'}
EXPR = {'SH01': 'heran, menantang ringan', 'SH02': 'ceria, menyapa', 'SH03': 'fokus ke monitor, agak capek',
        'SH04': 'senang sambil lihat HP', 'SH05': 'percaya diri', 'SH06': 'menjelaskan', 'SH07': 'menunjuk ke arah tombol',
        'SH08': 'menjelaskan', 'SH09': 'ceria', 'SH10': 'puas', 'SH11': 'analitis', 'SH12': 'menjelaskan, "nah"',
        'SH13': 'ceria, setuju', 'SH14': 'tegas, tangan bersilang', 'SH15': 'analitis', 'SH16': 'menjelaskan sambil lihat HP',
        'SH17': 'santai, menutup', 'SH18': 'malu-malu, senyum (mulut smile)', 'SH19': 'ceria, melambai'}

# ---------------- warna UI Sakelar (mockup layar) ----------------
SK = dict(ink='#1B1D1F', bg='#F3F2EE', card='#FFFFFF', green='#1F6B52', mint='#8FD3B0', border='#D6D3CC', gray='#6B6F73', bar='#E4E1DA')
PH = (42, 8, 86, 46)   # posisi HP mockup di tutorial (kanan atas), kolom kiri untuk label langkah


# ---------------- helper lokal ----------------
def phone(l, box):
    """Bingkai HP gelap + layar terang. Return kotak layar (x0,y0,x1,y1) dalam %."""
    x0, y0, x1, y1 = box
    rr(l, (x0, y0 + 0.5, x1, y1 + 0.5), 56, F['ink'], a=45)
    rr(l, box, 56, SK['ink'])
    s = (x0 + 1.8, y0 + 1.0, x1 - 1.8, y1 - 1.0)
    rr(l, s, 42, SK['bg'])
    cx = (x0 + x1) / 2; rr(l, (cx - 4.5, y0 + 1.5, cx + 4.5, y0 + 2.4), 12, SK['ink'])
    return s

def toggle(l, cx, cy, s=1.0):
    """Logo toggle Sakelar sederhana: pil gelap + bulatan mint di kanan."""
    w, h = 74 * s / W * 100, 40 * s / H * 100
    rr(l, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 40, SK['ink'])
    circ(l, cx + w / 2 - 20 * s / W * 100, cy, 14 * s, SK['mint'])

def burger(l, cx, cy, s=1.0):
    circ(l, cx, cy, 30 * s, SK['ink'])
    for k in (-1, 0, 1): line(l, cx - 1.3 * s, cy + k * 0.55 * s, cx + 1.3 * s, cy + k * 0.55 * s, F['white'], 4)

def topbar(l, sc, name=True):
    x0, y0, x1, y1 = sc
    toggle(l, x0 + 4.5, y0 + 3.3, 0.8)
    if name: txt(l, 'Sakelar', (x0 + 9, y0 + 3.3), 30, SK['ink'], 'Bold', 'lm')
    burger(l, x1 - 5, y0 + 3.3, 0.9)
    line(l, x0, y0 + 6.0, x1, y0 + 6.0, SK['border'], 2)

def tap(l, cx, cy, t, t0):
    """Efek ketuk: titik + cincin melebar 0.5 s (fungsi murni dari t)."""
    if t < t0: return
    p = clamp((t - t0) / 0.5)
    circ(l, cx, cy, 22 + 46 * p, None, outline=F['coral'], w=6, a=255 * (1 - p))
    if t < t0 + 0.9: circ(l, cx, cy, 20, F['coral'], a=170)

def step_head(l, n, label):
    """Kolom kiri tutorial: lingkaran nomor besar + label 2 baris."""
    circ(l, 20, 15, 62, CHIPC[(n - 1) % 5]); txt(l, str(n), (20, 15.2), 72, F['white'])
    txt(l, label, (20, 25.5), 40, F['ink'], 'Bold', spacing=8)

def menu_rows(l, sc, y0, hl=False):
    """Daftar menu dashboard (mengikuti screenshot user). Ringkasan aktif, Chat bisa disorot."""
    x0, _, x1, _ = sc
    items = ['Ringkasan', 'Chat', 'Top up', 'Shop', 'API keys', 'Model', 'Pemakaian']
    for i, it in enumerate(items):
        y = y0 + i * 3.6
        if i == 0:
            rr(l, (x0 + 1.5, y - 1.45, x1 - 1.5, y + 1.45), 26, SK['ink'])
            txt(l, it, (x0 + 4.5, y), 30, F['white'], 'Medium', 'lm')
        else:
            if i == 1 and hl:
                rr(l, (x0 + 1.5, y - 1.45, x1 - 1.5, y + 1.45), 26, '#E3F2EA', outline=SK['green'], w=4)
            txt(l, it, (x0 + 4.5, y), 30, SK['green'] if (i == 1 and hl) else SK['gray'], 'SemiBold' if (i == 1 and hl) else 'Medium', 'lm')

def chat_head(l, sc, model='pilih model', picked=False):
    x0, y0, x1, y1 = sc
    topbar(l, sc)
    txt(l, 'Chat', (x0 + 2.5, y0 + 9.3), 38, SK['ink'], 'Bold', 'lm')
    w = (tw_px(model, 24, 'Medium') + 70) / W * 100
    bx1 = x1 - 2; bx0 = bx1 - w
    rr(l, (bx0, y0 + 8.0, bx1, y0 + 10.6), 30, SK['card'], outline=SK['green'] if picked else SK['border'], w=3)
    txt(l, model, (bx0 + 1.8, y0 + 9.3), 24, SK['ink'], 'Medium', 'lm')
    poly(l, [(bx1 - 3.0, y0 + 9.0), (bx1 - 1.6, y0 + 9.0), (bx1 - 2.3, y0 + 9.7)], SK['gray'])

def chat_input(l, sc, s='', send_hl=False):
    x0, y0, x1, y1 = sc
    rr(l, (x0 + 1.5, y1 - 4.6, x1 - 7.5, y1 - 1.4), 30, SK['card'], outline=SK['border'], w=3)
    txt(l, s if s else 'Tulis pesan…', (x0 + 3.5, y1 - 3.0), 24, SK['ink'] if s else SK['gray'], 'Medium', 'lm')
    circ(l, x1 - 4.2, y1 - 3.0, 30, SK['green'] if (s or send_hl) else SK['border'])
    arrow(l, x1 - 5.2, y1 - 3.0, x1 - 3.0, y1 - 3.0, 1, F['white'], 5)

def ai_lines(l, x0, y0, n, k, wmax=26):
    """Baris jawaban abu yang tumbuh (k 0..1)."""
    ws = [wmax, wmax * 0.85, wmax * 0.95, wmax * 0.6][:n]
    for i, w in enumerate(ws):
        kk = clamp(k * n - i)
        if kk > 0: rr(l, (x0, y0 + i * 1.7 - 0.45, x0 + w * kk, y0 + i * 1.7 + 0.45), 8, SK['bar'])

def doc_icon(l, cx, cy, s=1.0):
    rr(l, (cx - 4.5 * s, cy - 4.5 * s, cx + 4.5 * s, cy + 4.5 * s), 16, F['white'], outline=F['ink2'], w=4)
    for i in range(4): rr(l, (cx - 3 * s, cy - 2.6 * s + i * 1.6 * s, cx + (3 - (i == 3) * 2) * s, cy - 2.1 * s + i * 1.6 * s), 4, F['blue2'])


def panel(t, sid, im):
    """Gambar visual (area y 7–47%) shot sid pada waktu t ke layer 2x im."""
    s = SH[sid]; u = t - s['start']; L = lambda lid, f=0.0: rel(lid, f)
    def G(t0, fn, anchor=(50, 25), d=0.35):
        a, sc = appear(t, t0, d)
        if a <= 0: return
        lay = canvas(); fn(lay); comp(im, lay, a, sc, anchor)

    if sid == 'SH01':   # nggak bisa ngoding
        def code(l):
            rr(l, (10, 9.4, 90, 33.4), 30, F['ink'], a=40); rr(l, (10, 9, 90, 33), 30, F['ink'])
            for i, c in enumerate((F['red'], F['yellow'], F['mint'])): circ(l, 14 + i * 2.8, 11.2, 10, c)
            for i, (w_, c) in enumerate(((44, '#7E8AA8'), (60, '#C9D3EA'), (36, '#7E8AA8'), (52, '#C9D3EA'), (28, '#7E8AA8'))):
                rr(l, (15, 15 + i * 3.2, 15 + w_, 16.2 + i * 3.2), 8, c)
        G(s['start'] + 0.15, code, (50, 21))
        for i, (x, y) in enumerate(((78, 15), (84, 24), (72, 28))):
            a, sc = appear(t, L('L01', 0.35 + 0.12 * i))
            lay = canvas(); circ(lay, x, y, 34, F['coral']); txt(lay, '?', (x, y + 0.1), 46, F['white']); comp(im, lay, a, sc, (x, y))
        a, sc = appear(t, L('L01', 0.7))
        lay = canvas(); badge(lay, 'nggak bisa ngoding?', 50, 40, F['coral'], F['white'], 40); comp(im, lay, a, sc, (50, 40))

    elif sid == 'SH02':   # fitur baru Chat
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); wordmark(lay, 50, 12, 220, tsize=40); comp(im, lay, a, sc, (50, 12))
        a, sc = appear(t, L('L02', 0.5))
        lay = canvas(); badge(lay, 'FITUR BARU', 50, 23.5, F['yellow'], F['ink'], 34); comp(im, lay, a, sc, (50, 23.5))
        def chatb(l):
            rr(l, (30, 28, 70, 40), 40, SK['green'])
            poly(l, [(36, 39.5), (42, 39.5), (35, 43.5)], SK['green'])
            txt(l, 'Chat', (50, 34), 70, F['white'])
        G(L('L02', 0.78), chatb, (50, 34))

    elif sid == 'SH03':   # dulu: ribet
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); badge(lay, 'DULU', 50, 10.5, F['ink2'], F['white'], 36); comp(im, lay, a, sc, (50, 10.5))
        steps = [('tulis kode', L('L03', 0.6)), ('API key', L('L04', 0.08)), ('aplikasi', L('L04', 0.33)), ('ngobrol\nsama AI', L('L04', 0.75))]
        xs = [15, 38.3, 61.7, 85]
        for i, ((lab, t0), x) in enumerate(zip(steps, xs)):
            def f(l, lab=lab, x=x, i=i):
                card(l, (x - 10, 15, x + 10, 30), r=30)
                if i == 0: txt(l, '</>', (x, 20), 46, F['blue'])
                elif i == 1: circ(l, x - 4.5, 20, 30, F['yellow']); circ(l, x - 4.5, 20, 12, F['white']); rr(l, (x - 2, 19.6, x + 6, 20.4), 6, F['yellow']); rr(l, (x + 3, 20.2, x + 4.3, 21.4), 4, F['yellow']); rr(l, (x + 4.8, 20.2, x + 6, 21.0), 4, F['yellow'])
                elif i == 2: rr(l, (x - 4.5, 17.5, x + 4.5, 22.8), 12, F['blue2']); rr(l, (x - 4.5, 17.5, x + 4.5, 18.6), 6, F['blue'])
                else: ai_box(l, x, 20.2, 0.32)
                txt(l, lab, (x, 26.6 if '\n' not in lab else 26.0), 26 if '\n' not in lab else 22, F['ink'], 'SemiBold', spacing=2)
            G(t0, f, (x, 22))
            if i:
                k = clamp((t - t0 + 0.1) / 0.3)
                if k > 0: lay = canvas(); arrow(lay, xs[i - 1] + 10.6, 22.5, x - 10.6, 22.5, k, F['ink2'], 5); comp(im, lay)
        a, sc = appear(t, L('L04', 0.85))
        lay = canvas(); badge(lay, 'harus ngoding dulu', 50, 37, F['coral'], F['white'], 34); comp(im, lay, a, sc, (50, 37))

    elif sid == 'SH04':   # sekarang: buka web, chat
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); badge(lay, 'SEKARANG', 50, 10.5, SK['green'], F['white'], 36); comp(im, lay, a, sc, (50, 10.5))
        def f(l):
            scr = phone(l, (30, 14, 70, 46)); x0, y0, x1, y1 = scr
            topbar(l, scr)
            rr(l, (x1 - 20, y0 + 9, x1 - 2, y0 + 12.2), 26, SK['green']); txt(l, 'Halo!', (x1 - 11, y0 + 10.6), 26, F['white'], 'Medium')
            if t >= L('L05', 0.75):
                rr(l, (x0 + 2, y0 + 14, x0 + 26, y0 + 20.5), 26, SK['card'], outline=SK['border'], w=2)
                ai_lines(l, x0 + 4, y0 + 15.6, 3, clamp((t - L('L05', 0.75)) / 0.5), 19)
            chat_input(l, scr)
        G(L('L05', 0.35), f, (50, 30))

    elif sid == 'SH05':   # 4 langkah
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'CUMA\n4 LANGKAH', (50, 18), 86, F['ink'], 'Bold', spacing=4); comp(im, lay, a, sc, (50, 18))
        for i in range(4):
            a, sc = appear(t, L('L06', 0.45 + 0.12 * i))
            x = 23 + 18 * i
            lay = canvas(); circ(lay, x, 35.5, 50, CHIPC[i]); txt(lay, str(i + 1), (x, 35.7), 58, F['white']); comp(im, lay, a, sc, (x, 35.5))

    elif sid in ('SH06', 'SH07', 'SH08', 'SH09', 'SH10'):
        n = {'SH06': 1, 'SH07': 2, 'SH08': 3, 'SH09': 4, 'SH10': 0}[sid]
        lid = {'SH06': 'L07', 'SH07': 'L08', 'SH08': 'L09', 'SH09': 'L10', 'SH10': 'L11'}[sid]
        if n:
            lab = ['Login ke\ndashboard', 'Ketuk\ntombol menu', 'Pilih\nChat', 'Pilih model,\nketik, kirim'][n - 1]
            a, sc = appear(t, s['start'] + 0.05)
            lay = canvas(); step_head(lay, n, lab); comp(im, lay, a, sc, (20, 20))
        else:
            a, sc = appear(t, L(lid, 0.3))
            lay = canvas(); check(lay, 20, 15, 1.8); txt(lay, 'Jawaban\nlangsung\nmuncul', (20, 27), 40, F['ink'], 'Bold', spacing=8); comp(im, lay, a, sc, (20, 20))
        lay = canvas(); scr = phone(lay, PH); x0, y0, x1, y1 = scr; cx = (x0 + x1) / 2
        if n == 1:
            toggle(lay, cx, y0 + 7, 1.4); txt(lay, 'Sakelar', (cx, y0 + 11.2), 40, SK['ink'], 'Bold')
            for i, ph in enumerate(('email', 'password')):
                yy = y0 + 15.5 + i * 4.6
                rr(lay, (x0 + 3, yy - 1.6, x1 - 3, yy + 1.6), 24, SK['card'], outline=SK['border'], w=3)
                filled = t >= L(lid, 0.25 + 0.15 * i)
                txt(lay, ('kamu@email.com' if i == 0 else '••••••••') if filled else ph, (x0 + 5, yy), 26, SK['ink'] if filled else SK['gray'], 'Medium', 'lm')
            rr(lay, (x0 + 3, y0 + 23.6, x1 - 3, y0 + 27.0), 24, SK['green']); txt(lay, 'Masuk', (cx, y0 + 25.3), 30, F['white'], 'SemiBold')
            tap(lay, x1 - 6, y0 + 25.3, t, L(lid, 0.7))
            txt(lay, 'contoh tampilan', (cx, y1 - 2.5), 22, SK['gray'], 'Medium')
        elif n == 2:
            topbar(lay, scr)
            rr(lay, (x0 + 2, y0 + 8, x1 - 2, y0 + 18), 30, SK['ink'])
            rr(lay, (x0 + 4, y0 + 10.5, x0 + 16, y0 + 11.5), 6, '#555A5F'); rr(lay, (x0 + 4, y0 + 13.5, x0 + 22, y0 + 15.5), 8, '#3A3E42')
            for i in range(2): rr(lay, (x0 + 2, y0 + 20 + i * 8, x1 - 2, y0 + 26.5 + i * 8), 30, SK['card'], outline=SK['border'], w=2)
            if t >= L(lid, 0.3):
                p = (t - L(lid, 0.3)) * 2.2
                circ(lay, x1 - 5, y0 + 3.3, 36 + 6 * abs(math.sin(p)), None, outline=F['coral'], w=6)
            tap(lay, x1 - 5, y0 + 3.3, t, L(lid, 0.7))
        elif n == 3:
            rr(lay, (x0, y0, x1, y1), 42, F['white'])
            toggle(lay, x0 + 4.5, y0 + 3.3, 0.8); txt(lay, 'Sakelar', (x0 + 9, y0 + 3.3), 30, SK['ink'], 'Bold', 'lm')
            circ(lay, x1 - 5, y0 + 3.3, 27, '#E8E6E0'); line(lay, x1 - 5.9, y0 + 2.8, x1 - 4.1, y0 + 3.8, SK['ink'], 4); line(lay, x1 - 5.9, y0 + 3.8, x1 - 4.1, y0 + 2.8, SK['ink'], 4)
            menu_rows(lay, scr, y0 + 8.5, hl=t >= L(lid, 0.45))
            tap(lay, x1 - 6, y0 + 12.1, t, L(lid, 0.6))
        elif n == 4:
            picked = t >= L(lid, 0.3)
            chat_head(lay, scr, 'Model A (contoh)' if picked else 'pilih model', picked)
            full = 'Ringkas teks ini dong'
            k = clamp((t - L(lid, 0.45)) / 0.3)
            sent = t >= L(lid, 0.85)
            chat_input(lay, scr, '' if sent else full[:int(len(full) * k)], send_hl=k >= 1)
            if not sent: tap(lay, x1 - 4.2, y1 - 3.0, t, L(lid, 0.8))
            if sent:
                p = clamp((t - L(lid, 0.85)) / 0.25)
                rr(lay, (x1 - 25, y0 + 14 - 1 + p, x1 - 2, y0 + 17.2 - 1 + p), 26, SK['green'], a=255 * p)
                txt(lay, full, (x1 - 13.5, y0 + 15.6 - 1 + p), 22, F['white'], 'Medium', a=255 * p)
        else:   # SH10 jawaban muncul
            chat_head(lay, scr, 'Model A (contoh)', True)
            rr(lay, (x1 - 25, y0 + 13, x1 - 2, y0 + 16.2), 26, SK['green'])
            txt(lay, 'Ringkas teks ini dong', (x1 - 13.5, y0 + 14.6), 22, F['white'], 'Medium')
            k = clamp((t - L(lid, 0.15)) / 0.8)
            if k > 0:
                rr(lay, (x0 + 2, y0 + 17.8, x0 + 31, y0 + 26.0), 26, SK['card'], outline=SK['border'], w=2)
                ai_lines(lay, x0 + 4, y0 + 19.6, 4, k, 24)
            chat_input(lay, scr)
        a, sc = appear(t, s['start'] + 0.05)
        comp(im, lay, a, sc, (64, 27))

    elif sid == 'SH11':   # satu dashboard
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); wordmark(lay, 50, 12, 220, tsize=40); comp(im, lay, a, sc, (50, 12))
        items = [('Chat', SK['green'], 0.45), ('Top up', F['blue'], 0.6), ('API keys', F['coral'], 0.82)]
        xs = [22, 50, 78]
        for (lab, col, f_), x in zip(items, xs):
            def f(l, lab=lab, col=col, x=x):
                card(l, (x - 12.5, 24, x + 12.5, 33), r=30)
                txt(l, lab, (x, 28.5), 38, col, 'Bold')
            G(L('L12', f_), f, (x, 28.5))
        a, sc = appear(t, L('L12', 0.25))
        lay = canvas(); badge(lay, 'satu dashboard', 50, 40, F['ink'], F['white'], 36); comp(im, lay, a, sc, (50, 40))

    elif sid == 'SH12':   # tips
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'TIPS PILIH\nMODEL', (50, 18), 86, F['ink'], 'Bold', spacing=4); comp(im, lay, a, sc, (50, 18))
        a, sc = appear(t, L('L13', 0.55))
        lay = canvas(); chip_row(lay, ['ringan', 'besar', 'bandingin'], 36, 38, k=clamp((t - L('L13', 0.55)) / 0.5)); comp(im, lay)

    elif sid == 'SH13':   # tugas simpel → model ringan
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Tugas simpel', (50, 10), 46, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 10))
        def f(l):
            card(l, (8, 15, 42, 35), r=30); doc_icon(l, 25, 22.5, 1.1); txt(l, 'ringkas teks', (25, 31.5), 30, F['ink'], 'SemiBold')
        G(L('L14', 0.1), f, (25, 25))
        k = clamp((t - L('L14', 0.5)) / 0.3)
        if k > 0: lay = canvas(); arrow(lay, 45, 25, 55, 25, k, F['ink2'], 7); comp(im, lay)
        def g(l):
            card(l, (58, 15, 92, 35), r=30, outline=F['mint']); ai_box(l, 75, 22.2, 0.42); txt(l, 'model ringan', (75, 31.5), 30, F['ink'], 'SemiBold')
        G(L('L14', 0.65), g, (75, 25))
        a, sc = appear(t, L('L14', 0.8))
        lay = canvas(); badge(lay, 'cukup yang ringan', 50, 41, F['mint'], F['white'], 34); comp(im, lay, a, sc, (50, 41))

    elif sid == 'SH14':   # tugas berat → model besar
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Tugas berat', (50, 10), 46, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 10))
        def f(l):
            card(l, (8, 15, 42, 35), r=30); rr(l, (14, 18, 36, 27), 20, F['ink']); txt(l, '</>', (25, 22.5), 54, F['mint'])
            txt(l, 'nulis kode', (25, 31.5), 30, F['ink'], 'SemiBold')
        G(L('L15', 0.1), f, (25, 25))
        k = clamp((t - L('L15', 0.45)) / 0.3)
        if k > 0: lay = canvas(); arrow(lay, 45, 25, 55, 25, k, F['ink2'], 7); comp(im, lay)
        def g(l):
            card(l, (58, 15, 92, 35), r=30, outline=F['blue']); ai_box(l, 75, 22.2, 0.62); txt(l, 'model besar', (75, 31.5), 30, F['ink'], 'SemiBold')
        G(L('L15', 0.6), g, (75, 25))
        a, sc = appear(t, L('L15', 0.82))
        lay = canvas(); badge(lay, 'biasanya lebih jago', 50, 41, F['blue'], F['white'], 34); comp(im, lay, a, sc, (50, 41))

    elif sid == 'SH15':   # bandingin dua model
        def q(l):
            rr(l, (24, 8.5, 76, 13.5), 40, SK['green']); txt(l, 'pertanyaan yang sama', (50, 11), 32, F['white'], 'Medium')
        G(s['start'] + 0.1, q, (50, 11))
        k = clamp((t - L('L16', 0.4)) / 0.35)
        if k > 0:
            lay = canvas(); arrow(lay, 40, 14.5, 28, 18.5, k, F['ink2'], 5); arrow(lay, 60, 14.5, 72, 18.5, k, F['ink2'], 5); comp(im, lay)
        for i, (x, lab) in enumerate(((27, 'Model A'), (73, 'Model B'))):
            def f(l, x=x, lab=lab, i=i):
                card(l, (x - 19, 19.5, x + 19, 36), r=30)
                txt(l, lab, (x, 22.6), 32, CHIPC[i], 'Bold')
                ai_lines(l, x - 15, 26.5, 4, clamp((t - L('L16', 0.55)) / 0.6), 28)
            G(L('L16', 0.48 + 0.08 * i), f, (x, 27))
        a, sc = appear(t, L('L16', 0.6))
        lay = canvas(); circ(lay, 50, 27.5, 40, F['yellow']); txt(lay, 'vs', (50, 27.4), 38, F['ink']); comp(im, lay, a, sc, (50, 27.5))
        a, sc = appear(t, L('L16', 0.85))
        lay = canvas(); badge(lay, 'bandingin hasilnya', 50, 41.5, F['ink'], F['white'], 34)
        txt(lay, 'contoh', (88, 38.3), 22, F['ink2'], 'Medium'); comp(im, lay, a, sc, (50, 41.5))

    elif sid == 'SH16':   # menu pemakaian
        def f(l):
            card(l, (10, 9, 90, 38), r=40)
            for i, h in enumerate((1.2, 2.0, 2.8)): rr(l, (15 + i * 1.9, 14.2 - h, 16.3 + i * 1.9, 14.2), 4, SK['ink'])
            txt(l, 'Pemakaian', (23, 12.9), 42, SK['ink'], 'Bold', 'lm')
            line(l, 15, 34, 85, 34, SK['border'], 3)
            hs = [5, 8, 6, 11, 7, 13, 9]
            for i, h in enumerate(hs):
                kk = clamp((t - L('L17', 0.35) - i * 0.06) / 0.4)
                if kk > 0: rr(l, (17 + i * 9.6, 34 - h * ease_out_cubic(kk), 23 + i * 9.6, 34), 10, SK['green'] if i == 5 else F['blue2'])
        G(s['start'] + 0.1, f, (50, 23))
        a, sc = appear(t, L('L17', 0.3))
        lay = canvas(); txt(lay, 'ilustrasi', (50, 42), 24, F['ink2'], 'Medium'); comp(im, lay, a, sc, (50, 42))

    elif sid == 'SH17':   # developer API, kamu chat
        def dev(l):
            rr(l, (5, 10.4, 49, 30.4), 28, F['ink'], a=40); rr(l, (5, 10, 49, 30), 28, F['ink'])
            for i, c in enumerate((F['red'], F['yellow'], F['mint'])): circ(l, 8.5 + i * 2.6, 12.2, 9, c)
            txt(l, 'base_url =', (8, 17), 28, '#C9D3EA', 'Medium', 'lm')
            txt(l, '"api.sakelar.web.id/v1"', (8, 21.2), 26, F['mint'], 'Medium', 'lm')
            txt(l, 'developer: API', (27, 34), 32, F['ink'], 'Bold')
            check(l, 45, 27, 0.7)
        G(L('L18', 0.25), dev, (27, 22))
        def you(l):
            scr = phone(l, (60, 9, 88, 31)); x0, y0, x1, y1 = scr
            rr(l, (x1 - 15, y0 + 3, x1 - 1.5, y0 + 6), 22, SK['green']); txt(l, 'Halo!', (x1 - 8.2, y0 + 4.5), 24, F['white'], 'Medium')
            rr(l, (x0 + 1.5, y0 + 7.5, x0 + 17, y0 + 12.5), 22, SK['card'], outline=SK['border'], w=2); ai_lines(l, x0 + 3, y0 + 9, 2, 1, 11)
            txt(l, 'kamu: Chat', (74, 34), 32, F['ink'], 'Bold')
        G(L('L19', 0.3), you, (74, 22))
        a, sc = appear(t, L('L19', 0.75))
        lay = canvas(); badge(lay, 'tinggal chat', 74, 40, SK['green'], F['white'], 32); comp(im, lay, a, sc, (74, 40))

    elif sid == 'SH18':   # isi hati aku
        a, sc = appear(t, L('L20', 0.45))
        lay = canvas(); heart(lay, 50, 18, 3.4, F['coral']); txt(lay, '?', (50, 21.5), 90, F['white']); comp(im, lay, a, sc, (50, 21))
        for i, (x, y, s_, ph) in enumerate(((20, 32, 1.4, 0), (80, 26, 1.8, 1.1), (86, 40, 1.1, 2.2), (30, 14, 1.0, 3.1))):
            t0 = L('L20', 0.6 + 0.07 * i)
            if t < t0: continue
            p = t - t0
            lay = canvas(); heart(lay, x + 0.6 * math.sin(p * 2 + ph), y - p * 1.5, s_ * (0.7 + 0.3 * ease_out_back(clamp(p / 0.4))))
            comp(im, lay, min(1, p * 3))
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); badge(lay, 'Gampang kan?', 50, 9.5, F['mint'], F['white'], 36); comp(im, lay, a, sc, (50, 9.5))
        a, sc = appear(t, L('L20', 0.75))
        lay = canvas(); txt(lay, 'isi hati aku', (50, 40), 50, F['coral'], 'Bold'); comp(im, lay, a, sc, (50, 40))

    elif sid == 'SH19':   # end card
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        card(lay, (10, 9, 90, 42), r=44)
        wordmark(lay, 50, 15, 240, tsize=50)
        txt(lay, 'Sekarang bisa langsung Chat', (50, 26.5), 38, F['ink'], 'SemiBold')
        rr(lay, (22, 30, 78, 35.5), 40, SK['green']); txt(lay, 'sakelar.web.id', (50, 32.75), 44, F['white'], 'Bold')
        txt(lay, 'Reina Tutorial Ep 03 · Chat AI di Web Sakelar', (50, 39), 28, F['ink2'], 'Medium')
        comp(im, lay, a, sc, (50, 25))


# Per-shot spec: goal, obj, anim (list of (t_rel, text)), text, sfx (list of (t_rel, name, len, dB, fn)), qa
def spec(sid):
    s = SH[sid]; d = round(s['end'] - s['start'], 3)
    if sid == 'SH01': return dict(
        goal='Hook: mau coba model AI tapi nggak bisa ngoding.',
        obj=['Kartu kode gelap x=10–90%, y=9–33% dengan 3 titik jendela + 5 baris kode abstrak.',
             'Tiga lingkaran coral "?" di (78,15), (84,24), (72,28).', 'Badge coral "nggak bisa ngoding?" (50%,40%).'],
        anim=[(0.15, 'Kartu kode pop-in.'), (r(sid, 'L01', 0.35), '"?" pop-in bergantian tiap +12%.'), (r(sid, 'L01', 0.7), 'Badge pop-in.')],
        text=['"?" Bold 46px putih.', '"nggak bisa ngoding?" Medium 40px putih.'],
        sfx=[(0.15, 'pop', 0.15, -16, 'kartu'), (r(sid, 'L01', 0.35), 'blip', 0.5, -18, 'tanda tanya'), (r(sid, 'L01', 0.7), 'boing', 0.25, -16, 'badge')],
        qa=['Reina kiri, balon subtitle kanan.'])
    if sid == 'SH02': return dict(
        goal='Pengumuman: Sakelar AI punya fitur baru Chat.',
        obj=['Logo toggle + "Sakelar AI" via wordmark() 220px (50%,12%).', 'Badge kuning "FITUR BARU" (50%,23.5%).',
             'Balon chat hijau #1F6B52 x=30–70%, y=28–40% berekor kiri bawah, teks "Chat" Bold 70px putih.'],
        anim=[(0.1, 'Logo pop-in.'), (r(sid, 'L02', 0.5), 'Badge FITUR BARU pop-in (saat "fitur baru").'), (r(sid, 'L02', 0.78), 'Balon Chat pop-in (saat "Chat!").')],
        text=['"FITUR BARU" Medium 34px navy.', '"Chat" Bold 70px putih.'],
        sfx=[(0.1, 'jingle', 0.6, -14, 'logo'), (r(sid, 'L02', 0.5), 'sparkle', 0.6, -18, 'fitur baru'), (r(sid, 'L02', 0.78), 'pop_hi', 0.2, -14, 'Chat')],
        qa=['Logo toggle baru lewat wordmark().', 'Posisi closeup: balon Chat (y≤43.5%) tidak menabrak subtitle tengah.'])
    if sid == 'SH03': return dict(
        goal='Dulu: pakai API AI harus nulis kode, bikin API key, pasang di aplikasi.',
        obj=['Badge abu "DULU" (50%,10.5%).', 'Empat kartu 20%×15% di x=15/38.3/61.7/85%, y=15–30%: "</>" + "tulis kode", kunci kuning + "API key", jendela app + "aplikasi", chip AI + "ngobrol sama AI".',
             'Panah abu antar kartu di y=22.5%.', 'Badge coral "harus ngoding dulu" (50%,37%).'],
        anim=[(0.05, 'Badge DULU.'), (r(sid, 'L03', 0.6), 'Kartu "tulis kode".'), (r(sid, 'L04', 0.08), 'Panah + kartu "API key".'),
              (r(sid, 'L04', 0.33), 'Panah + kartu "aplikasi".'), (r(sid, 'L04', 0.75), 'Panah + kartu AI.'), (r(sid, 'L04', 0.85), 'Badge coral.')],
        text=['"DULU" Medium 36px.', 'Label kartu SemiBold 26px / 22px.', '"harus ngoding dulu" Medium 34px.'],
        sfx=[(r(sid, 'L03', 0.6), 'clicks', 0.5, -18, 'kode'), (r(sid, 'L04', 0.08), 'pop', 0.15, -16, 'API key'),
             (r(sid, 'L04', 0.33), 'pop', 0.15, -16, 'aplikasi'), (r(sid, 'L04', 0.75), 'pop_hi', 0.15, -16, 'AI'), (r(sid, 'L04', 0.85), 'buzz', 0.25, -20, 'ribet')],
        qa=['Pose desk = tengah; kartu tidak menutupi monitor/subtitle.'])
    if sid == 'SH04': return dict(
        goal='Sekarang: cukup buka web, langsung chat.',
        obj=['Badge hijau "SEKARANG" (50%,10.5%).', 'Mockup HP x=30–70%, y=14–46%: top bar (toggle + "Sakelar" + tombol ☰), balon user hijau "Halo!", balon jawaban putih dengan baris abu, kolom "Tulis pesan…" + tombol kirim.'],
        anim=[(0.05, 'Badge.'), (r(sid, 'L05', 0.35), 'HP pop-in (saat "buka webnya").'), (r(sid, 'L05', 0.75), 'Balon jawaban muncul, baris abu tumbuh 0.5 s.')],
        text=['"SEKARANG" Medium 36px.', '"Halo!" Medium 26px.', '"Tulis pesan…" Medium 24px abu.'],
        sfx=[(r(sid, 'L05', 0.35), 'whoosh', 0.4, -18, 'HP'), (r(sid, 'L05', 0.75), 'blip', 0.2, -16, 'balasan')],
        qa=['Reina kanan; balon subtitle kiri y≈60% tidak menabrak HP (y≤46.5%).'])
    if sid == 'SH05': return dict(
        goal='Transisi ke tutorial: cuma 4 langkah.',
        obj=['Judul 2 baris "CUMA / 4 LANGKAH" Bold 86px (50%,18%).', 'Lingkaran r=50px angka 1–4 di x=23/41/59/77%, y=35.5%.'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L06', 0.45), 'Lingkaran pop-in tiap +12%.')],
        text=['"CUMA\\n4 LANGKAH"', '"1" "2" "3" "4" Bold 58px.'],
        sfx=[(r(sid, 'L06', 0.45), 'pop_hi', 0.6, -14, 'angka')], qa=['Judul tidak terpotong.'])
    if sid in ('SH06', 'SH07', 'SH08', 'SH09', 'SH10'):
        n = {'SH06': 1, 'SH07': 2, 'SH08': 3, 'SH09': 4, 'SH10': 0}[sid]
        lid = {'SH06': 'L07', 'SH07': 'L08', 'SH08': 'L09', 'SH09': 'L10', 'SH10': 'L11'}[sid]
        head = ('Kolom kiri: lingkaran nomor "' + str(n) + '" r=62px (20%,15%) + label Bold 40px 2 baris (20%,25.5%).') if n else \
               'Kolom kiri: ✓ hijau besar (20%,15%) + "Jawaban / langsung / muncul" Bold 40px (20%,27%).'
        hp = 'Mockup HP x=42–86%, y=8–46% (layar terang #F3F2EE, bingkai #1B1D1F).'
        if n == 1: return dict(goal='Langkah 1: login ke dashboard Sakelar.',
            obj=[head, hp, 'Layar login: toggle besar + "Sakelar", field "email" & "password", tombol hijau "Masuk", teks kecil "contoh tampilan".'],
            anim=[(0.05, 'Kolom kiri + HP pop-in.'), (r(sid, lid, 0.25), 'Field email terisi "kamu@email.com".'), (r(sid, lid, 0.4), 'Field password terisi "••••••••".'),
                  (r(sid, lid, 0.7), 'Ketuk tombol Masuk (titik coral + cincin melebar 0.5 s).')],
            text=['"Login ke\\ndashboard"', '"email" / "password" / "kamu@email.com" Medium 26px.', '"Masuk" SemiBold 30px.', '"contoh tampilan" 22px abu.'],
            sfx=[(0.05, 'swipe', 0.3, -18, 'HP'), (r(sid, lid, 0.25), 'clicks', 0.4, -18, 'ketik'), (r(sid, lid, 0.7), 'click', 0.1, -14, 'Masuk')],
            qa=['Tampilan login generik (lihat daftar konfirmasi).'])
        if n == 2: return dict(goal='Langkah 2: ketuk tombol menu bulat di pojok kanan atas.',
            obj=[head, hp, 'Layar dashboard: top bar (toggle + "Sakelar" + tombol ☰ hitam di kanan), kartu gelap besar + 2 kartu terang (isi disamarkan).',
                 'Cincin coral berdenyut di tombol ☰.'],
            anim=[(0.05, 'Kolom kiri + HP.'), (r(sid, lid, 0.3), 'Cincin coral berdenyut di tombol menu (saat "tombol menu").'), (r(sid, lid, 0.7), 'Ketuk tombol menu.')],
            text=['"Ketuk\\ntombol menu"', '"Sakelar" Bold 30px.'],
            sfx=[(r(sid, lid, 0.3), 'tick', 0.3, -20, 'sorot'), (r(sid, lid, 0.7), 'click', 0.1, -14, 'ketuk')],
            qa=['Posisi tombol menu = pojok kanan atas, sama dengan screenshot user.'])
        if n == 3: return dict(goal='Langkah 3: pilih menu Chat, tepat di bawah Ringkasan.',
            obj=[head, hp, 'Layar menu putih: toggle + "Sakelar" + tombol ✕; daftar Ringkasan (aktif, pil hitam), Chat, Top up, Shop, API keys, Model, Pemakaian.',
                 'Baris "Chat" disorot hijau muda + outline #1F6B52.'],
            anim=[(0.05, 'Kolom kiri + HP.'), (r(sid, lid, 0.45), 'Baris Chat disorot (saat "Chat").'), (r(sid, lid, 0.6), 'Ketuk baris Chat.')],
            text=['"Pilih\\nChat"', 'Item menu Medium 30px (urutan persis screenshot).'],
            sfx=[(r(sid, lid, 0.45), 'ding', 0.4, -16, 'sorot Chat'), (r(sid, lid, 0.6), 'click', 0.1, -14, 'ketuk')],
            qa=['Urutan menu sama dengan screenshot.'])
        if n == 4: return dict(goal='Langkah 4: pilih model, ketik pertanyaan, kirim.',
            obj=[head, hp, 'Layar Chat: top bar, judul "Chat", dropdown model (kanan) "pilih model" → "Model A (contoh)".',
                 'Kolom input diketik "Ringkas teks ini dong", tombol kirim hijau, lalu balon user hijau muncul di atas.'],
            anim=[(0.05, 'Kolom kiri + HP.'), (r(sid, lid, 0.3), 'Dropdown berubah jadi "Model A (contoh)" dengan outline hijau (saat "pilih modelnya").'),
                  (r(sid, lid, 0.45), 'Teks diketik 0.3 s.'), (r(sid, lid, 0.8), 'Ketuk tombol kirim.'), (r(sid, lid, 0.85), 'Balon user turun & muncul 0.25 s, input kosong lagi.')],
            text=['"Pilih model,\\nketik, kirim"', '"pilih model" / "Model A (contoh)" Medium 24px — PLACEHOLDER.', '"Ringkas teks ini dong" Medium 24px/22px.'],
            sfx=[(r(sid, lid, 0.3), 'pop', 0.15, -16, 'model'), (r(sid, lid, 0.45), 'clicks', 0.3, -18, 'ketik'), (r(sid, lid, 0.82), 'swipe', 0.3, -16, 'kirim')],
            qa=['Nama model placeholder; cek apakah ada pemilih model (konfirmasi).'])
        return dict(goal='Hasil: jawaban AI langsung muncul.',
            obj=[head, hp, 'Layar Chat sama seperti SH09: balon user hijau + balon jawaban putih (x0+2…x0+31%) dengan 4 baris abu yang tumbuh.'],
            anim=[(0.05, 'HP.'), (r(sid, lid, 0.15), 'Balon jawaban muncul, baris abu tumbuh 0.8 s.'), (r(sid, lid, 0.3), 'Kolom kiri ✓ + teks pop-in.')],
            text=['"Jawaban\\nlangsung\\nmuncul" Bold 40px.'],
            sfx=[(r(sid, lid, 0.15), 'blip', 0.2, -16, 'balasan'), (r(sid, lid, 0.3), 'chime', 0.6, -14, 'berhasil')],
            qa=['Closeup: subtitle tengah tidak menabrak HP (y≤46.5%).', 'Isi jawaban disamarkan (baris abu), tidak ada klaim jawaban.'])
    if sid == 'SH11': return dict(
        goal='Semua ada di satu dashboard: Chat, Top up, API keys.',
        obj=['wordmark() 220px (50%,12%).', 'Tiga kartu 25%×9% di x=22/50/78%, y=24–33%: "Chat" hijau, "Top up" biru, "API keys" coral (Bold 38px).', 'Badge navy "satu dashboard" (50%,40%).'],
        anim=[(0.05, 'Logo.'), (r(sid, 'L12', 0.25), 'Badge.'), (r(sid, 'L12', 0.45), 'Kartu Chat.'), (r(sid, 'L12', 0.6), 'Kartu Top up.'), (r(sid, 'L12', 0.82), 'Kartu API keys.')],
        text=['"Chat" / "Top up" / "API keys" Bold 38px.', '"satu dashboard" Medium 36px.'],
        sfx=[(0.05, 'jingle', 0.6, -16, 'logo'), (r(sid, 'L12', 0.45), 'pop', 0.15, -16, 'Chat'), (r(sid, 'L12', 0.6), 'pop', 0.15, -16, 'Top up'), (r(sid, 'L12', 0.82), 'pop_hi', 0.15, -16, 'API keys')],
        qa=['Nama menu persis seperti di dashboard.'])
    if sid == 'SH12': return dict(
        goal='Transisi ke tips memilih model.',
        obj=['Judul "TIPS PILIH / MODEL" Bold 86px (50%,18%).', 'Chip row "ringan" / "besar" / "bandingin" di y=36%.'],
        anim=[(0.05, 'Judul.'), (r(sid, 'L13', 0.55), 'Chip muncul berurutan 0.5 s.')],
        text=['"TIPS PILIH\\nMODEL"', 'Chip Medium 38px.'], sfx=[(0.05, 'whoosh', 0.4, -18, 'judul'), (r(sid, 'L13', 0.55), 'pop_hi', 0.5, -16, 'chip')], qa=['Judul tidak terpotong.'])
    if sid == 'SH13': return dict(
        goal='Tips 1: tugas simpel (ringkas teks) cukup model ringan.',
        obj=['Judul "Tugas simpel" (50%,10%).', 'Kartu kiri x=8–42%, y=15–35%: ikon dokumen + "ringkas teks".', 'Panah 45→55% (y=25%).',
             'Kartu kanan outline mint x=58–92%: chip AI kecil (skala 0.42) + "model ringan".', 'Badge mint "cukup yang ringan" (50%,41%).'],
        anim=[(0.05, 'Judul.'), (r(sid, 'L14', 0.1), 'Kartu kiri.'), (r(sid, 'L14', 0.5), 'Panah 0.3 s.'), (r(sid, 'L14', 0.65), 'Kartu kanan.'), (r(sid, 'L14', 0.8), 'Badge.')],
        text=['"Tugas simpel" Bold 46px.', 'Label SemiBold 30px.', 'Badge Medium 34px.'],
        sfx=[(r(sid, 'L14', 0.1), 'pop', 0.15, -16, 'tugas'), (r(sid, 'L14', 0.65), 'ding', 0.4, -16, 'model ringan')],
        qa=['Tidak menyebut nama model asli.'])
    if sid == 'SH14': return dict(
        goal='Tips 2: tugas berat (nulis kode) — model lebih besar biasanya lebih jago.',
        obj=['Judul "Tugas berat" (50%,10%).', 'Kartu kiri: layar gelap "</>" mint + "nulis kode".', 'Panah 45→55%.',
             'Kartu kanan outline biru: chip AI besar (skala 0.62) + "model besar".', 'Badge biru "biasanya lebih jago" (50%,41%).'],
        anim=[(0.05, 'Judul.'), (r(sid, 'L15', 0.1), 'Kartu kiri.'), (r(sid, 'L15', 0.45), 'Panah.'), (r(sid, 'L15', 0.6), 'Kartu kanan.'), (r(sid, 'L15', 0.82), 'Badge.')],
        text=['"Tugas berat" Bold 46px.', '"biasanya lebih jago" Medium 34px.'],
        sfx=[(r(sid, 'L15', 0.1), 'clicks', 0.4, -18, 'kode'), (r(sid, 'L15', 0.6), 'chime', 0.5, -16, 'model besar')],
        qa=['Klaim memakai "biasanya", tidak mutlak.', 'Closeup: semua elemen ≤ y 43%.'])
    if sid == 'SH15': return dict(
        goal='Tips 3: tanya hal yang sama ke dua model lalu bandingkan.',
        obj=['Pil hijau "pertanyaan yang sama" x=24–76%, y=8.5–13.5%.', 'Dua panah ke kartu "Model A" (x=8–46%) & "Model B" (x=54–92%), y=19.5–36%, isi baris abu.',
             'Lingkaran kuning "vs" (50%,27.5%).', 'Badge navy "bandingin hasilnya" (50%,41.5%) + teks "contoh".'],
        anim=[(0.1, 'Pil pertanyaan.'), (r(sid, 'L16', 0.4), 'Panah 0.35 s.'), (r(sid, 'L16', 0.48), 'Kartu A, B (+8%), baris jawaban tumbuh 0.6 s.'), (r(sid, 'L16', 0.6), '"vs".'), (r(sid, 'L16', 0.85), 'Badge.')],
        text=['"pertanyaan yang sama" Medium 32px.', '"Model A" / "Model B" Bold 32px (contoh).', '"vs" 38px.', '"bandingin hasilnya" Medium 34px.'],
        sfx=[(0.1, 'pop', 0.15, -16, 'pertanyaan'), (r(sid, 'L16', 0.48), 'whoosh', 0.4, -18, 'dua model'), (r(sid, 'L16', 0.6), 'boing', 0.25, -16, 'vs')],
        qa=['Nama model placeholder.'])
    if sid == 'SH16': return dict(
        goal='Pemakaian bisa dipantau di menu Pemakaian.',
        obj=['Kartu putih x=10–90%, y=9–38%: ikon batang kecil + judul "Pemakaian"; 7 batang (biru muda, batang ke-6 hijau) di atas garis y=34%.', 'Teks "ilustrasi" (50%,42%).'],
        anim=[(0.1, 'Kartu pop-in.'), (r(sid, 'L17', 0.35), 'Batang tumbuh berurutan (jeda 0.06 s, 0.4 s easeOutCubic).')],
        text=['"Pemakaian" Bold 42px.', '"ilustrasi" Medium 24px abu.'],
        sfx=[(0.1, 'pop', 0.15, -16, 'kartu'), (r(sid, 'L17', 0.35), 'stack', 0.6, -18, 'batang')],
        qa=['Tanpa angka pemakaian.', 'Menu "Pemakaian" sesuai dashboard.'])
    if sid == 'SH17': return dict(
        goal='Rangkuman: developer tetap pakai API, yang mau coba tinggal chat.',
        obj=['Kartu kode gelap x=5–49%, y=10–30%: `base_url =` / `"api.sakelar.web.id/v1"` + ✓; label "developer: API" (27%,34%).',
             'HP kecil x=60–88%, y=9–31%: balon "Halo!" + balon jawaban; label "kamu: Chat" (74%,34%).', 'Badge hijau "tinggal chat" (74%,40%).'],
        anim=[(r(sid, 'L18', 0.25), 'Kartu developer pop-in.'), (r(sid, 'L19', 0.3), 'HP pop-in.'), (r(sid, 'L19', 0.75), 'Badge.')],
        text=['Kode Medium 28/26px (verbatim).', 'Label Bold 32px.', '"tinggal chat" Medium 32px.'],
        sfx=[(r(sid, 'L18', 0.25), 'clicks', 0.4, -18, 'kode'), (r(sid, 'L19', 0.3), 'swipe', 0.3, -16, 'HP'), (r(sid, 'L19', 0.75), 'ding', 0.4, -16, 'badge')],
        qa=['Base URL persis "api.sakelar.web.id/v1".', 'Reina kanan; balon subtitle kiri tidak menabrak elemen (y≤41.5%).'])
    if sid == 'SH18': return dict(
        goal='Punchline manis: lebih gampang daripada nebak isi hati Reina.',
        obj=['Badge mint "Gampang kan?" (50%,9.5%).', 'Hati coral besar (50%,18%) berisi "?" putih.', '4 hati kecil melayang.', 'Teks "isi hati aku" Bold 50px coral (50%,40%).'],
        anim=[(0.1, 'Badge.'), (r(sid, 'L20', 0.45), 'Hati "?" pop-in.'), (r(sid, 'L20', 0.6), 'Hati kecil tiap +7%, naik 1.5%/s.'), (r(sid, 'L20', 0.75), 'Teks pop-in.')],
        text=['"Gampang kan?" Medium 36px.', '"?" 90px putih.', '"isi hati aku" Bold 50px coral.'],
        sfx=[(0.1, 'pop', 0.15, -16, 'badge'), (r(sid, 'L20', 0.45), 'boing', 0.25, -16, 'hati'), (r(sid, 'L20', 0.6), 'sparkle', 1.0, -18, 'hati melayang')],
        qa=['Mulut sprite smile.', 'Posisi closeup.'])
    if sid == 'SH19': return dict(
        goal='End card: ajakan mencoba fitur Chat di Sakelar AI.',
        obj=['Kartu putih x=10–90%, y=9–42%.', 'wordmark() 240px (50%,15%).', '"Sekarang bisa langsung Chat" (50%,26.5%).',
             'Tombol hijau #1F6B52 x=22–78%, y=30–35.5% "sakelar.web.id".', '"Reina Tutorial Ep 03 · Chat AI di Web Sakelar" (50%,39%).'],
        anim=[(0.05, 'Kartu pop-in.'), (round(d - 0.5, 3), 'Fade ke warna latar 0.5 s.')],
        text=['"Sekarang bisa langsung Chat" SemiBold 38px.', '"sakelar.web.id" Bold 44px putih.', 'Judul episode Medium 28px abu.'],
        sfx=[(0.05, 'stinger', 1.2, -12, 'end card'), (0.1, 'jingle', 0.6, -16, 'logo')],
        qa=['URL — cek konfirmasi (sakelar.web.id vs app.sakelar.web.id).', 'Logo toggle baru.'])
