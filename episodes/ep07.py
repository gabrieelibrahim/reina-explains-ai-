"""Reina Explains AI — Episode 07: "Kok Jawaban AI Beda-beda?" (temperature & unsur acak).
Satu file = satu episode: naskah, shot, pose, visual panel(t), spec storyboard + SFX, arahan VO.
Jalankan:  python run.py stage1 episodes/ep07.py   lalu   python run.py stage2 episodes/ep07.py <zip_suara>"""
import math
from PIL import Image, ImageDraw
from reina import *

EP = 7
TITLE = 'Kok Jawaban AI Beda-beda?'
SCENES = {1: 'Hook', 2: 'AI menebak kata', 3: 'Temperature', 4: 'Fakta unik', 5: 'Tips konsisten',
          6: 'Soft sell Sakelar AI', 7: 'Closing', 8: 'End card'}
META = dict(
    tujuan='Menjelaskan kenapa jawaban AI bisa beda untuk pertanyaan sama (prediksi kata + unsur acak + temperature); soft sell Sakelar AI sebagai satu pintu ke banyak model',
    konsep=('Hook: tanya hal sama dua kali, jawaban beda → "AI-nya galau?" → bukan error → AI menebak kata berikutnya, tiap pilihan punya peluang, '
            'kadang "kocok dadu" → setelan temperature (rendah = konsisten, tinggi = kreatif/ngelantur) → fakta unik: temperature paling rendah pun '
            'nggak selalu sama persis → 3 cara biar konsisten → soft sell: banyak model lewat satu pintu, tiap model punya gaya, paket token per model → punchline manis.'),
    fakta=['Model bahasa menyusun jawaban dengan memprediksi token/kata berikutnya berdasarkan peluang.',
           'Temperature = setelan tingkat acak saat memilih kata; rendah → lebih konsisten, tinggi → lebih variatif.',
           'Temperature rendah pun tidak menjamin hasil 100% identik (disebut "nggak selalu", tidak mutlak).',
           'Sakelar AI = satu pintu (gateway) ke banyak model; token dijual dalam paket per model (sekian juta token / "M").',
           'CTA URL: app.sakelar.web.id.'],
    asumsi=['Persentase peluang di SH06 (nasi 60% / bakso 25% / mie 15%) adalah ilustrasi — label "angka ilustrasi" selalu tampil.',
            'Contoh jawaban nama kucing (Mochi, Kopi, dst.) adalah ilustrasi, bukan output model sungguhan.',
            'Rentang nilai temperature tidak disebut karena beda tiap penyedia/model; sebagian model juga mungkin tidak membuka setelan ini.',
            'Tidak diklaim bahwa Sakelar AI menyediakan setelan temperature — tips 3 ditulis umum "kalau pakai API".'],
    konfirmasi=['Nama model & gaya jawaban di SH17 masih placeholder ("Model A/B/C — kalem/kreatif/ringkas", contoh).',
                'Isi paket di SH18 masih "??M token (contoh)" — ganti kalau ada data resmi.'],
    softsell='SH16–SH18 + end card',
)
PRON = [('AI', 'ei-ai'), ('temperature', 'tem-pe-re-cer'), ('API', 'ei-pi-ai'), ('error', 'e-ror'),
        ('Sakelar', 'sa-ke-lar')]
VO_DIR = {'L01': 'santai, heran, nada naik di "beda?"', 'L02': 'bercanda, bisik curiga di "galau"',
 'L03': 'menenangkan, senyum, tekan "bukan error"', 'L04': 'menjelaskan, pelan di "satu per satu"',
 'L05': 'ritmis, sebut "nasi, bakso, mie" seperti menghitung', 'L06': 'jelas, tekan "paling besar" lalu "tetap ada kesempatan"',
 'L07': 'nada "nah", agak jahil di "kocok dadu"', 'L08': 'menjelaskan, sebut "temperature" jelas (tem-pe-re-cer)',
 'L09': 'tenang, datar, "konsisten dan aman"', 'L10': 'lebih ekspresif, naik di "kreatif", turun lucu di "ngelantur"',
 'L11': 'nada "fakta seru", semangat di "Dan nih"', 'L12': 'menenangkan, santai', 'L13': 'energik, membuka daftar',
 'L14': 'tegas tapi ramah', 'L15': 'ringan', 'L16': 'dua bagian: tenang di "turunkan", semangat di "ide liar? naikkan aja"',
 'L17': 'ramah, nada "nah" naik', 'L18': 'santai, "kalem" pelan, "kreatif" ceria', 'L19': 'meyakinkan, santai',
 'L20': 'menjelaskan, "M" tidak disebut — cukup "juta token"', 'L21': 'menyimpulkan, mantap',
 'L22': 'malu-malu manis, pelan, jeda di "Beda sama aku...", senyum di "nggak pernah berubah"'}

# ---- naskah terkunci (1 item = 1 baris VO = L01, L02, ...) ----
LINES = [
 'Pernah nanya hal yang sama ke AI dua kali, tapi jawabannya beda?',
 'Jangan-jangan AI-nya lagi galau?',
 'Tenang, itu bukan error. Memang begitu cara kerjanya.',
 'AI nulis jawaban dengan menebak kata berikutnya, satu per satu.',
 'Misalnya "Aku mau makan...". Lanjutannya bisa nasi, bakso, atau mie.',
 'Tiap pilihan punya peluang. Nasi mungkin paling besar, tapi yang lain tetap ada kesempatan.',
 'Nah, AI nggak selalu ambil yang paling besar. Kadang dia "kocok dadu" dulu.',
 'Seberapa berani dia ngocok, diatur sama setelan namanya temperature.',
 'Temperature rendah: jawabannya lebih konsisten dan aman.',
 'Temperature tinggi: lebih kreatif dan variatif, tapi bisa ngelantur.',
 'Dan nih, di temperature paling rendah pun, jawabannya nggak selalu sama persis.',
 'Jadi jawaban beda itu wajar, bukan tanda AI-nya rusak.',
 'Tiga cara biar jawabannya lebih konsisten.',
 'Satu, kasih instruksi yang jelas dan detail.',
 'Dua, kasih contoh format jawaban yang kamu mau.',
 'Tiga, kalau pakai API, turunkan temperature-nya. Butuh ide liar? Naikkan aja.',
 'Nah, di Sakelar AI, kamu bisa akses banyak model AI lewat satu pintu.',
 'Tiap model juga punya gaya jawaban sendiri. Ada yang kalem, ada yang kreatif.',
 'Jadi kamu bisa coba beberapa model, lalu pilih yang paling cocok.',
 'Tokennya dijual dalam paket per model, isinya sekian juta token.',
 'Jadi AI itu bukan plin-plan, cuma punya sedikit unsur acak.',
 'Beda sama aku... jawabanku buat kamu nggak pernah berubah kok.',
]

# (id, scene, judul, [nomor baris], jeda_awal_s, jeda_akhir_s)
SHOTS = [
 ('SH01', 1, 'Pertanyaan sama, jawaban beda', [1], 0.5, 0.2),
 ('SH02', 1, 'AI-nya galau?', [2], 0.15, 0.2),
 ('SH03', 1, 'Bukan error, cara kerja', [3], 0.15, 0.4),
 ('SH04', 2, 'Menebak kata berikutnya', [4], 0.25, 0.2),
 ('SH05', 2, 'Aku mau makan... nasi/bakso/mie', [5], 0.15, 0.2),
 ('SH06', 2, 'Tiap pilihan punya peluang', [6], 0.15, 0.2),
 ('SH07', 2, 'Kocok dadu', [7], 0.15, 0.4),
 ('SH08', 3, 'Setelan temperature', [8], 0.25, 0.2),
 ('SH09', 3, 'Temperature rendah', [9], 0.15, 0.2),
 ('SH10', 3, 'Temperature tinggi', [10], 0.15, 0.4),
 ('SH11', 4, 'Paling rendah pun bisa beda', [11, 12], 0.25, 0.4),
 ('SH12', 5, 'Tiga cara biar konsisten', [13], 0.25, 0.15),
 ('SH13', 5, 'Tips 1: instruksi jelas', [14], 0.1, 0.2),
 ('SH14', 5, 'Tips 2: contoh format', [15], 0.1, 0.2),
 ('SH15', 5, 'Tips 3: atur temperature', [16], 0.1, 0.4),
 ('SH16', 6, 'Banyak model, satu pintu', [17], 0.25, 0.2),
 ('SH17', 6, 'Tiap model punya gaya', [18], 0.1, 0.2),
 ('SH18', 6, 'Coba, pilih, paket token', [19, 20], 0.1, 0.4),
 ('SH19', 7, 'Bukan plin-plan', [21], 0.25, 0.25),
 ('SH20', 7, 'Jawabanku nggak berubah', [22], 0.1, 0.6),
 ('SH21', 8, 'End card', [], 0.0, 2.5),
]

