"""Reina Explains AI — Episode 12: "API Key Itu Apa, Kenapa Harus Dijaga?" (tema putih polos, posisi Reina berganti).
Satu file = satu episode: naskah, shot, pose, posisi, visual panel(t), spec storyboard + SFX, arahan VO.
Jalankan:  python run.py stage1 episodes/ep12.py   lalu   python run.py stage2 episodes/ep12.py <zip_suara>"""
import math
from PIL import Image, ImageDraw
from reina import *

EP = 12
TITLE = 'API Key Itu Apa, Kenapa Harus Dijaga?'
SCENES = {1: 'Hook', 2: 'Apa itu API key', 3: 'Kenapa bisa bocor', 4: 'Fakta unik', 5: 'Tips jaga key',
          6: 'Soft sell Sakelar AI', 7: 'Closing', 8: 'End card'}
META = dict(
    tujuan='Menjelaskan API key dengan analogi kunci rumah, kenapa bisa bocor, dan cara menjaganya; soft sell Sakelar AI sebagai satu pintu ke banyak model',
    konsep=('Hook: tagihan AI bengkak padahal nggak dipakai → penyebab: API key bocor → API key = kunci akses layanan AI lewat aplikasi/kode → '
            'siapa pun yang pegang bisa pakai atas nama kamu → bocor karena ditempel di kode publik atau kefoto → fakta: ada bot yang mencari key bocor → '
            '3 cara jaga key → soft sell: makin banyak layanan makin banyak akun dijaga; Sakelar AI satu pintu, paket token per model → punchline "kunci hatiku".'),
    fakta=['API key = kode rahasia untuk mengakses layanan (mis. layanan AI) lewat aplikasi/kode; pemegangnya bisa memakai layanan atas nama pemilik akun.',
           'Key sering bocor karena ditulis langsung di kode yang diunggah ke publik atau terlihat di screenshot.',
           'Ada program otomatis (bot) yang memindai kode publik untuk mencari key yang bocor — disebut tanpa angka waktu pasti ("dalam waktu singkat").',
           'Kalau key bocor: hapus/cabut key lama lalu buat key baru.',
           'Sakelar AI = satu pintu (gateway) ke banyak model; token dijual dalam paket per model (sekian juta token).', 'CTA URL: app.sakelar.web.id.'],
    asumsi=['Contoh key di SH04 ("sk-contoh-...") dikarang & ditandai "contoh, bukan key asli".',
            'Tagihan di SH01 memakai "Rp ???" dan label "ilustrasi" — tidak ada angka karangan.',
            'Tidak diklaim Sakelar AI memakai "satu API key" atau punya fitur keamanan khusus; L15–L16 hanya bilang banyak model lewat satu pintu.'],
    konfirmasi=['Isi paket di SH14 masih "Model A · ??M token (contoh)" — ganti kalau ada data resmi.',
                'Kalau Sakelar AI memang memberi satu API key untuk semua model, L16 bisa dipertegas di revisi berikutnya.'],
    softsell='SH12–SH14 + end card',
)
PRON = [('API', 'ei-pi-ai'), ('API key', 'ei-pi-ai ki'), ('AI', 'ei-ai'), ('screenshot', 'skrin-syot'), ('Sakelar', 'sa-ke-lar')]
VO_DIR = {'L01': 'heran, sedikit dramatis di "bengkak"', 'L02': 'pelan lalu tegas di "bocor"',
 'L03': 'menjelaskan, santai, tekan "kunci rumah"', 'L04': 'ringan', 'L05': 'serius, tekan "atas nama kamu"',
 'L06': 'pendek, sedikit ngeri', 'L07': 'santai, nada "nah"', 'L08': 'ritmis, dua contoh dipisah jelas',
 'L09': 'nada "fakta seru", semangat di "Dan nih"', 'L10': 'serius, tegas', 'L11': 'energik, membuka daftar',
 'L12': 'tegas tapi ramah', 'L13': 'ringan, tekan "jangan pernah"', 'L14': 'tegas, cepat di "langsung hapus"',
 'L15': 'ramah, nada "nah" naik', 'L16': 'meyakinkan, santai', 'L17': 'menjelaskan, ringan',
 'L18': 'menyimpulkan, mantap', 'L19': 'malu-malu manis, pelan, jeda di "Kecuali kunci hatiku...", senyum di akhir'}

# ---- naskah terkunci (1 item = 1 baris VO = L01, L02, ...) ----
LINES = [
 'Pernah dengar cerita tagihan AI orang tiba-tiba bengkak, padahal dia nggak pakai?',
 'Bisa jadi gara-gara satu hal kecil: API key-nya bocor.',
 'API key itu kayak kunci rumah buat akses layanan AI lewat aplikasi atau kode.',
 'Bentuknya deretan huruf dan angka acak yang panjang.',
 'Siapa pun yang pegang kunci ini bisa pakai layanannya atas nama kamu.',
 'Termasuk kuota dan saldo kamu.',
 'Biasanya bocornya karena hal sepele.',
 'Ditempel langsung di kode yang diunggah ke publik, atau kefoto pas lagi screenshot.',
 'Dan nih, ada bot yang kerjanya keliling internet nyari key yang bocor.',
 'Jadi key yang ketahuan publik bisa disalahgunakan dalam waktu singkat.',
 'Tiga cara jaga API key.',
 'Satu, jangan tempel di kode. Simpan di pengaturan rahasia.',
 'Dua, jangan pernah bagi di chat, grup, atau screenshot.',
 'Tiga, kalau curiga bocor, langsung hapus dan bikin key baru.',
 'Nah, makin banyak layanan AI yang kamu pakai, makin banyak juga akun yang harus dijaga.',
 'Di Sakelar AI, kamu bisa akses banyak model lewat satu pintu.',
 'Tokennya dijual dalam paket per model, isinya sekian juta token.',
 'Jadi, API key itu kunci. Jaga baik-baik, jangan dipinjemin.',
 'Kecuali kunci hatiku... itu udah aku titipin ke kamu.',
]