POSE = {'SH01': 'phone', 'SH02': 'think', 'SH03': 'point_up', 'SH04': 'point', 'SH05': 'point_up', 'SH06': 'arms34',
        'SH07': 'hands_on_hips', 'SH08': 'desk', 'SH09': 'point_up', 'SH10': 'arms34', 'SH11': 'point',
        'SH12': 'hands_on_hips', 'SH13': 'point_up', 'SH14': 'thumbs_up', 'SH15': 'arms34', 'SH16': 'wave',
        'SH17': 'phone', 'SH18': 'thumbs_up', 'SH19': 'hands_on_hips', 'SH20': 'shy_lean', 'SH21': 'wave'}
SMILE = {'SH20'}   # shot yang pakai mulut senyum
EXPR = {'SH01': 'heran sambil lihat HP', 'SH02': 'bingung, tangan di dagu', 'SH03': 'menenangkan, menjelaskan',
        'SH04': 'serius, menunjuk penonton', 'SH05': 'menjelaskan', 'SH06': 'analitis',
        'SH07': 'jahil, percaya diri', 'SH08': 'fokus ke monitor', 'SH09': 'tenang, menjelaskan', 'SH10': 'ekspresif, analitis',
        'SH11': 'semangat, "dan nih"', 'SH12': 'percaya diri', 'SH13': 'menjelaskan', 'SH14': 'ceria', 'SH15': 'tegas',
        'SH16': 'ramah, menyapa', 'SH17': 'menjelaskan sambil lihat HP', 'SH18': 'ceria, meyakinkan',
        'SH19': 'santai, menutup', 'SH20': 'malu-malu, senyum (mulut smile)', 'SH21': 'ceria, melambai'}


# ---------------- helper lokal ----------------
def mix(c1, c2, k):
    a, b = rgba(c1), rgba(c2)
    return '#%02X%02X%02X' % tuple(int(lerp(a[i], b[i], k)) for i in range(3))

def slider(l, x0, x1, y, k, labels=True, size=28):
    """Slider temperature: track gradasi biru→coral, knob di posisi k (0..1)."""
    n = 24; seg = (x1 - x0) / n
    for i in range(n):
        rr(l, (x0 + i * seg - 0.15, y - 0.55, x0 + (i + 1) * seg + 0.15, y + 0.55), 6, mix(F['blue'], F['coral'], i / (n - 1)))
    circ(l, x0, y, 11, F['blue']); circ(l, x1, y, 11, F['coral'])
    kx = lerp(x0, x1, clamp(k))
    circ(l, kx, y + 0.25, 30, F['ink'], a=45); circ(l, kx, y, 30, F['white'], outline=F['ink'], w=6)
    circ(l, kx, y, 11, mix(F['blue'], F['coral'], clamp(k)))
    if labels:
        txt(l, 'rendah', (x0, y + 3.0), size, F['blue'], 'SemiBold', 'lm')
        txt(l, 'tinggi', (x1, y + 3.0), size, F['coral'], 'SemiBold', 'rm')

PIPS = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
        5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}
def dice(l, cx, cy, px, n, col=F['white'], pip=F['ink']):
    """Dadu flat: sisi px piksel (1080-scale), wajah n."""
    hx, hy = px / 2 / W * 100, px / 2 / H * 100
    rr(l, (cx - hx, cy - hy + 0.4, cx + hx, cy + hy + 0.4), px * 0.18, F['ink'], a=50)
    rr(l, (cx - hx, cy - hy, cx + hx, cy + hy), px * 0.18, col, outline=F['ink'], w=5)
    for dx, dy in PIPS[n]:
        circ(l, cx + dx * hx * 0.52, cy + dy * hy * 0.52, px * 0.085, pip)

def cloud(l, cx, cy, s=1.0, col=F['ink2']):
    for dx, dy, r_ in ((-5, 0.6, 46), (0, -0.6, 58), (5.2, 0.5, 44), (-2, 1.4, 44), (2.5, 1.4, 44)):
        circ(l, cx + dx * s, cy + dy * s, r_ * s, col)


def panel(t, sid, im):
    """Gambar panel visual (area y 7–47%) shot sid pada waktu t ke layer 2x im."""
    s = SH[sid]; u = t - s['start']; L = lambda lid, f=0.0: rel(lid, f)
    def G(t0, fn, anchor=(50, 25), d=0.35, dy=0.0):
        a, sc = appear(t, t0, d)
        if a <= 0: return
        lay = canvas(); fn(lay); comp(im, lay, a, sc, anchor, dy)

    if sid == 'SH01':   # same question twice, different answers
        Q = 'Kasih 1 ide nama kucing'
        for i, (y, ans, f_) in enumerate(((9.5, 'Mochi', 0.05), (25.0, 'Kopi', 0.45))):
            def f(l, y=y, ans=ans, i=i):
                badge(l, f'Tanya #{i + 1}', 14, y + 2.4, F['ink'], F['white'], 24)
                bubble(l, (30, y, 92, y + 5), Q, 'u', size=32)
                bubble(l, (8, y + 7, 46, y + 12), ans, 'a', size=36)
                txt(l, 'AI', (50, y + 9.5), 26, F['ink2'], 'SemiBold', 'lm')
            G(L('L01', f_) if i else s['start'] + 0.15, f, (50, y + 6))
        a, sc = appear(t, L('L01', 0.85))
        lay = canvas(); badge(lay, 'kok beda?', 76, 37.5, F['coral'], F['white'], 34); comp(im, lay, a, sc, (76, 37.5))
        a, sc = appear(t, L('L01', 0.75))
        lay = canvas(); circ(lay, 76, 22.2, 34, F['yellow']); txt(lay, '≠', (76, 22.2), 52, F['ink']); comp(im, lay, a, sc, (76, 22.2))

    elif sid == 'SH02':   # AI galau: rain cloud
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); ai_box(lay, 50, 30, 0.85); comp(im, lay, a, sc, (50, 30))
        a2, sc2 = appear(t, L('L02', 0.15))
        lay = canvas()
        for i in range(9):   # rain: pure function of t
            x = 42 + (i % 5) * 4 + (i // 5) * 2
            yy = 16.5 + ((t * 9 + i * 1.7) % 6.0)
            line(lay, x, yy, x - 0.4, yy + 1.2, F['blue'], 5, a=200)
        cloud(lay, 50, 13.5, 1.0)
        comp(im, lay, a2, sc2, (50, 14))
        a3, sc3 = appear(t, L('L02', 0.55))
        lay = canvas(); badge(lay, 'lagi galau?', 50, 41.5, F['coral'], F['white'], 36); comp(im, lay, a3, sc3, (50, 41.5))
        for i, (x, y, ph) in enumerate(((20, 22, 0), (80, 18, 1.4), (78, 34, 2.6))):
            a, sc = appear(t, L('L02', 0.1 + 0.15 * i))
            lay = canvas(); txt(lay, '?', (x, y + 0.6 * math.sin(t * 3 + ph)), 80, F['coral']); comp(im, lay, a, sc, (x, y))

    elif sid == 'SH03':   # not an error, it's how it works
        def left(l):
            card(l, (7, 11, 47, 35), r=36)
            cross(l, 27, 18.5, 1.3)
            txt(l, 'error', (27, 27), 50, F['ink2'], 'Bold')
            line(l, 16, 27.2, 38, 27.2, F['red'], 7)
        G(L('L03', 0.12), left, (27, 23))
        def right(l):
            card(l, (53, 11, 93, 35), r=36, outline=F['mint'])
            check(l, 73, 18.5, 1.3)
            txt(l, 'cara\nkerjanya', (73, 27.6), 42, F['ink'], 'Bold', spacing=4)
        G(L('L03', 0.55), right, (73, 23))
        a, sc = appear(t, L('L03', 0.7))
        lay = canvas(); badge(lay, 'normal kok', 50, 41.5, F['mint'], F['white'], 36); comp(im, lay, a, sc, (50, 41.5))

    elif sid == 'SH04':   # predict next word, one by one
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); txt(lay, 'AI menebak kata berikutnya', (50, 11.5), 44, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 11.5))
        lay = canvas(); card(lay, (8, 16, 92, 27), r=32); comp(im, lay, a, sc, (50, 21))
        k = clamp((t - L('L04', 0.25)) / max(0.3, L('L04', 0.85) - L('L04', 0.25)))
        lay = canvas()
        chip_row(lay, ['Aku', 'mau', 'makan', '???'], 21.5, 44, gap=1.6, k=k,
                 cols=[F['blue'], F['blue'], F['blue'], F['coral']])
        comp(im, lay)
        if k >= 1 and (int((t - s['start']) * 3) % 2 == 0):   # blinking cursor right after last chip
            tot = sum((tw_px(p_, 44) + 44) / W * 100 for p_ in ['Aku', 'mau', 'makan', '???']) + 1.6 * 3
            cx_ = 50 + tot / 2 + 1.6
            lay = canvas(); rr(lay, (cx_, 19.3, cx_ + 0.8, 23.7), 2, F['ink']); comp(im, lay)
        a2, sc2 = appear(t, L('L04', 0.8))
        lay = canvas(); arrow(lay, 50, 28.5, 50, 33, 1, F['ink2'])
        badge(lay, 'satu kata per langkah', 50, 37.5, F['ink'], F['white'], 34); comp(im, lay, a2, sc2, (50, 35))

    elif sid == 'SH05':   # Aku mau makan... -> nasi/bakso/mie
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); card(lay, (14, 8.8, 86, 15.6), r=32); txt(lay, '"Aku mau makan..."', (50, 12.2), 46, F['ink'], 'Bold')
        comp(im, lay, a, sc, (50, 12))
        for i, (w_, x, f_) in enumerate((('nasi', 22, 0.55), ('bakso', 50, 0.68), ('mie', 78, 0.8))):
            k = clamp((t - L('L05', f_ - 0.08)) / 0.3)
            if k > 0:
                lay = canvas(); arrow(lay, 50, 16.8, lerp(50, x, 0.92), 22.5, k, F['ink2'], 6); comp(im, lay)
            def f(l, w_=w_, x=x, i=i): chip(l, w_, x, 27, CHIPC[i], 50)
            G(L('L05', f_), f, (x, 27))
        a, sc = appear(t, L('L05', 0.84))
        lay = canvas(); txt(lay, 'kemungkinan lanjutan', (50, 34), 32, F['ink2'], 'SemiBold'); comp(im, lay, a, sc, (50, 34))

    elif sid == 'SH06':   # probability bars (illustration)
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Tiap pilihan punya peluang', (50, 11), 44, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 11))
        rows = [('nasi', 60, F['blue']), ('bakso', 25, F['coral']), ('mie', 15, F['yellow'])]
        k = ease_out_cubic(clamp((t - L('L06', 0.12)) / 0.7))
        hl = clamp((t - L('L06', 0.4)) / 0.25)
        lay = canvas()
        card(lay, (6, 15, 94, 37.5), r=34)
        for i, (w_, p, col) in enumerate(rows):
            y = 19.5 + i * 6.5
            if i == 0 and hl > 0: rr(lay, (8, y - 2.6, 92, y + 2.6), 24, F['yellow'], a=90 * hl)
            txt(lay, w_, (11, y), 38, F['ink'], 'SemiBold', 'lm')
            rr(lay, (30, y - 1.1, 78, y + 1.1), 20, F['bg2'])
            rr(lay, (30, y - 1.1, 30 + 48 * (p / 60) * k, y + 1.1), 20, col)
            txt(lay, f'{int(round(p * k))}%', (90, y), 38, F['ink'], 'Bold', 'rm')
        comp(im, lay, a, sc, (50, 26))
        a2, sc2 = appear(t, L('L06', 0.2))
        lay = canvas(); txt(lay, 'angka ilustrasi', (50, 40), 26, F['ink2'], 'Medium'); comp(im, lay, a2, sc2, (50, 40))
        a3, sc3 = appear(t, L('L06', 0.75))
        lay = canvas(); badge(lay, 'yang kecil tetap ada kesempatan', 50, 44, F['coral'], F['white'], 30); comp(im, lay, a3, sc3, (50, 44))

    elif sid == 'SH07':   # roll the dice -> picks bakso
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Kadang "kocok dadu" dulu', (50, 11), 44, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 11))
        t_roll, t_stop = L('L07', 0.55), L('L07', 0.82)
        if t < t_roll: n, bob = 1, 0.0
        elif t < t_stop: n, bob = 1 + int((t - t_roll) * 14) % 6, 1.2 * abs(math.sin((t - t_roll) * 18))
        else: n, bob = 4, 0.0
        lay = canvas(); dice(lay, 28, 26 - bob, 180, n); comp(im, lay, a, sc, (28, 26))
        picked = t >= t_stop
        for i, (w_, y) in enumerate((('nasi', 18), ('bakso', 26), ('mie', 34))):
            def f(l, w_=w_, y=y, i=i):
                on = picked and i == 1
                chip(l, w_, 68, y, F['coral'] if on else F['gray'], 46 if on else 40, tcol=F['white'] if on else F['ink2'])
                if on: check(l, 86, y, 0.8)
            G(L('L07', 0.1 + 0.08 * i), f, (68, y))
        a2, sc2 = appear(t, L('L07', 0.25))
        lay = canvas(); badge(lay, 'nggak selalu yang terbesar', 50, 41.5, F['ink'], F['white'], 32); comp(im, lay, a2, sc2, (50, 41.5))

    elif sid == 'SH08':   # temperature slider
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); card(lay, (6, 9, 94, 36), r=40)
        txt(lay, 'TEMPERATURE', (50, 14), 64, F['ink'], 'Bold')
        txt(lay, 'setelan tingkat acak', (50, 19), 32, F['ink2'], 'SemiBold')
        comp(im, lay, a, sc, (50, 20))
        a2, sc2 = appear(t, L('L08', 0.6))
        k = 0.5 + 0.42 * math.sin((t - L('L08', 0.6)) * 2.4) if t >= L('L08', 0.6) else 0.5
        lay = canvas(); slider(lay, 14, 86, 26.5, k, size=30); comp(im, lay, a2, sc2, (50, 27))
        a3, sc3 = appear(t, L('L08', 0.25))
        lay = canvas(); badge(lay, 'seberapa berani "ngocok"', 50, 41, F['coral'], F['white'], 32); comp(im, lay, a3, sc3, (50, 41))

    elif sid in ('SH09', 'SH10'):   # low vs high temperature
        hi = sid == 'SH10'; lid = 'L10' if hi else 'L09'
        k0 = 0.5; k1 = 0.9 if hi else 0.1
        kk = lerp(k0, k1, ease_out_back(clamp((t - s['start'] - 0.1) / 0.5)))
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); slider(lay, 20, 80, 11.5, kk, labels=False)
        badge(lay, 'TINGGI' if hi else 'RENDAH', 12, 11.5, F['coral'] if hi else F['blue'], F['white'], 26)
        comp(im, lay, a, sc, (50, 11.5))
        answers = ['Kopi', 'Tahu Bulat', 'Bulan'] if hi else ['Mochi', 'Mochi', 'Mochi']
        for i, (ans, x) in enumerate(zip(answers, (20, 50, 80))):
            def f(l, ans=ans, x=x):
                card(l, (x - 13.5, 16.5, x + 13.5, 25.5), r=30)
                txt(l, ans, (x, 21), 38 if len(ans) < 8 else 34, F['ink'], 'Bold')
            G(L(lid, 0.1 + 0.08 * i), f, (x, 21))
        tags = [('lebih kreatif', 30, F['yellow'], 0.35), ('lebih variatif', 70, F['lilac'], 0.5)] if hi else \
               [('konsisten', 32, F['mint'], 0.5), ('aman', 68, F['mint'], 0.75)]
        for tg, x, col, f_ in tags:
            a, sc = appear(t, L(lid, f_))
            lay = canvas(); badge(lay, tg, x, 30.2, col, F['ink'] if col == F['yellow'] else F['white'], 32); comp(im, lay, a, sc, (x, 30.2))
        if hi:
            def wild(l):
                bubble(l, (8, 33.6, 80, 38.6), 'Btw, kucing itu alien dari Mars...', 'a', size=30)
                cross(l, 87, 36.1, 0.9)
            G(L(lid, 0.78), wild, (45, 37))
            a, sc = appear(t, L(lid, 0.85))
            lay = canvas(); badge(lay, 'bisa ngelantur', 50, 42.2, F['coral'], F['white'], 28); comp(im, lay, a, sc, (50, 42.2))
        else:
            a, sc = appear(t, L(lid, 0.85))
            lay = canvas(); check(lay, 50, 38, 1.1); comp(im, lay, a, sc, (50, 38))
        lay = canvas(); txt(lay, 'contoh jawaban (ilustrasi)', (50, 45.5) if hi else (50, 45.3), 24, F['ink2'], 'Medium')
        a, sc = appear(t, L(lid, 0.3)); comp(im, lay, a, sc, (50, 45))

    elif sid == 'SH11':   # even lowest temp: not always identical
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); slider(lay, 30, 88, 11, 0.0, labels=False)
        badge(lay, 'paling rendah', 15, 11, F['blue'], F['white'], 26); comp(im, lay, a, sc, (50, 11))
        def b1(l):
            badge(l, '#1', 11, 18.6, F['ink'], F['white'], 24)
            bubble(l, (16, 16, 92, 21.2), 'Coba "Mochi", singkat dan lucu.', 'a', size=32)
        G(L('L11', 0.35), b1, (50, 18.6))
        def b2(l):
            badge(l, '#2', 11, 25.6, F['ink'], F['white'], 24)
            bubble(l, (16, 23, 92, 28.2), '"Mochi" aja! Lucu dan singkat.', 'a', size=32)
        G(L('L11', 0.55), b2, (50, 25.6))
        a, sc = appear(t, L('L11', 0.78))
        lay = canvas(); badge(lay, 'nggak selalu sama persis', 50, 32.8, F['coral'], F['white'], 32); comp(im, lay, a, sc, (50, 32.8))
        if t >= L('L12', 0.0):
            def ok(l):
                card(l, (18, 36.5, 82, 43.5), r=30, outline=F['mint'])
                check(l, 26, 40, 0.8)
                txt(l, 'wajar, bukan rusak', (31, 40), 38, F['ink'], 'Bold', 'lm')
            G(L('L12', 0.4), ok, (50, 40))
        lay = canvas(); txt(lay, 'contoh jawaban (ilustrasi)', (50, 45.6), 24, F['ink2'], 'Medium')
        comp(im, lay, *appear(t, L('L11', 0.6)), (50, 45.6))

    elif sid == 'SH12':   # three ways
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, '3 CARA BIAR\nKONSISTEN', (50, 19), 82, F['ink'], 'Bold', spacing=4); comp(im, lay, a, sc, (50, 19))
        for i in range(3):
            a, sc = appear(t, L('L13', 0.2 + 0.25 * i))
            lay = canvas(); circ(lay, 32 + 18 * i, 35, 52, CHIPC[i]); txt(lay, str(i + 1), (32 + 18 * i, 35.2), 60, F['white'])
            comp(im, lay, a, sc, (32 + 18 * i, 35))

    elif sid in ('SH13', 'SH14', 'SH15'):
        n = int(sid[-1]) - 2; lid = ['L14', 'L15', 'L16'][n - 1]
        title = ['Instruksi jelas & detail', 'Kasih contoh format', 'Atur temperature (API)'][n - 1]
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        circ(lay, 13, 11.5, 46, CHIPC[n - 1]); txt(lay, str(n), (13, 11.7), 56, F['white'])
        txt(lay, title, (20.5, 11.5), 44, F['ink'], 'Bold', 'lm')
        comp(im, lay, a, sc, (40, 11.5))
        if n == 1:
            def bad(l):
                bubble(l, (8, 17, 80, 22.5), 'Buatin caption.', 'u', size=32, fill=F['gray'], tcol=F['ink'])
                cross(l, 87, 19.75, 0.9)
            G(L(lid, 0.2), bad, (45, 19.75))
            def good(l):
                bubble(l, (8, 26, 80, 34), 'Caption kopi susu, gaya santai,\nmaks 12 kata.', 'u', size=32)
                check(l, 87, 30, 0.9)
            G(L(lid, 0.55), good, (45, 30))
            a2, sc2 = appear(t, L(lid, 0.75))
            lay = canvas(); badge(lay, 'makin jelas, makin konsisten', 50, 39.5, F['mint'], F['white'], 30); comp(im, lay, a2, sc2, (50, 39.5))
        elif n == 2:
            def f(l): bubble(l, (8, 16.5, 80, 22), 'Jawab pakai format ini:', 'u', size=32)
            G(L(lid, 0.2), f, (45, 19))
            def g(l):
                card(l, (14, 24.5, 86, 38.5), r=30)
                txt(l, 'Nama: ...', (19, 28.3), 36, F['ink'], 'SemiBold', 'lm')
                txt(l, 'Alasan: ...', (19, 32.3), 36, F['ink'], 'SemiBold', 'lm')
                txt(l, 'Maks 1 kalimat', (19, 36.0), 28, F['ink2'], 'Medium', 'lm')
                check(l, 80, 28.5, 0.8)
            G(L(lid, 0.5), g, (50, 31))
            a2, sc2 = appear(t, L(lid, 0.8))
            lay = canvas(); badge(lay, 'AI tinggal ikut polanya', 50, 42.3, F['blue'], F['white'], 30); comp(im, lay, a2, sc2, (50, 42.3))
        else:
            t1, t2 = L(lid, 0.3), L(lid, 0.72)
            kk = 0.5
            if t >= t1: kk = lerp(0.5, 0.08, ease_out_back(clamp((t - t1) / 0.5)))
            if t >= t2: kk = lerp(0.08, 0.92, ease_out_back(clamp((t - t2) / 0.6)))
            a1, sc1 = appear(t, L(lid, 0.05))
            lay = canvas(); card(lay, (6, 16.5, 94, 33.5), r=34); slider(lay, 14, 86, 22.5, kk, size=28); comp(im, lay, a1, sc1, (50, 25))
            a2, sc2 = appear(t, t1 + 0.1)
            lay = canvas(); badge(lay, 'turunkan = konsisten', 29, 29.8, F['blue'], F['white'], 28); comp(im, lay, a2, sc2, (30, 29.8))
            a3, sc3 = appear(t, t2 + 0.1)
            lay = canvas(); badge(lay, 'naikkan = ide liar', 73, 29.8, F['coral'], F['white'], 28); comp(im, lay, a3, sc3, (72, 29.8))
            a4, sc4 = appear(t, L(lid, 0.12))
            lay = canvas(); txt(lay, 'API = akses AI lewat kode / aplikasi', (50, 37.5), 32, F['ink2'], 'SemiBold')
            txt(lay, 'tiap model & penyedia bisa beda setelannya', (50, 41.2), 28, F['ink2'], 'Medium')
            comp(im, lay, a4, sc4, (50, 39))

    elif sid == 'SH16':   # Sakelar AI: many models, one door
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); wordmark(lay, 50, 10.5, 200, tsize=42); comp(im, lay, a, sc, (50, 12))
        ys = (22.5, 29.5, 36.5)
        for i, y in enumerate(ys):
            def f(l, i=i, y=y): chip(l, f'Model {"ABC"[i]}', 22, y, CHIPC[i], 36)
            G(L('L17', 0.35 + 0.1 * i), f, (22, y))
        k = clamp((t - L('L17', 0.65)) / 0.5)
        if k > 0:
            lay = canvas()
            for y in ys: arrow(lay, 36, y, 62, lerp(y, 29.5, 0.6), k, F['ink2'], 6)
            comp(im, lay)
        def door(l):
            rr(l, (64, 20, 84, 40), 22, F['ink']); rr(l, (66.5, 22.5, 81.5, 40), 14, F['blue'])
            circ(l, 79, 31, 10, F['yellow'])
        G(L('L17', 0.7), door, (74, 30))
        a2, sc2 = appear(t, L('L17', 0.8))
        lay = canvas(); badge(lay, 'satu pintu', 74, 43.5, F['blue'], F['white'], 30); comp(im, lay, a2, sc2, (74, 43.5))

    elif sid == 'SH17':   # each model has its own style (placeholder)
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Tiap model punya gaya', (50, 10.8), 46, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 10.8))
        rows = [('Model A', 'kalem', F['blue'], 0.5), ('Model B', 'kreatif', F['coral'], 0.75), ('Model C', 'ringkas', F['mint'], 0.88)]
        for i, (m_, st, col, f_) in enumerate(rows):
            y = 17.5 + i * 7.6
            def f(l, m_=m_, st=st, col=col, y=y):
                card(l, (8, y - 3.1, 92, y + 3.1), r=30)
                circ(l, 14.5, y, 28, col)
                txt(l, m_, (19, y), 38, F['ink'], 'SemiBold', 'lm')
                chip(l, st, 76, y, col, 36)
            G(L('L18', (0.05, 0.3, 0.5)[i]), f, (50, y))
        a2, sc2 = appear(t, L('L18', 0.6))
        lay = canvas(); txt(lay, 'contoh — nama & gaya model menyesuaikan', (50, 41.5), 26, F['ink2'], 'Medium'); comp(im, lay, a2, sc2, (50, 41.5))

    elif sid == 'SH18':   # try, pick, token package
        pick = t >= L('L19', 0.75)
        for i, x in enumerate((22, 50, 78)):
            def f(l, i=i, x=x):
                on = pick and i == 1
                card(l, (x - 12, 9.5, x + 12, 21.5), r=30, outline=F['mint'] if on else None)
                circ(l, x, 13.6, 30, CHIPC[i]); txt(l, 'ABC'[i], (x, 13.7), 36, F['white'])
                txt(l, f'Model {"ABC"[i]}', (x, 18.3), 30, F['ink'], 'SemiBold')
            G(L('L19', 0.15 + 0.12 * i), f, (x, 15.5))
        if pick:
            a, sc = appear(t, L('L19', 0.75))
            lay = canvas(); check(lay, 59.5, 10.5, 0.8); badge(lay, 'paling cocok', 50, 24.3, F['mint'], F['white'], 26)
            comp(im, lay, a, sc, (50, 18))
        if t >= L('L20', 0.0):
            def box(l):
                rr(l, (32, 30, 68, 41), 22, F['blue']); rr(l, (29.5, 27.6, 70.5, 31.2), 18, '#3561B3')
                rr(l, (47.8, 27.6, 52.2, 31.2), 6, F['yellow'])
                circ(l, 47.3, 26.9, 16, F['yellow']); circ(l, 52.7, 26.9, 16, F['yellow'])
                txt(l, 'PAKET TOKEN', (50, 36.0), 40, F['white'])
            G(L('L20', 0.15), box, (50, 34))
            a, sc = appear(t, L('L20', 0.6))
            lay = canvas(); badge(lay, 'Model B · ??M token (contoh)', 50, 44.3, F['yellow'], F['ink'], 28); comp(im, lay, a, sc, (50, 44.3))

    elif sid == 'SH19':   # not fickle, just a bit random
        a, sc = appear(t, L('L21', 0.15))
        lay = canvas(); txt(lay, 'plin-plan', (50, 11.5), 50, F['ink2'], 'Bold')
        line(lay, 37, 11.8, 63, 11.8, F['red'], 8); comp(im, lay, a, sc, (50, 11.5))
        a2, sc2 = appear(t, L('L21', 0.45))
        lay = canvas(); ai_box(lay, 30, 25, 0.8); txt(lay, '+', (50, 25), 90, F['ink2'], 'Bold')
        roll = t - L('L21', 0.55)
        n = 1 + int(roll * 10) % 6 if 0 <= roll < 0.6 else 5
        dice(lay, 70, 25, 150, n); comp(im, lay, a2, sc2, (50, 25))
        a3, sc3 = appear(t, L('L21', 0.7))
        lay = canvas(); badge(lay, 'sedikit unsur acak', 50, 39.5, F['ink'], F['white'], 36); comp(im, lay, a3, sc3, (50, 39.5))

    elif sid == 'SH20':   # punchline
        for i, (x, y, s_, ph) in enumerate(((22, 30, 1.6, 0), (78, 24, 2.0, 1.1), (64, 40, 1.2, 2.2), (34, 18, 1.0, 3.1), (50, 26, 2.6, 0.5))):
            t0 = L('L22', 0.4 + 0.08 * i)
            if t < t0: continue
            p = t - t0; a = min(1, p * 3)
            lay = canvas(); heart(lay, x + 0.6 * math.sin(p * 2 + ph), y - p * 1.5, s_ * (0.7 + 0.3 * ease_out_back(clamp(p / 0.4))))
            comp(im, lay, a)
        a, sc = appear(t, L('L22', 0.7))
        lay = canvas(); txt(lay, 'nggak pernah berubah', (50, 10.5), 50, F['coral'], 'Bold'); comp(im, lay, a, sc, (50, 10.5))

    elif sid == 'SH21':   # end card
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        card(lay, (10, 9, 90, 42), r=44)
        wordmark(lay, 50, 14.5, 240, tsize=50)
        txt(lay, 'Satu pintu, banyak model AI', (50, 25.5), 38, F['ink'], 'SemiBold')
        rr(lay, (18, 29.5, 82, 35), 40, F['blue']); txt(lay, 'app.sakelar.web.id', (50, 32.25), 42, F['white'], 'Bold')
        txt(lay, 'Ep 07 · Kok Jawaban AI Beda-beda?', (50, 38.7), 30, F['ink2'], 'Medium')
        comp(im, lay, a, sc, (50, 25))