# (id, scene, judul, [nomor baris], jeda_awal_s, jeda_akhir_s)
SHOTS = [
 ('SH01', 1, 'Tagihan AI bengkak', [1], 0.5, 0.2),
 ('SH02', 1, 'API key bocor', [2], 0.15, 0.4),
 ('SH03', 2, 'Kunci rumah = API key', [3], 0.25, 0.2),
 ('SH04', 2, 'Deretan huruf & angka', [4], 0.15, 0.2),
 ('SH05', 2, 'Dipakai atas nama kamu', [5, 6], 0.15, 0.4),
 ('SH06', 3, 'Bocor karena hal sepele', [7, 8], 0.25, 0.4),
 ('SH07', 4, 'Bot pencari key bocor', [9, 10], 0.25, 0.4),
 ('SH08', 5, 'Tiga cara jaga API key', [11], 0.25, 0.15),
 ('SH09', 5, 'Tips 1: jangan di kode', [12], 0.1, 0.2),
 ('SH10', 5, 'Tips 2: jangan dibagi', [13], 0.1, 0.2),
 ('SH11', 5, 'Tips 3: hapus & bikin baru', [14], 0.1, 0.4),
 ('SH12', 6, 'Banyak layanan, banyak akun', [15], 0.25, 0.2),
 ('SH13', 6, 'Sakelar AI satu pintu', [16], 0.1, 0.2),
 ('SH14', 6, 'Paket token per model', [17], 0.1, 0.4),
 ('SH15', 7, 'Jaga baik-baik', [18], 0.25, 0.25),
 ('SH16', 7, 'Kunci hatiku', [19], 0.1, 0.6),
 ('SH17', 8, 'End card', [], 0.0, 2.5),
]

POSE = {'SH01': 'phone', 'SH02': 'point_up', 'SH03': 'point', 'SH04': 'arms34', 'SH05': 'hands_on_hips',
        'SH06': 'point_up', 'SH07': 'desk', 'SH08': 'hands_on_hips', 'SH09': 'point_up', 'SH10': 'thumbs_up',
        'SH11': 'bust', 'SH12': 'phone', 'SH13': 'wave', 'SH14': 'thumbs_up', 'SH15': 'hands_on_hips',
        'SH16': 'shy_lean', 'SH17': 'wave'}
# posisi Reina per shot (tema putih polos): kiri / kanan / closeup / tengah
POS = {'SH01': 'kiri', 'SH02': 'closeup', 'SH03': 'kanan', 'SH04': 'kiri', 'SH05': 'kanan', 'SH06': 'kiri',
       'SH07': 'tengah', 'SH08': 'tengah', 'SH09': 'kanan', 'SH10': 'kiri', 'SH11': 'closeup', 'SH12': 'kanan',
       'SH13': 'kiri', 'SH14': 'kanan', 'SH15': 'kiri', 'SH16': 'closeup', 'SH17': 'tengah'}
SMILE = {'SH16'}
EXPR = {'SH01': 'heran sambil lihat HP', 'SH02': 'serius, menekankan', 'SH03': 'menjelaskan, menunjuk penonton',
        'SH04': 'analitis', 'SH05': 'serius', 'SH06': 'menjelaskan', 'SH07': 'fokus ke monitor', 'SH08': 'percaya diri',
        'SH09': 'menjelaskan', 'SH10': 'ceria', 'SH11': 'tegas, tangan bersilang', 'SH12': 'menjelaskan sambil lihat HP',
        'SH13': 'ramah, menyapa', 'SH14': 'ceria, meyakinkan', 'SH15': 'santai, menutup',
        'SH16': 'malu-malu, senyum (mulut smile)', 'SH17': 'ceria, melambai'}


# ---------------- helper lokal ----------------
def key_icon(l, cx, cy, s=1.0, col=F['yellow'], a=255):
    """Kunci flat: kepala bulat berlubang + batang + 2 gigi. s=1 → lebar ±24% kanvas."""
    r_ = 46 * s
    hx = cx - 7.5 * s
    circ(l, hx, cy, r_, col, a)
    circ(l, hx, cy, r_ * 0.42, BGC, a)
    rr(l, (hx + 3.0 * s, cy - 0.75 * s, cx + 11.5 * s, cy + 0.75 * s), 8, col, a=a)
    rr(l, (cx + 6.5 * s, cy, cx + 8.3 * s, cy + 2.4 * s), 4, col, a=a)
    rr(l, (cx + 9.7 * s, cy, cx + 11.5 * s, cy + 1.8 * s), 4, col, a=a)
BGC = '#F7F5F0'

def bot_icon(l, cx, cy, s=1.0, col=F['ink2']):
    """Robot kecil: kepala kotak, 2 mata, antena."""
    hw, hh = 5.5 * s, 5.5 * s * W / H
    line(l, cx, cy - hh, cx, cy - hh - 1.6 * s, col, 6)
    circ(l, cx, cy - hh - 1.8 * s, 12 * s, F['coral'])
    rr(l, (cx - hw, cy - hh, cx + hw, cy + hh), 22, col)
    circ(l, cx - hw * 0.42, cy - 0.2, 13 * s, F['yellow']); circ(l, cx + hw * 0.42, cy - 0.2, 13 * s, F['yellow'])
    rr(l, (cx - hw * 0.4, cy + hh * 0.45, cx + hw * 0.4, cy + hh * 0.6), 4, F['white'])

def person(l, cx, cy, col, s=1.0):
    """Ikon orang flat (kepala + badan)."""
    circ(l, cx, cy - 1.4 * s, 26 * s, col)
    rr(l, (cx - 3.2 * s, cy + 0.2 * s, cx + 3.2 * s, cy + 3.0 * s), 30, col)

def code_card(l, box, lines, hl=None):
    """Kartu kode gelap; hl = indeks baris yang disorot merah."""
    x0, y0, x1, y1 = box
    rr(l, (x0, y0 + 0.4, x1, y1 + 0.4), 28, F['ink'], a=40); rr(l, box, 28, F['ink'])
    for i, c in enumerate((F['red'], F['yellow'], F['mint'])): circ(l, x0 + 3 + i * 2.6, y0 + 1.6, 9, c)
    for i, s_ in enumerate(lines):
        y = y0 + 4.4 + i * 3.0
        if hl == i: rr(l, (x0 + 1.5, y - 1.3, x1 - 1.5, y + 1.3), 10, F['red'])
        txt(l, s_, (x0 + 3, y), 30, F['white'] if hl == i else '#C9D3EA', 'SemiBold' if hl == i else 'Medium', 'lm')