# Per-shot spec: purpose, objects, anim (list of (t_rel, text)), screen text, sfx (list of (t_rel, name, len, dB, fn)), qa
def spec(sid):
    s = SH[sid]; d = round(s['end'] - s['start'], 3)
    if sid == 'SH01': return dict(
        goal='Hook: pertanyaan sama ke AI dua kali, jawaban beda.',
        obj=['Baris 1 (y≈9.5–21.5%): badge navy "Tanya #1" (14%,11.9%), bubble biru user x=30–92% "Kasih 1 ide nama kucing", bubble putih AI x=8–46% "Mochi" + label "AI".',
             'Baris 2 (y≈25–37%): sama, jawaban AI "Kopi".',
             'Lingkaran kuning r=34px berisi "≠" di (76%,22.2%).', 'Badge coral "kok beda?" (76%,37.5%).'],
        anim=[(0.15, 'Baris 1 pop-in 0.35 s easeOutBack.'), (r(sid, 'L01', 0.45), 'Baris 2 pop-in.'),
              (r(sid, 'L01', 0.75), '"≠" pop-in.'), (r(sid, 'L01', 0.85), 'Badge "kok beda?" pop-in (saat kata "beda").')],
        text=['"Tanya #1" / "Tanya #2" — Medium 24px putih.', '"Kasih 1 ide nama kucing" — Medium 32px putih.',
              '"Mochi" / "Kopi" — Medium 36px navy.', '"≠" Bold 52px.', '"kok beda?" — Medium 34px putih.'],
        sfx=[(0.15, 'pop', 0.15, -16, 'baris 1'), (r(sid, 'L01', 0.45), 'pop', 0.15, -16, 'baris 2'), (r(sid, 'L01', 0.85), 'boing', 0.25, -16, 'kok beda?')],
        qa=['Jawaban "Mochi"/"Kopi" ilustrasi.', 'Bubble tidak keluar panel (x ≤ 92%).'])
    if sid == 'SH02': return dict(
        goal='Bercanda: AI-nya lagi galau?',
        obj=['Chip AI navy skala 0.85 di (50%,30%).', 'Awan abu (5 lingkaran) di (50%,13.5%) + 9 garis hujan biru y 16.5→22.5%.',
             'Tiga "?" coral 80px di (20,22), (80,18), (78,34).', 'Badge coral "lagi galau?" (50%,41.5%).'],
        anim=[(0.1, 'Chip AI pop-in.'), (r(sid, 'L02', 0.15), 'Awan + hujan pop-in; hujan: y = 16.5 + ((9t + 1.7i) mod 6).'),
              (r(sid, 'L02', 0.1), '"?" pop-in bergiliran tiap +15%, goyang y ±0.6% sin(3t).'), (r(sid, 'L02', 0.55), 'Badge pop-in.')],
        text=['"AI" Bold.', '"?" ×3.', '"lagi galau?" — Medium 36px putih.'],
        sfx=[(r(sid, 'L02', 0.15), 'whoosh', 0.4, -20, 'awan'), (r(sid, 'L02', 0.55), 'boing', 0.25, -16, 'galau')],
        qa=['Pose think tanpa lip sync — baris pendek.'])
    if sid == 'SH03': return dict(
        goal='Koreksi: bukan error, memang cara kerjanya.',
        obj=['Kartu kiri x=7–47%, y=11–35%: ikon ✕ merah (27%,18.5%), kata "error" abu dicoret garis merah (27%,27%).',
             'Kartu kanan x=53–93% (outline mint): ikon ✓ hijau (73%,18.5%), "cara\\nkerjanya" (73%,27.6%).', 'Badge mint "normal kok" (50%,41.5%).'],
        anim=[(r(sid, 'L03', 0.12), 'Kartu kiri pop-in (saat "bukan error").'), (r(sid, 'L03', 0.55), 'Kartu kanan pop-in.'), (r(sid, 'L03', 0.7), 'Badge pop-in.')],
        text=['"error" Bold 50px abu + coret.', '"cara\\nkerjanya" Bold 42px navy.', '"normal kok" Medium 36px putih.'],
        sfx=[(r(sid, 'L03', 0.12), 'buzz', 0.25, -18, '✕ error'), (r(sid, 'L03', 0.55), 'ding', 0.4, -16, '✓ cara kerja')],
        qa=['Coretan tepat di kata "error".'])
    if sid == 'SH04': return dict(
        goal='AI menulis dengan menebak kata berikutnya, satu per satu.',
        obj=['Judul "AI menebak kata berikutnya" (50%,11.5%).', 'Kartu x=8–92%, y=16–27%.',
             'Chip [Aku][mau][makan] biru + [???] coral di y=21.5%, font 44px; kursor berkedip di x≈85.5%.',
             'Panah bawah (50%,28.5→33%) + badge navy "satu kata per langkah" (50%,37.5%).'],
        anim=[(0.1, 'Judul + kartu pop-in.'), (r(sid, 'L04', 0.25), 'Chip muncul satu per satu (stagger merata sampai 85% L04), tiap chip turun 1.2%→0 easeOutBack.'),
              (r(sid, 'L04', 0.8), 'Panah + badge pop-in.')],
        text=['"AI menebak kata berikutnya" Bold 44px.', 'Chip Medium 44px.', '"satu kata per langkah" Medium 34px putih.'],
        sfx=[(r(sid, 'L04', 0.25), 'clicks', 0.8, -18, 'chip muncul'), (r(sid, 'L04', 0.8), 'pop', 0.15, -16, 'badge')],
        qa=['Penyederhanaan: aslinya per token, di sini "kata" demi awam.'])
    if sid == 'SH05': return dict(
        goal='Contoh: "Aku mau makan..." bisa lanjut nasi, bakso, atau mie.',
        obj=['Kartu x=14–86%, y=8.8–15.6% berisi "\\"Aku mau makan...\\"".', 'Tiga panah dari (50%,16.8%) ke chip "nasi" (22%,27%) biru, "bakso" (50%,27%) coral, "mie" (78%,27%) kuning, font 50px.',
             'Teks "kemungkinan lanjutan" (50%,34%).'],
        anim=[(0.05, 'Kartu pop-in.'), (r(sid, 'L05', 0.52), 'Panah tumbuh 0.3 s, chip pop-in saat kata diucapkan: nasi 55%, bakso 68%, mie 80% L05.'),
              (r(sid, 'L05', 0.84), 'Teks bawah muncul.')],
        text=['"\\"Aku mau makan...\\"" Bold 46px.', '"nasi" / "bakso" / "mie" Medium 50px.', '"kemungkinan lanjutan" SemiBold 32px abu.'],
        sfx=[(r(sid, 'L05', 0.55), 'pop', 0.15, -16, 'nasi'), (r(sid, 'L05', 0.68), 'pop', 0.15, -16, 'bakso'), (r(sid, 'L05', 0.8), 'pop_hi', 0.15, -16, 'mie')],
        qa=['Chip sinkron dengan kata.'])
    if sid == 'SH06': return dict(
        goal='Tiap pilihan punya peluang; yang terbesar belum tentu satu-satunya.',
        obj=['Judul "Tiap pilihan punya peluang" (50%,11%).', 'Kartu x=6–94%, y=15–37.5%.',
             'Tiga baris y=19.5/26/32.5%: label (11%), track x=30–78%, bar biru 60% / coral 25% / kuning 15%, angka % kanan (90%).',
             'Sorotan kuning transparan di baris "nasi".', 'Teks "angka ilustrasi" (50%,40%).', 'Badge coral "yang kecil tetap ada kesempatan" (50%,44%).'],
        anim=[(0.05, 'Judul + kartu pop-in.'), (r(sid, 'L06', 0.12), 'Bar tumbuh 0.7 s easeOutCubic, angka ikut naik.'),
              (r(sid, 'L06', 0.4), 'Sorotan "nasi" fade-in 0.25 s (saat "paling besar").'), (r(sid, 'L06', 0.75), 'Badge pop-in.')],
        text=['"Tiap pilihan punya peluang" Bold 44px.', '"nasi"/"bakso"/"mie" SemiBold 38px.', '"60%"/"25%"/"15%" Bold 38px.', '"angka ilustrasi" Medium 26px abu.', '"yang kecil tetap ada kesempatan" Medium 30px.'],
        sfx=[(r(sid, 'L06', 0.12), 'swipe', 0.6, -18, 'bar tumbuh'), (r(sid, 'L06', 0.4), 'ding', 0.4, -18, 'nasi'), (r(sid, 'L06', 0.75), 'pop', 0.15, -16, 'badge')],
        qa=['Label "angka ilustrasi" wajib tampil.'])
    if sid == 'SH07': return dict(
        goal='AI kadang tidak ambil pilihan terbesar — ada unsur acak ("kocok dadu").',
        obj=['Judul "Kadang \\"kocok dadu\\" dulu" (50%,11%).', 'Dadu putih sisi 180px di (28%,26%), outline navy.',
             'Chip "nasi"/"bakso"/"mie" abu di x=68%, y=18/26/34%; setelah dadu berhenti, "bakso" jadi coral (lebih besar) + ✓ (86%,26%).',
             'Badge navy "nggak selalu yang terbesar" (50%,41.5%).'],
        anim=[(0.05, 'Judul + dadu pop-in.'), (r(sid, 'L07', 0.1), 'Chip pop-in bergiliran.'), (r(sid, 'L07', 0.25), 'Badge pop-in.'),
              (r(sid, 'L07', 0.55), 'Dadu dikocok: wajah ganti 14×/s, loncat |sin(18u)|·1.2%.'), (r(sid, 'L07', 0.82), 'Dadu berhenti di 4; "bakso" terpilih.')],
        text=['Judul Bold 44px.', 'Chip Medium 40/46px.', '"nggak selalu yang terbesar" Medium 32px putih.'],
        sfx=[(r(sid, 'L07', 0.55), 'clicks', 0.8, -14, 'dadu'), (r(sid, 'L07', 0.82), 'ding', 0.4, -16, 'bakso terpilih')],
        qa=['"bakso" (bukan nasi) yang terpilih — menegaskan bukan selalu yang terbesar.'])
    if sid == 'SH08': return dict(
        goal='Perkenalkan setelan temperature.',
        obj=['Kartu x=6–94%, y=9–36%: "TEMPERATURE" Bold 64px (50%,14%), "setelan tingkat acak" (50%,19%).',
             'Slider x=14–86%, y=26.5%: track gradasi biru→coral, knob putih r=30px outline navy; label "rendah" biru kiri, "tinggi" coral kanan.',
             'Badge coral "seberapa berani \\"ngocok\\"" (50%,41%).'],
        anim=[(0.1, 'Kartu pop-in.'), (r(sid, 'L08', 0.25), 'Badge pop-in.'), (r(sid, 'L08', 0.6), 'Slider muncul; knob bergoyang k = 0.5 + 0.42·sin(2.4u).')],
        text=['"TEMPERATURE"', '"setelan tingkat acak" SemiBold 32px abu.', '"rendah" / "tinggi" SemiBold 30px.', 'badge Medium 32px.'],
        sfx=[(0.1, 'pop', 0.15, -16, 'kartu'), (r(sid, 'L08', 0.6), 'whoosh', 0.5, -18, 'slider')],
        qa=['Pose desk: monitor tidak menutupi subtitle.', 'Tidak menyebut angka rentang temperature.'])
    if sid in ('SH09', 'SH10'):
        hi = sid == 'SH10'; lid = 'L10' if hi else 'L09'
        base = dict(
            goal='Temperature tinggi: kreatif & variatif, tapi bisa ngelantur.' if hi else 'Temperature rendah: jawaban lebih konsisten dan aman.',
            obj=['Slider x=20–80%, y=11.5% (tanpa label), knob bergerak ke ' + ('kanan (0.9); badge coral "TINGGI"' if hi else 'kiri (0.1); badge biru "RENDAH"') + ' (12%,11.5%).',
                 'Tiga kartu jawaban x pusat 20/50/80%, y=16.5–25.5%: ' + ('"Kopi", "Tahu Bulat", "Bulan"' if hi else '"Mochi" ×3') + '.',
                 'Badge "lebih kreatif" kuning (30%,30.2%) + "lebih variatif" lilac (70%,30.2%).' if hi else 'Badge mint "konsisten" (32%,30.2%) + "aman" (68%,30.2%); ✓ hijau (50%,38%).']
                + (['Bubble AI x=8–80%, y=33.6–38.6% "Btw, kucing itu alien dari Mars..." + ✕ (87%,36.1%); badge coral "bisa ngelantur" (50%,42.2%).'] if hi else
                   [])
                + ['Teks "contoh jawaban (ilustrasi)" Medium 24px abu (50%,' + ('45.5' if hi else '45.3') + '%).'],
            anim=[(0.1, 'Knob meluncur 0.5 s easeOutBack.'), (r(sid, lid, 0.1), 'Kartu jawaban pop-in bergiliran (+8%).')]
                 + ([(r(sid, lid, 0.35), 'Badge kreatif.'), (r(sid, lid, 0.5), 'Badge variatif.'), (r(sid, lid, 0.78), 'Bubble ngelantur + ✕.'), (r(sid, lid, 0.85), 'Badge "bisa ngelantur".')] if hi else
                    [(r(sid, lid, 0.5), 'Badge konsisten.'), (r(sid, lid, 0.75), 'Badge aman.'), (r(sid, lid, 0.85), '✓ pop-in.')]),
            text=(['"TINGGI"', '"Kopi" / "Tahu Bulat" / "Bulan" Bold 38/34px.', '"lebih kreatif" / "lebih variatif" Medium 32px.', '"Btw, kucing itu alien dari Mars..." Medium 30px.', '"bisa ngelantur" Medium 28px.'] if hi else
                  ['"RENDAH"', '"Mochi" Bold 38px ×3.', '"konsisten" / "aman" Medium 32px putih.', '"contoh jawaban (ilustrasi)" Medium 24px abu.']),
            sfx=([(0.1, 'swipe', 0.3, -18, 'knob'), (r(sid, lid, 0.1), 'pop', 0.4, -16, 'kartu'), (r(sid, lid, 0.35), 'sparkle', 0.6, -20, 'kreatif'), (r(sid, lid, 0.78), 'buzz', 0.25, -18, 'ngelantur')] if hi else
                 [(0.1, 'swipe', 0.3, -18, 'knob'), (r(sid, lid, 0.1), 'pop', 0.4, -16, 'kartu'), (r(sid, lid, 0.85), 'ding', 0.4, -16, '✓')]),
            qa=['Contoh jawaban ilustrasi.', 'Elemen bawah tidak lewat y 47%.'])
        return base
    if sid == 'SH11': return dict(
        goal='Fakta unik: temperature paling rendah pun jawaban nggak selalu sama persis — dan itu wajar.',
        obj=['Slider x=30–88%, y=11%, knob di paling kiri; badge biru "paling rendah" (15%,11%).',
             'Bubble AI #1 x=16–92%, y=16–21.2% "Coba \\"Mochi\\", singkat dan lucu."; bubble #2 y=23–28.2% "\\"Mochi\\" aja! Lucu dan singkat."; badge "#1"/"#2" di x=11%.',
             'Badge coral "nggak selalu sama persis" (50%,32.8%).', 'Kartu outline mint x=18–82%, y=36.5–43.5%: ✓ + "wajar, bukan rusak".', 'Teks "contoh jawaban (ilustrasi)" (50%,45.6%).'],
        anim=[(0.05, 'Slider pop-in.'), (r(sid, 'L11', 0.35), 'Bubble #1 pop-in.'), (r(sid, 'L11', 0.55), 'Bubble #2 pop-in.'),
              (r(sid, 'L11', 0.78), 'Badge coral pop-in.'), (r(sid, 'L12', 0.4), 'Kartu "wajar, bukan rusak" pop-in.')],
        text=['"paling rendah" Medium 26px.', 'Isi bubble Medium 32px (verbatim di atas).', '"nggak selalu sama persis" Medium 32px.', '"wajar, bukan rusak" Bold 38px.', 'Catatan Medium 24px abu.'],
        sfx=[(0.05, 'ding', 0.4, -16, '"Dan nih"'), (r(sid, 'L11', 0.35), 'pop', 0.15, -16, '#1'), (r(sid, 'L11', 0.55), 'pop', 0.15, -16, '#2'), (r(sid, 'L12', 0.4), 'chime', 0.6, -16, 'wajar')],
        qa=['Kalimat memakai "nggak selalu" — bukan klaim mutlak.'])
    if sid == 'SH12': return dict(
        goal='Transisi ke tips: 3 cara biar konsisten.',
        obj=['Judul 2 baris "3 CARA BIAR / KONSISTEN" Bold 82px navy (50%,19%).', 'Tiga lingkaran r=52px di (32,35), (50,35), (68,35): biru, coral, kuning, angka putih 60px.'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L13', 0.2), 'Lingkaran 1 pop-in, 2 & 3 tiap +25% L13.')],
        text=['"3 CARA BIAR\\nKONSISTEN"', '"1", "2", "3"'],
        sfx=[(r(sid, 'L13', 0.2), 'pop_hi', 0.6, -14, 'angka')], qa=['Judul tidak terpotong.'])
    if sid in ('SH13', 'SH14', 'SH15'):
        n = int(sid[-1]) - 2; lid = ['L14', 'L15', 'L16'][n - 1]
        head = f'Header: lingkaran nomor "{n}" r=46px di (13%,11.5%) + judul Bold 44px di x=20.5% left.'
        base = dict(goal=['Tips 1: instruksi jelas & detail.', 'Tips 2: kasih contoh format.', 'Tips 3: atur temperature kalau pakai API.'][n - 1])
        if n == 1: base.update(
            obj=[head, 'Bubble abu "Buatin caption." x=8–80%, y=17–22.5% + ✕ (87%,19.75%).',
                 'Bubble biru "Caption kopi susu, gaya santai,\\nmaks 12 kata." x=8–80%, y=26–34% + ✓ (87%,30%).', 'Badge mint "makin jelas, makin konsisten" (50%,39.5%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.2), 'Bubble buruk + ✕.'), (r(sid, lid, 0.55), 'Bubble bagus + ✓.'), (r(sid, lid, 0.75), 'Badge.')],
            text=['"Instruksi jelas & detail"', 'Isi bubble Medium 32px (verbatim).', 'Badge Medium 30px.'],
            sfx=[(r(sid, lid, 0.2), 'buzz', 0.25, -18, '✕'), (r(sid, lid, 0.55), 'ding', 0.4, -16, '✓')])
        if n == 2: base.update(
            obj=[head, 'Bubble biru "Jawab pakai format ini:" x=8–80%, y=16.5–22%.',
                 'Kartu x=14–86%, y=24.5–38.5%: "Nama: ..." (y 28.3%), "Alasan: ..." (y 32.3%), "Maks 1 kalimat" (y 36%), ✓ (80%,28.5%).', 'Badge biru "AI tinggal ikut polanya" (50%,42.3%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.2), 'Bubble pop-in.'), (r(sid, lid, 0.5), 'Kartu format pop-in.'), (r(sid, lid, 0.8), 'Badge.')],
            text=['"Kasih contoh format"', '"Jawab pakai format ini:" Medium 32px.', '"Nama: ..." / "Alasan: ..." SemiBold 36px; "Maks 1 kalimat" Medium 28px.', 'Badge Medium 30px.'],
            sfx=[(r(sid, lid, 0.2), 'whoosh', 0.3, -18, 'bubble'), (r(sid, lid, 0.5), 'stack', 0.6, -18, 'kartu format'), (r(sid, lid, 0.8), 'ding', 0.4, -16, 'badge')])
        if n == 3: base.update(
            obj=[head, 'Kartu x=6–94%, y=16.5–33.5% dengan slider x=14–86%, y=22.5% (label rendah/tinggi).',
                 'Badge biru "turunkan = konsisten" (29%,29.8%); badge coral "naikkan = ide liar" (73%,29.8%).',
                 'Teks "API = akses AI lewat kode / aplikasi" (50%,37.5%) + "tiap model & penyedia bisa beda setelannya" (50%,41%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.05), 'Kartu slider pop-in.'), (r(sid, lid, 0.12), 'Teks API muncul.'),
                  (r(sid, lid, 0.3), 'Knob 0.5→0.08 easeOutBack 0.5 s (saat "turunkan"); badge biru +0.1 s.'),
                  (r(sid, lid, 0.72), 'Knob 0.08→0.92 easeOutBack 0.6 s (saat "naikkan"); badge coral +0.1 s.')],
            text=['"Atur temperature (API)"', 'Badge Medium 28px.', 'Teks SemiBold 32px / Medium 28px abu.'],
            sfx=[(r(sid, lid, 0.3), 'swipe', 0.3, -18, 'turun'), (r(sid, lid, 0.72), 'swipe', 0.3, -18, 'naik'), (r(sid, lid, 0.78), 'sparkle', 0.6, -20, 'ide liar')])
        base['qa'] = ['Nomor tips sama dengan urutan dialog.', 'Contoh prompt ditulis persis.'] + (['Tidak mengklaim semua model membuka setelan temperature.'] if n == 3 else [])
        return base
    if sid == 'SH16': return dict(
        goal='Soft sell: di Sakelar AI banyak model lewat satu pintu.',
        obj=['Logo Sakelar (gelap) 200px + "Sakelar AI" Bold 42px di (50%,10.5%).',
             'Chip "Model A" biru / "Model B" coral / "Model C" kuning di x=22%, y=22.5/29.5/36.5%.',
             'Tiga panah x 36→62% menyatu ke pintu.', 'Pintu: kusen navy x=64–84%, y=20–40%; daun biru; gagang kuning (79%,31%).', 'Badge biru "satu pintu" (74%,43.5%).'],
        anim=[(0.05, 'Logo pop-in.'), (r(sid, 'L17', 0.35), 'Chip model pop-in tiap +10%.'), (r(sid, 'L17', 0.65), 'Panah tumbuh 0.5 s.'),
              (r(sid, 'L17', 0.7), 'Pintu pop-in.'), (r(sid, 'L17', 0.8), 'Badge "satu pintu" pop-in.')],
        text=['"Sakelar AI"', '"Model A/B/C" Medium 36px (placeholder, bukan nama asli).', '"satu pintu" Medium 30px putih.'],
        sfx=[(0.05, 'jingle', 0.6, -14, 'logo'), (r(sid, 'L17', 0.35), 'pop', 0.4, -18, 'chip'), (r(sid, 'L17', 0.7), 'chime', 0.6, -14, 'satu pintu')],
        qa=['Logo file asli Sakelar, tidak diubah bentuk.', 'Tidak menyebut nama model asli.'])
    if sid == 'SH17': return dict(
        goal='Tiap model punya gaya jawaban sendiri.',
        obj=['Judul "Tiap model punya gaya" (50%,10.8%).', 'Tiga kartu x=8–92%, tinggi 6.2%, pusat y=17.5/25.1/32.7%: titik warna, nama model (19% left), chip gaya (76%): kalem biru, kreatif coral, ringkas mint.',
             'Catatan "contoh — nama & gaya model menyesuaikan" (50%,41.5%).'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L18', 0.05), 'Kartu A pop-in.'), (r(sid, 'L18', 0.3), 'Kartu B pop-in.'), (r(sid, 'L18', 0.5), 'Kartu C pop-in.'),
              (r(sid, 'L18', 0.6), 'Catatan muncul.')],
        text=['"Tiap model punya gaya" Bold 46px.', '"Model A/B/C" SemiBold 38px.', '"kalem"/"kreatif"/"ringkas" chip 36px — PLACEHOLDER.', 'Catatan Medium 26px abu.'],
        sfx=[(r(sid, 'L18', 0.05), 'swipe', 0.3, -18, 'kartu A'), (r(sid, 'L18', 0.3), 'pop', 0.15, -16, 'kartu B'), (r(sid, 'L18', 0.5), 'pop_hi', 0.15, -16, 'kartu C')],
        qa=['Gaya model ditandai contoh — belum ada daftar resmi.'])
    if sid == 'SH18': return dict(
        goal='Coba beberapa model, pilih yang cocok; token dijual dalam paket per model.',
        obj=['Tiga kartu model lebar 24% di x=22/50/78%, y=9.5–21.5%: lingkaran huruf + "Model A/B/C".',
             'Saat dipilih: kartu B outline mint, ✓ (59.5%,10.5%), badge mint "paling cocok" (50%,24.3%).',
             'Kotak "PAKET TOKEN" biru x=32–68%, y=30–41%, tutup x=29.5–70.5%, pita + pita simpul kuning hanya di tutup (teks tidak tertutup).', 'Badge kuning "Model B · ??M token (contoh)" (50%,44.3%).'],
        anim=[(r(sid, 'L19', 0.15), 'Kartu model pop-in tiap +12%.'), (r(sid, 'L19', 0.75), 'Kartu B terpilih + ✓ + badge.'),
              (r(sid, 'L20', 0.15), 'Kotak paket pop-in.'), (r(sid, 'L20', 0.6), 'Badge isi paket pop-in.')],
        text=['"Model A/B/C" SemiBold 30px.', '"paling cocok" Medium 26px.', '"PAKET TOKEN" Bold 38px putih.', '"Model B · ??M token (contoh)" Medium 28px — PLACEHOLDER.'],
        sfx=[(r(sid, 'L19', 0.15), 'pop', 0.4, -18, 'kartu'), (r(sid, 'L19', 0.75), 'ding', 0.4, -16, 'terpilih'), (r(sid, 'L20', 0.15), 'coins', 0.8, -18, 'paket')],
        qa=['Isi paket placeholder "??M (contoh)".'])
    if sid == 'SH19': return dict(
        goal='Rangkuman: AI bukan plin-plan, cuma ada sedikit unsur acak.',
        obj=['Kata "plin-plan" abu Bold 50px dicoret garis merah (50%,11.5%).', 'Chip AI skala 0.8 (30%,25%) + "+" (50%,25%) + dadu 150px (70%,25%).', 'Badge navy "sedikit unsur acak" (50%,39.5%).'],
        anim=[(r(sid, 'L21', 0.15), '"plin-plan" + coretan pop-in.'), (r(sid, 'L21', 0.45), 'AI + dadu pop-in.'),
              (r(sid, 'L21', 0.55), 'Dadu dikocok 0.6 s (10 wajah/s) lalu berhenti di 5.'), (r(sid, 'L21', 0.7), 'Badge pop-in.')],
        text=['"plin-plan"', '"+"', '"sedikit unsur acak" Medium 36px putih.'],
        sfx=[(r(sid, 'L21', 0.15), 'scratch', 0.3, -18, 'coret'), (r(sid, 'L21', 0.55), 'clicks', 0.6, -16, 'dadu')],
        qa=['Coretan tepat di kata.'])
    if sid == 'SH20': return dict(
        goal='Punchline manis: jawaban Reina buat penonton nggak pernah berubah.',
        obj=['5 hati coral di (22,30), (78,24), (64,40), (34,18), (50,26), skala 1.0–2.6.', 'Teks "nggak pernah berubah" Bold 50px coral (50%,10.5%).'],
        anim=[(r(sid, 'L22', 0.4), 'Hati muncul tiap +8% L22; naik 1.5%/s, goyang x ±0.6%, skala 0.7→1.0 easeOutBack.'), (r(sid, 'L22', 0.7), 'Teks pop-in.')],
        text=['"nggak pernah berubah" Bold 50px coral.'],
        sfx=[(r(sid, 'L22', 0.4), 'sparkle', 1.0, -18, 'hati'), (r(sid, 'L22', 0.7), 'pop_hi', 0.2, -16, 'teks')],
        qa=['Mulut memakai sprite smile.'])
    if sid == 'SH21': return dict(
        goal='End card: ajakan mencoba Sakelar AI.',
        obj=['Kartu putih x=10–90%, y=9–42%, radius 44px.', 'Logo 240px + "Sakelar AI" Bold 50px (pusat 50%,14.5%).',
             '"Satu pintu, banyak model AI" (50%,25.5%).', 'Tombol biru x=18–82%, y=29.5–35% "app.sakelar.web.id".', '"Ep 07 · Kok Jawaban AI Beda-beda?" (50%,38.7%).'],
        anim=[(0.05, 'Kartu pop-in 0.35 s.'), (round(d - 0.5, 3), 'Seluruh frame fade ke #F6F1E7 dalam 0.5 s.')],
        text=['"Sakelar AI"', '"Satu pintu, banyak model AI" Medium 38px.', '"app.sakelar.web.id" Bold 42px putih.', '"Ep 07 · Kok Jawaban AI Beda-beda?" Medium 30px abu.'],
        sfx=[(0.05, 'stinger', 1.2, -12, 'end card'), (0.1, 'jingle', 0.6, -16, 'logo')], qa=['URL tertulis persis "app.sakelar.web.id".', 'Video berakhir di frame latar polos.'])