def panel(t, sid, im):
    """Gambar visual (area y 7–47%) shot sid pada waktu t ke layer 2x im."""
    s = SH[sid]; u = t - s['start']; L = lambda lid, f=0.0: rel(lid, f)
    def G(t0, fn, anchor=(50, 25), d=0.35):
        a, sc = appear(t, t0, d)
        if a <= 0: return
        lay = canvas(); fn(lay); comp(im, lay, a, sc, anchor)

    if sid == 'SH01':   # tagihan bengkak
        def f(l):
            card(l, (10, 9, 90, 38), r=40)
            txt(l, 'Tagihan AI', (15, 13.5), 40, F['ink'], 'Bold', 'lm')
            badge(l, 'bulan ini', 82, 13.5, F['bg2'], F['ink2'], 24)
            for i in range(5):   # batang naik
                h = [2.5, 3.0, 2.8, 3.4, 15.0][i] * (ease_out_cubic(clamp((t - L('L01', 0.45)) / 0.6)) if i == 4 else 1)
                rr(l, (15 + i * 9, 33 - h, 21 + i * 9, 33), 10, F['coral'] if i == 4 else F['blue2'])
            txt(l, 'Rp ???', (84, 22), 46, F['red'], 'Bold', 'rm')
            txt(l, 'ilustrasi', (50, 35.8), 24, F['ink2'], 'Medium')
        G(s['start'] + 0.15, f, (50, 23))
        a, sc = appear(t, L('L01', 0.55))
        lay = canvas(); arrow(lay, 76, 31, 76, 25.5, 1, F['red'], 9); comp(im, lay, a, sc, (76, 28))
        a, sc = appear(t, L('L01', 0.8))
        lay = canvas(); badge(lay, 'padahal nggak dipakai?', 50, 43, F['coral'], F['white'], 34); comp(im, lay, a, sc, (50, 43))

    elif sid == 'SH02':   # key bocor
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); key_icon(lay, 50, 22, 1.4); comp(im, lay, a, sc, (50, 22))
        for i in range(3):   # tetesan bocor: fungsi murni dari t
            t0 = L('L02', 0.6) + i * 0.25
            if t < t0: continue
            p = ((t - t0) * 0.9) % 1.0
            lay = canvas(); ell(lay, 60 + i * 3, lerp(25, 34, p), 12, 18, F['blue'], a=255 * (1 - p)); comp(im, lay)
        a, sc = appear(t, L('L02', 0.7))
        lay = canvas(); badge(lay, 'BOCOR!', 50, 40, F['red'], F['white'], 44); comp(im, lay, a, sc, (50, 40))

    elif sid == 'SH03':   # kunci rumah = API key
        def house(l):
            poly(l, [(12, 20), (24, 12), (36, 20)], F['coral'])
            rr(l, (14, 20, 34, 31), 12, F['white']); rr(l, (21.5, 24, 26.5, 31), 8, F['blue'])
            txt(l, 'rumah', (24, 34), 30, F['ink2'], 'SemiBold')
        G(L('L03', 0.1), house, (24, 22))
        a, sc = appear(t, L('L03', 0.2))
        lay = canvas(); key_icon(lay, 50, 22, 0.8); comp(im, lay, a, sc, (50, 22))
        a, sc = appear(t, L('L03', 0.55))
        lay = canvas(); arrow(lay, 62, 22, 70, 22, 1, F['ink2'], 7); ai_box(lay, 81, 22, 0.6)
        txt(lay, 'layanan AI', (81, 31.5), 30, F['ink2'], 'SemiBold'); comp(im, lay, a, sc, (78, 22))
        a, sc = appear(t, L('L03', 0.7))
        lay = canvas(); badge(lay, 'API key = kunci akses', 50, 41, F['ink'], F['white'], 36); comp(im, lay, a, sc, (50, 41))

    elif sid == 'SH04':   # deretan acak
        def f(l):
            card(l, (8, 13, 92, 27), r=36)
            txt(l, 'API KEY', (13, 16.6), 26, F['ink2'], 'SemiBold', 'lm')
            full = 'sk-contoh-8fK2qL9xR7mT4vB1'
            n = int(len(full) * clamp((t - L('L04', 0.15)) / 0.6))
            txt(l, full[:max(3, n)], (13, 22), 48, F['ink'], 'Bold', 'lm')
        G(L('L04', 0.05), f, (50, 20))
        a, sc = appear(t, L('L04', 0.55))
        lay = canvas()
        chip(lay, 'huruf', 30, 33, F['blue'], 34); chip(lay, 'angka', 50, 33, F['coral'], 34); chip(lay, 'acak', 70, 33, F['mint'], 34)
        comp(im, lay, a, sc, (50, 33))
        a, sc = appear(t, L('L04', 0.4))
        lay = canvas(); txt(lay, 'contoh, bukan key asli', (50, 40), 26, F['ink2'], 'Medium'); comp(im, lay, a, sc, (50, 40))

    elif sid == 'SH05':   # dipakai atas nama kamu
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); person(lay, 18, 15, F['blue']); txt(lay, 'kamu', (18, 21), 30, F['ink'], 'SemiBold')
        comp(im, lay, a, sc, (18, 16))
        a2, sc2 = appear(t, L('L05', 0.3))
        lay = canvas(); person(lay, 18, 30, F['red']); txt(lay, 'orang lain', (18, 36), 30, F['red'], 'SemiBold')
        key_icon(lay, 33, 30, 0.35); comp(im, lay, a2, sc2, (22, 31))
        a3, sc3 = appear(t, L('L05', 0.15))
        lay = canvas(); arrow(lay, 26, 15, 52, 22, 1, F['ink2'], 6)
        if t >= L('L05', 0.3): arrow(lay, 40, 30, 52, 24, clamp((t - L('L05', 0.35)) / 0.4), F['red'], 6)
        ai_box(lay, 62, 23, 0.55); comp(im, lay, a3, sc3, (55, 23))
        a4, sc4 = appear(t, L('L05', 0.8))
        lay = canvas(); badge(lay, 'atas nama kamu', 62, 33, F['coral'], F['white'], 28); comp(im, lay, a4, sc4, (62, 33))
        if t >= L('L06', 0.0):   # kuota menyusut
            k = clamp((t - L('L06', 0.1)) / max(0.6, s['end'] - L('L06', 0.1) - 0.2))
            lay = canvas()
            txt(lay, 'kuota & saldo kamu', (12, 40.5), 30, F['ink'], 'SemiBold', 'lm')
            rr(lay, (12, 42.5, 88, 45.5), 20, F['bg2']); rr(lay, (12, 42.5, 12 + 76 * (1 - 0.92 * k), 45.5), 20, F['red'] if k > 0.5 else F['mint'])
            comp(im, lay, min(1, (t - L('L06', 0.0)) * 5))

    elif sid == 'SH06':   # bocor karena hal sepele
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Bocor karena hal sepele', (50, 10.5), 44, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 10.5))
        def code(l):
            code_card(l, (5, 15, 55, 33), ['import ai', 'key = "sk-contoh-8fK2..."', 'ai.tanya("halo")'], hl=1)
            badge(l, 'PUBLIK', 49, 17.4, F['coral'], F['white'], 22)
            cross(l, 30, 37.3, 0.8)
        G(L('L08', 0.05), code, (30, 25))
        def shot(l):
            rr(l, (61, 15, 95, 33), 26, F['white'], outline=F['ink2'], w=4)
            for i in range(3): rr(l, (64, 18.5 + i * 3.2, 92 - i * 6, 19.9 + i * 3.2), 6, F['bg2'])
            rr(l, (64, 28, 92, 30.6), 8, F['yellow'], a=150); txt(l, 'sk-contoh-8fK2...', (65, 29.3), 26, F['ink'], 'SemiBold', 'lm')
            for cx_, cy_ in ((61, 15), (95, 15), (61, 33), (95, 33)): circ(l, cx_, cy_, 8, F['ink'])
            txt(l, 'screenshot', (78, 35.7), 28, F['ink2'], 'SemiBold')
            cross(l, 78, 39.5, 0.8)
        G(L('L08', 0.62), shot, (78, 25))
        a, sc = appear(t, L('L07', 0.2))
        lay = canvas(); txt(lay, 'contoh (ilustrasi)', (50, 45), 24, F['ink2'], 'Medium'); comp(im, lay, a, sc, (50, 45))

    elif sid == 'SH07':   # bot mencari key bocor
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        card(lay, (8, 9, 92, 34), r=36)
        for i in range(6):
            y = 13 + i * 3.3
            rr(lay, (13, y - 0.6, 13 + [52, 40, 58, 34, 48, 44][i], y + 0.6), 6, F['bg2'])
        found = t >= L('L09', 0.75)
        if found: rr(lay, (12, 25.0, 64, 28.0), 10, F['red'], a=80); txt(lay, 'key = "sk-..."', (14, 26.5), 26, F['red'], 'Bold', 'lm')
        comp(im, lay, a, sc, (50, 21))
        k = (t - s['start']) * 0.7
        gy = 13 + (abs(((k % 2.0) - 1.0)) * 16.5) if not found else 26.5   # kaca pembesar menyapu baris
        gx = 40 + 22 * math.sin(k * 2.2) if not found else 38
        lay = canvas(); circ(lay, gx, gy, 40, None, outline=F['ink'], w=8); line(lay, gx + 2.6, gy + 1.5, gx + 5.5, gy + 3.2, F['ink'], 12)
        comp(im, lay, a)
        lay = canvas(); bot_icon(lay, 80, 20, 1.0); comp(im, lay, a, sc, (80, 20))
        a2, sc2 = appear(t, L('L09', 0.3))
        lay = canvas(); badge(lay, 'bot pencari key bocor', 50, 38.5, F['ink'], F['white'], 32); comp(im, lay, a2, sc2, (50, 38.5))
        a3, sc3 = appear(t, L('L10', 0.5))
        lay = canvas(); badge(lay, 'key bocor = bahaya', 50, 43.5, F['coral'], F['white'], 32); comp(im, lay, a3, sc3, (50, 43.5))

    elif sid == 'SH08':   # 3 cara
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, '3 CARA JAGA\nAPI KEY', (50, 18), 82, F['ink'], 'Bold', spacing=4); comp(im, lay, a, sc, (50, 18))
        for i in range(3):
            a, sc = appear(t, L('L11', 0.2 + 0.25 * i))
            lay = canvas(); circ(lay, 32 + 18 * i, 35, 52, CHIPC[i]); txt(lay, str(i + 1), (32 + 18 * i, 35.2), 60, F['white'])
            comp(im, lay, a, sc, (32 + 18 * i, 35))

    elif sid in ('SH09', 'SH10', 'SH11'):
        n = {'SH09': 1, 'SH10': 2, 'SH11': 3}[sid]; lid = ['L12', 'L13', 'L14'][n - 1]
        title = ['Jangan tempel di kode', 'Jangan dibagi-bagi', 'Bocor? Hapus, bikin baru'][n - 1]
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); circ(lay, 12, 11.5, 46, CHIPC[n - 1]); txt(lay, str(n), (12, 11.7), 56, F['white'])
        txt(lay, title, (19.5, 11.5), 44, F['ink'], 'Bold', 'lm'); comp(im, lay, a, sc, (40, 11.5))
        if n == 1:
            def bad(l):
                code_card(l, (6, 16.5, 80, 25.5), ['key = "sk-contoh-8fK2..."'], hl=0)
                cross(l, 88, 21, 0.9)
            G(L(lid, 0.15), bad, (45, 21))
            def good(l):
                code_card(l, (6, 28.5, 80, 37.5), ['key = ambil_dari_rahasia()'])
                check(l, 88, 33, 0.9)
            G(L(lid, 0.55), good, (45, 33))
            a2, sc2 = appear(t, L(lid, 0.7))
            lay = canvas(); badge(lay, 'simpan di pengaturan rahasia', 50, 42.5, F['mint'], F['white'], 30); comp(im, lay, a2, sc2, (50, 42.5))
        elif n == 2:
            items = [('chat', 0.3, 20), ('grup', 0.45, 50), ('screenshot', 0.62, 80)]
            for lab, f_, x in items:
                def f(l, lab=lab, x=x):
                    card(l, (x - 13, 17, x + 13, 33), r=30)
                    key_icon(l, x, 23, 0.5)
                    txt(l, lab, (x, 29.5), 32, F['ink'], 'SemiBold')
                    cross(l, x + 10, 18.5, 0.7)
                G(L(lid, f_), f, (x, 25))
            a2, sc2 = appear(t, L(lid, 0.15))
            lay = canvas(); badge(lay, 'jangan pernah dibagi', 50, 40, F['coral'], F['white'], 34); comp(im, lay, a2, sc2, (50, 40))
        else:
            def old(l):
                card(l, (6, 17, 42, 33), r=30)
                key_icon(l, 24, 22.5, 0.45, F['gray'])
                txt(l, 'key lama', (24, 29.5), 32, F['ink2'], 'SemiBold')
                if t >= L(lid, 0.5): line(l, 9, 22.5, 39, 22.5, F['red'], 8)
            G(L(lid, 0.2), old, (24, 25))
            a2, sc2 = appear(t, L(lid, 0.5))
            lay = canvas(); badge(lay, 'hapus', 24, 37, F['red'], F['white'], 28); comp(im, lay, a2, sc2, (24, 37))
            k = clamp((t - L(lid, 0.6)) / 0.4)
            if k > 0:
                lay = canvas(); arrow(lay, 45, 25, 53, 25, k, F['ink2'], 7); comp(im, lay)
            def new(l):
                card(l, (56, 17, 94, 33), r=30, outline=F['mint'])
                key_icon(l, 75, 22.5, 0.45, F['yellow'])
                txt(l, 'key baru', (75, 29.5), 32, F['ink'], 'SemiBold')
                check(l, 92, 18, 0.7)
            G(L(lid, 0.75), new, (75, 25))

    elif sid == 'SH12':   # banyak layanan banyak akun
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Makin banyak layanan...', (50, 10.5), 44, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 10.5))
        for i in range(6):
            x = 20 + (i % 3) * 30; y = 19 + (i // 3) * 11
            def f(l, x=x, y=y, i=i):
                card(l, (x - 12, y - 4.2, x + 12, y + 4.2), r=26)
                key_icon(l, x - 1, y - 1.2, 0.45, CHIPC[i % 5])
                txt(l, f'akun {i + 1}', (x, y + 2.4), 26, F['ink2'], 'SemiBold')
            G(L('L15', 0.15 + 0.08 * i), f, (x, y))
        a2, sc2 = appear(t, L('L15', 0.75))
        lay = canvas(); badge(lay, '...makin banyak yang harus dijaga', 50, 40.5, F['coral'], F['white'], 32); comp(im, lay, a2, sc2, (50, 40.5))

    elif sid == 'SH13':   # satu pintu
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); wordmark(lay, 50, 11, 220, tsize=42); comp(im, lay, a, sc, (50, 12))
        ys = (24, 31, 38)
        for i, y in enumerate(ys):
            def f(l, i=i, y=y): chip(l, 'Model ' + 'ABC'[i], 22, y, CHIPC[i], 34)
            G(L('L16', 0.35 + 0.1 * i), f, (22, y))
        k = clamp((t - L('L16', 0.6)) / 0.5)
        if k > 0:
            lay = canvas()
            for y in ys: arrow(lay, 35, y, 61, lerp(y, 31, 0.6), k, F['ink2'], 6)
            comp(im, lay)
        def door(l):
            rr(l, (63, 21, 83, 41), 22, F['ink']); rr(l, (65.5, 23.5, 80.5, 41), 14, F['blue']); circ(l, 78, 32, 10, F['yellow'])
            badge(l, 'satu pintu', 73, 44.5, F['blue'], F['white'], 28)
        G(L('L16', 0.65), door, (73, 31))

    elif sid == 'SH14':   # paket token per model
        def box(l):
            rr(l, (30, 16, 70, 33), 22, F['blue']); rr(l, (27.5, 13, 72.5, 17.5), 18, '#3561B3')
            rr(l, (47.8, 13, 52.2, 17.5), 6, F['yellow']); circ(l, 47.3, 12.3, 16, F['yellow']); circ(l, 52.7, 12.3, 16, F['yellow'])
            txt(l, 'PAKET TOKEN', (50, 25), 42, F['white'])
        G(L('L17', 0.1), box, (50, 23))
        a, sc = appear(t, L('L17', 0.45))
        lay = canvas(); badge(lay, 'per model', 50, 37, F['ink'], F['white'], 32); comp(im, lay, a, sc, (50, 37))
        a, sc = appear(t, L('L17', 0.7))
        lay = canvas(); badge(lay, 'Model A · ??M token (contoh)', 50, 42.5, F['yellow'], F['ink'], 30); comp(im, lay, a, sc, (50, 42.5))

    elif sid == 'SH15':   # jaga baik-baik
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); key_icon(lay, 50, 22, 1.2); comp(im, lay, a, sc, (50, 22))
        a, sc = appear(t, L('L18', 0.4))
        lay = canvas(); badge(lay, 'jaga baik-baik', 50, 35, F['mint'], F['white'], 38); comp(im, lay, a, sc, (50, 35))
        a, sc = appear(t, L('L18', 0.75))
        lay = canvas(); badge(lay, 'jangan dipinjemin', 50, 41.5, F['coral'], F['white'], 32); comp(im, lay, a, sc, (50, 41.5))

    elif sid == 'SH16':   # kunci hatiku
        a, sc = appear(t, L('L19', 0.2))
        lay = canvas(); key_icon(lay, 50, 22, 1.0, F['coral'])
        heart(lay, 42.5, 21.4, 1.0, F['white']); comp(im, lay, a, sc, (50, 22))
        for i, (x, y, s_, ph) in enumerate(((20, 32, 1.4, 0), (80, 26, 1.8, 1.1), (66, 40, 1.1, 2.2), (32, 14, 1.0, 3.1))):
            t0 = L('L19', 0.5 + 0.08 * i)
            if t < t0: continue
            p = t - t0
            lay = canvas(); heart(lay, x + 0.6 * math.sin(p * 2 + ph), y - p * 1.5, s_ * (0.7 + 0.3 * ease_out_back(clamp(p / 0.4))))
            comp(im, lay, min(1, p * 3))
        a, sc = appear(t, L('L19', 0.7))
        lay = canvas(); txt(lay, 'kunci hatiku', (50, 9.8), 50, F['coral'], 'Bold'); comp(im, lay, a, sc, (50, 9.8))

    elif sid == 'SH17':   # end card
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        card(lay, (10, 9, 90, 42), r=44)
        wordmark(lay, 50, 15, 240, tsize=50)
        txt(lay, 'Satu pintu, banyak model AI', (50, 26.5), 38, F['ink'], 'SemiBold')
        rr(lay, (18, 30, 82, 35.5), 40, F['blue']); txt(lay, 'app.sakelar.web.id', (50, 32.75), 42, F['white'], 'Bold')
        txt(lay, 'Ep 12 · API Key Itu Apa, Kenapa Harus Dijaga?', (50, 39), 28, F['ink2'], 'Medium')
        comp(im, lay, a, sc, (50, 25))


# Per-shot spec: goal, obj, anim (list of (t_rel, text)), text, sfx (list of (t_rel, name, len, dB, fn)), qa
def spec(sid):
    s = SH[sid]; d = round(s['end'] - s['start'], 3)
    if sid == 'SH01': return dict(
        goal='Hook: tagihan AI bengkak padahal nggak dipakai.',
        obj=['Kartu putih x=10–90%, y=9–38%: judul "Tagihan AI" (15%,13.5%), badge "bulan ini" (82%,13.5%).',
             'Grafik 5 batang x=15–57%, alas y=33%: 4 batang biru muda pendek, batang ke-5 coral naik sampai 15% tinggi.',
             '"Rp ???" merah (84%,22%, rata kanan) + panah merah ke atas (76%, 31→25.5%). Teks "ilustrasi" (50%,35.8%).',
             'Badge coral "padahal nggak dipakai?" (50%,43%).'],
        anim=[(0.15, 'Kartu pop-in.'), (r(sid, 'L01', 0.45), 'Batang ke-5 tumbuh 0.6 s easeOutCubic (saat "bengkak").'),
              (r(sid, 'L01', 0.55), 'Panah pop-in.'), (r(sid, 'L01', 0.8), 'Badge pop-in.')],
        text=['"Tagihan AI" Bold 40px.', '"bulan ini" Medium 24px.', '"Rp ???" Bold 46px merah.', '"ilustrasi" Medium 24px abu.', '"padahal nggak dipakai?" Medium 34px putih.'],
        sfx=[(0.15, 'pop', 0.15, -16, 'kartu'), (r(sid, 'L01', 0.45), 'tick', 0.6, -18, 'batang naik'), (r(sid, 'L01', 0.8), 'boing', 0.25, -16, 'badge')],
        qa=['Tidak ada angka tagihan karangan ("Rp ???").', 'Reina posisi kiri; subtitle balon di kanan.'])
    if sid == 'SH02': return dict(
        goal='Penyebab: API key bocor.',
        obj=['Ikon kunci kuning skala 1.4 di (50%,22%).', '3 tetes biru jatuh dari (60–66%, 25→34%) berulang.', 'Badge merah "BOCOR!" (50%,40%).'],
        anim=[(0.1, 'Kunci pop-in.'), (r(sid, 'L02', 0.6), 'Tetesan mulai, jeda 0.25 s antar tetes, y = 25 + 9·((0.9u) mod 1), memudar.'), (r(sid, 'L02', 0.7), 'Badge pop-in.')],
        text=['"BOCOR!" Medium 44px putih.'],
        sfx=[(r(sid, 'L02', 0.6), 'blip', 0.2, -18, 'tetes'), (r(sid, 'L02', 0.7), 'buzz', 0.25, -16, 'bocor')],
        qa=['Posisi closeup: subtitle tengah tidak menutupi wajah.'])
    if sid == 'SH03': return dict(
        goal='Analogi: API key = kunci rumah untuk akses layanan AI.',
        obj=['Rumah flat: atap coral, dinding putih x=14–34%, y=20–31%, pintu biru; label "rumah" (24%,34%).',
             'Kunci kuning skala 0.8 di (50%,22%).', 'Panah 62→70% + chip AI skala 0.6 (81%,22%) + label "layanan AI".', 'Badge navy "API key = kunci akses" (50%,41%).'],
        anim=[(r(sid, 'L03', 0.1), 'Rumah pop-in.'), (r(sid, 'L03', 0.2), 'Kunci pop-in.'), (r(sid, 'L03', 0.55), 'Panah + AI pop-in.'), (r(sid, 'L03', 0.7), 'Badge pop-in.')],
        text=['"rumah" / "layanan AI" SemiBold 30px abu.', '"API key = kunci akses" Medium 36px putih.'],
        sfx=[(r(sid, 'L03', 0.2), 'coin', 0.4, -18, 'kunci'), (r(sid, 'L03', 0.55), 'whoosh', 0.4, -18, 'ke AI'), (r(sid, 'L03', 0.7), 'pop', 0.15, -16, 'badge')],
        qa=['Reina kanan, subtitle balon kiri.'])
    if sid == 'SH04': return dict(
        goal='Bentuk API key: deretan huruf & angka acak.',
        obj=['Kartu x=8–92%, y=13–27%: label "API KEY" (13%,16.6%), teks "sk-contoh-8fK2qL9xR7mT4vB1" Bold 48px (13%,22%) diketik bertahap.',
             'Chip "huruf" biru (30%,33%), "angka" coral (50%,33%), "acak" mint (70%,33%).', 'Catatan "contoh, bukan key asli" (50%,40%).'],
        anim=[(r(sid, 'L04', 0.05), 'Kartu pop-in.'), (r(sid, 'L04', 0.15), 'Teks key muncul huruf per huruf selama 0.6 s.'),
              (r(sid, 'L04', 0.4), 'Catatan muncul.'), (r(sid, 'L04', 0.55), 'Tiga chip pop-in.')],
        text=['"API KEY" SemiBold 26px.', 'Key contoh Bold 48px navy.', 'Chip Medium 34px.', '"contoh, bukan key asli" Medium 26px abu.'],
        sfx=[(r(sid, 'L04', 0.15), 'clicks', 0.6, -18, 'ketik'), (r(sid, 'L04', 0.55), 'pop_hi', 0.2, -16, 'chip')],
        qa=['Key jelas ditandai contoh, tidak menyerupai key layanan asli secara lengkap.'])
    if sid == 'SH05': return dict(
        goal='Siapa pun yang pegang key bisa pakai layanan atas nama kamu — termasuk kuota & saldo.',
        obj=['Ikon "kamu" biru (18%,15%) + label; ikon "orang lain" merah (18%,30%) + label + kunci kecil (33%,30%).',
             'Panah abu kamu→AI dan panah merah orang lain→AI; chip AI skala 0.55 (62%,23%); badge coral "atas nama kamu" (62%,33%).',
             'L06: label "kuota & saldo kamu" (12%,40.5%) + bar x=12–88%, y=42.5–45.5% menyusut (mint → merah).'],
        anim=[(0.1, 'Ikon kamu pop-in.'), (r(sid, 'L05', 0.15), 'AI + panah pertama.'), (r(sid, 'L05', 0.3), 'Orang lain + kunci pop-in; panah merah tumbuh 0.4 s.'),
              (r(sid, 'L05', 0.8), 'Badge pop-in.'), (r(sid, 'L06', 0.1), 'Bar kuota menyusut sampai 8% sisa; warna jadi merah setelah setengah jalan.')],
        text=['"kamu" / "orang lain" SemiBold 30px.', '"atas nama kamu" Medium 28px.', '"kuota & saldo kamu" SemiBold 30px.'],
        sfx=[(r(sid, 'L05', 0.3), 'swipe', 0.3, -18, 'orang lain'), (r(sid, 'L06', 0.1), 'whoosh', 0.8, -20, 'kuota turun')],
        qa=['Reina kanan; balon subtitle kiri (y≈60%) tidak menabrak bar kuota (y≤45.5%).'])
    if sid == 'SH06': return dict(
        goal='Key bocor karena hal sepele: ditempel di kode publik atau kefoto di screenshot.',
        obj=['Judul "Bocor karena hal sepele" (50%,10.5%).',
             'Kartu kode gelap x=5–55%, y=15–33%: 3 baris, baris key disorot merah; badge "PUBLIK" (49%,17.4%); ✕ (30%,37.3%).',
             'Bingkai screenshot x=61–95%, y=15–33% dengan sudut navy, baris key disorot kuning; label "screenshot" (78%,35.7%); ✕ (78%,39.5%).',
             'Catatan "contoh (ilustrasi)" (50%,45%).'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L07', 0.2), 'Catatan muncul.'), (r(sid, 'L08', 0.05), 'Kartu kode + ✕ pop-in.'), (r(sid, 'L08', 0.62), 'Screenshot + ✕ pop-in.')],
        text=['Judul Bold 44px.', 'Kode Medium 30px (verbatim).', '"PUBLIK" 22px.', '"screenshot" SemiBold 28px.', 'Catatan 24px abu.'],
        sfx=[(r(sid, 'L08', 0.05), 'buzz', 0.25, -18, 'kode'), (r(sid, 'L08', 0.62), 'click', 0.1, -14, 'jepret'), (r(sid, 'L08', 0.65), 'buzz', 0.25, -18, 'screenshot')],
        qa=['Reina kiri, balon subtitle kanan.'])
    if sid == 'SH07': return dict(
        goal='Fakta unik: ada bot yang mencari key bocor; key yang ketahuan bisa disalahgunakan dalam waktu singkat.',
        obj=['Kartu x=8–92%, y=9–34% berisi 6 baris kode abu.', 'Kaca pembesar r=40px menyapu baris (x = 40 + 22·sin(1.54u), y bolak-balik 13–29.5%).',
             'Robot kecil (80%,20%).', 'Saat ketemu: baris y≈26.5% disorot merah + teks "key = \\"sk-...\\"".',
             'Badge navy "bot pencari key bocor" (50%,38.5%); badge coral "key bocor = bahaya" (50%,43.5%).'],
        anim=[(0.05, 'Kartu + robot + kaca pembesar muncul.'), (r(sid, 'L09', 0.3), 'Badge bot pop-in.'),
              (r(sid, 'L09', 0.75), 'Kaca pembesar berhenti di baris key; sorot merah.'), (r(sid, 'L10', 0.5), 'Badge coral pop-in.')],
        text=['"key = \\"sk-...\\"" Bold 26px merah.', 'Badge Medium 32px / 28px.'],
        sfx=[(0.05, 'hum', d - 0.1, -24, 'scan'), (r(sid, 'L09', 0.75), 'ding', 0.4, -14, 'ketemu'), (r(sid, 'L10', 0.5), 'buzz', 0.25, -18, 'bahaya')],
        qa=['Tidak menyebut angka waktu pasti — "dalam waktu singkat".', 'Pose desk = posisi tengah; monitor tidak menutupi subtitle.'])
    if sid == 'SH08': return dict(
        goal='Transisi ke tips.',
        obj=['Judul 2 baris "3 CARA JAGA / API KEY" Bold 82px (50%,18%).', 'Lingkaran r=52px angka 1/2/3 di (32,35), (50,35), (68,35).'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L11', 0.2), 'Lingkaran pop-in tiap +25%.')],
        text=['"3 CARA JAGA\\nAPI KEY"', '"1" "2" "3"'], sfx=[(r(sid, 'L11', 0.2), 'pop_hi', 0.6, -14, 'angka')], qa=['Judul tidak terpotong.'])
    if sid in ('SH09', 'SH10', 'SH11'):
        n = {'SH09': 1, 'SH10': 2, 'SH11': 3}[sid]; lid = ['L12', 'L13', 'L14'][n - 1]
        head = 'Header: lingkaran nomor "' + str(n) + '" r=46px (12%,11.5%) + judul Bold 44px x=19.5% left.'
        base = dict(goal=['Tips 1: jangan tempel key di kode.', 'Tips 2: jangan bagi key di chat, grup, screenshot.', 'Tips 3: kalau curiga bocor, hapus & bikin key baru.'][n - 1])
        if n == 1: base.update(
            obj=[head, 'Kartu kode x=6–80%, y=16.5–25.5%: `key = "sk-contoh-8fK2..."` disorot merah + ✕ (88%,21%).',
                 'Kartu kode y=28.5–37.5%: `key = ambil_dari_rahasia()` + ✓ (88%,33%).', 'Badge mint "simpan di pengaturan rahasia" (50%,42.5%).'],
            anim=[(0.05, 'Header.'), (r(sid, lid, 0.15), 'Kode buruk + ✕.'), (r(sid, lid, 0.55), 'Kode aman + ✓.'), (r(sid, lid, 0.7), 'Badge.')],
            text=['"Jangan tempel di kode"', 'Kode Medium 30px (verbatim).', 'Badge Medium 30px.'],
            sfx=[(r(sid, lid, 0.15), 'buzz', 0.25, -18, '✕'), (r(sid, lid, 0.55), 'ding', 0.4, -16, '✓')])
        if n == 2: base.update(
            obj=[head, 'Tiga kartu lebar 26% di x=20/50/80%, y=17–33%: kunci kecil + label "chat" / "grup" / "screenshot" + ✕ di pojok kanan atas.', 'Badge coral "jangan pernah dibagi" (50%,40%).'],
            anim=[(0.05, 'Header.'), (r(sid, lid, 0.15), 'Badge.'), (r(sid, lid, 0.3), 'Kartu chat.'), (r(sid, lid, 0.45), 'Kartu grup.'), (r(sid, lid, 0.62), 'Kartu screenshot.')],
            text=['"Jangan dibagi-bagi"', 'Label SemiBold 32px.', 'Badge Medium 34px.'],
            sfx=[(r(sid, lid, 0.3), 'pop', 0.15, -16, 'chat'), (r(sid, lid, 0.45), 'pop', 0.15, -16, 'grup'), (r(sid, lid, 0.62), 'pop_hi', 0.15, -16, 'screenshot')])
        if n == 3: base.update(
            obj=[head, 'Kartu "key lama" x=6–42%, y=17–33% (kunci abu), dicoret merah; badge merah "hapus" (24%,37%).',
                 'Panah 45→53% di y=25%.', 'Kartu "key baru" x=56–94% outline mint, kunci kuning, ✓ (92%,18%).'],
            anim=[(0.05, 'Header.'), (r(sid, lid, 0.2), 'Key lama pop-in.'), (r(sid, lid, 0.5), 'Coret + badge hapus.'), (r(sid, lid, 0.6), 'Panah tumbuh 0.4 s.'), (r(sid, lid, 0.75), 'Key baru pop-in.')],
            text=['"Bocor? Hapus, bikin baru"', '"key lama" / "key baru" SemiBold 32px.', '"hapus" Medium 28px.'],
            sfx=[(r(sid, lid, 0.5), 'scratch', 0.3, -18, 'hapus'), (r(sid, lid, 0.75), 'chime', 0.6, -16, 'key baru')])
        base['qa'] = ['Nomor tips sama dengan urutan dialog.', 'Contoh kode ditulis persis.']
        return base
    if sid == 'SH12': return dict(
        goal='Jembatan soft sell: makin banyak layanan AI, makin banyak akun yang harus dijaga.',
        obj=['Judul "Makin banyak layanan..." (50%,10.5%).', 'Grid 6 kartu kecil 24%×8.4% di x=20/50/80%, y=19/30%: kunci warna + "akun 1…6".',
             'Badge coral "...makin banyak yang harus dijaga" (50%,40.5%).'],
        anim=[(0.05, 'Judul.'), (r(sid, 'L15', 0.15), 'Kartu akun pop-in tiap +8%.'), (r(sid, 'L15', 0.75), 'Badge.')],
        text=['Judul Bold 44px.', '"akun 1"…"akun 6" SemiBold 26px.', 'Badge Medium 32px.'],
        sfx=[(r(sid, 'L15', 0.15), 'stack', 0.6, -18, 'akun menumpuk'), (r(sid, 'L15', 0.75), 'pop', 0.15, -16, 'badge')],
        qa=['Tidak menyebut nama layanan asli.'])
    if sid == 'SH13': return dict(
        goal='Soft sell: di Sakelar AI banyak model lewat satu pintu.',
        obj=['Logo Sakelar toggle + "Sakelar AI" via wordmark() lebar 220px di (50%,11%).', 'Chip "Model A/B/C" di x=22%, y=24/31/38%.',
             'Panah 35→61% menyatu ke pintu.', 'Pintu: kusen navy x=63–83%, y=21–41%, daun biru, gagang kuning; badge "satu pintu" (73%,44.5%).'],
        anim=[(0.05, 'Logo pop-in.'), (r(sid, 'L16', 0.35), 'Chip model tiap +10%.'), (r(sid, 'L16', 0.6), 'Panah tumbuh 0.5 s.'), (r(sid, 'L16', 0.65), 'Pintu + badge.')],
        text=['"Sakelar AI"', '"Model A/B/C" Medium 34px (placeholder).', '"satu pintu" Medium 28px.'],
        sfx=[(0.05, 'jingle', 0.6, -14, 'logo'), (r(sid, 'L16', 0.65), 'chime', 0.6, -14, 'satu pintu')],
        qa=['Logo memakai logo toggle baru lewat wordmark().', 'Tidak diklaim "satu API key".'])
    if sid == 'SH14': return dict(
        goal='Token dijual dalam paket per model.',
        obj=['Kotak "PAKET TOKEN" biru x=30–70%, y=16–33%, tutup x=27.5–72.5%, pita & simpul kuning di tutup.', 'Badge navy "per model" (50%,37%).',
             'Badge kuning "Model A · ??M token (contoh)" (50%,42.5%).'],
        anim=[(r(sid, 'L17', 0.1), 'Kotak pop-in.'), (r(sid, 'L17', 0.45), 'Badge per model.'), (r(sid, 'L17', 0.7), 'Badge isi paket.')],
        text=['"PAKET TOKEN" Bold 42px.', '"per model" Medium 32px.', '"Model A · ??M token (contoh)" Medium 30px — PLACEHOLDER.'],
        sfx=[(r(sid, 'L17', 0.1), 'coins', 0.8, -18, 'paket'), (r(sid, 'L17', 0.7), 'ding', 0.4, -16, 'isi')],
        qa=['Isi paket placeholder sampai ada data resmi.'])
    if sid == 'SH15': return dict(
        goal='Rangkuman: API key itu kunci, jaga baik-baik.',
        obj=['Kunci kuning skala 1.2 (50%,22%).', 'Badge mint "jaga baik-baik" (50%,35%).', 'Badge coral "jangan dipinjemin" (50%,41.5%).'],
        anim=[(0.05, 'Kunci pop-in.'), (r(sid, 'L18', 0.4), 'Badge mint.'), (r(sid, 'L18', 0.75), 'Badge coral.')],
        text=['"jaga baik-baik" Medium 38px.', '"jangan dipinjemin" Medium 32px.'],
        sfx=[(0.05, 'coin', 0.4, -16, 'kunci'), (r(sid, 'L18', 0.75), 'pop', 0.15, -16, 'badge')], qa=['Reina kiri, balon kanan.'])
    if sid == 'SH16': return dict(
        goal='Punchline manis: kunci hati Reina dititipkan ke penonton.',
        obj=['Kunci coral (50%,22%) dengan hati putih di kepala kunci.', '4 hati coral melayang di (20,32), (80,26), (66,40), (32,14).', 'Teks "kunci hatiku" Bold 50px coral (50%,9.8%).'],
        anim=[(r(sid, 'L19', 0.2), 'Kunci-hati pop-in.'), (r(sid, 'L19', 0.5), 'Hati muncul tiap +8%, naik 1.5%/s, goyang x.'), (r(sid, 'L19', 0.7), 'Teks pop-in.')],
        text=['"kunci hatiku" Bold 50px coral.'],
        sfx=[(r(sid, 'L19', 0.5), 'sparkle', 1.0, -18, 'hati'), (r(sid, 'L19', 0.7), 'pop_hi', 0.2, -16, 'teks')],
        qa=['Mulut sprite smile.', 'Posisi closeup.'])
    if sid == 'SH17': return dict(
        goal='End card: ajakan mencoba Sakelar AI.',
        obj=['Kartu putih x=10–90%, y=9–42%.', 'Logo toggle + "Sakelar AI" via wordmark() 240px (50%,15%).', '"Satu pintu, banyak model AI" (50%,26.5%).',
             'Tombol biru x=18–82%, y=30–35.5% "app.sakelar.web.id".', '"Ep 12 · API Key Itu Apa, Kenapa Harus Dijaga?" (50%,39%).'],
        anim=[(0.05, 'Kartu pop-in.'), (round(d - 0.5, 3), 'Fade ke warna latar 0.5 s.')],
        text=['"Satu pintu, banyak model AI" Medium 38px.', '"app.sakelar.web.id" Bold 42px putih.', 'Judul episode Medium 28px abu.'],
        sfx=[(0.05, 'stinger', 1.2, -12, 'end card'), (0.1, 'jingle', 0.6, -16, 'logo')],
        qa=['URL persis "app.sakelar.web.id".', 'Logo toggle baru.'])
