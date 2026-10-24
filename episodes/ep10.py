"""Reina Explains AI — Episode 10: "Prompt yang Bagus Itu Kayak Gimana?" (cara menulis prompt yang jelas).
Satu file = satu episode: naskah, shot, pose, visual panel(t), spec storyboard + SFX, arahan VO.
Jalankan:  python run.py stage1 episodes/ep10.py   lalu   python run.py stage2 episodes/ep10.py <zip_suara>"""
import math
from PIL import Image, ImageDraw
from reina import *

EP = 10
TITLE = 'Prompt yang Bagus Itu Kayak Gimana?'
SCENES = {1: 'Hook', 2: 'Prompt itu apa', 3: 'AI nggak bisa baca pikiran', 4: 'Fakta unik', 5: 'Tips 3 bahan prompt',
          6: 'Soft sell Sakelar AI', 7: 'Closing', 8: 'End card'}
META = dict(
    tujuan='Menjelaskan apa itu prompt dan ciri prompt yang bagus (jelas: konteks, tugas, format) dengan analogi pesan nasi goreng; soft sell Sakelar AI sebagai satu pintu ke banyak model',
    konsep=('Hook: minta "bikinin caption", hasilnya biasa banget → bisa jadi prompt-nya kurang jelas → prompt = pesan/perintah yang diketik ke AI → '
            'analogi pesan nasi goreng: "satu" dapat standar, detail (pedas, telur dadar, tanpa acar) dapat yang pas → AI nggak bisa baca pikiran, cuma kerja dari info yang dikasih → '
            'fakta unik: bisa minta AI nanya balik dulu → 3 bahan prompt bagus: konteks, tugas jelas, format → soft sell: prompt sama bisa beda gaya di model beda, '
            'banyak model lewat satu pintu, tes satu prompt ke beberapa model, paket token per model → rangkuman "bukan panjang, tapi jelas" → punchline manis.'),
    fakta=['Prompt = teks instruksi/pertanyaan yang diberikan pengguna ke model AI.',
           'Model hanya bisa memakai informasi yang ada di prompt/percakapan (plus pengetahuan latihnya) — tidak bisa menebak maksud yang tidak ditulis.',
           'Menambahkan konteks, tugas yang spesifik, dan format yang diinginkan umumnya membuat jawaban lebih sesuai (praktik umum prompting, bukan jaminan).',
           'Pengguna bisa meminta AI mengajukan pertanyaan klarifikasi sebelum mengerjakan tugas.',
           'Model yang berbeda bisa menjawab prompt yang sama dengan gaya berbeda.',
           'Sakelar AI = satu pintu (gateway) ke banyak model; token dijual dalam paket per model (sekian juta token / "M").',
           'CTA URL: app.sakelar.web.id.'],
    asumsi=['Semua isi chat (caption "Hari yang indah", pertanyaan balik AI, contoh prompt kopi susu) adalah ilustrasi — label "contoh"/"ilustrasi" tampil.',
            'Gaya jawaban Model A/B/C di SH15 ("kalem/ceria/ringkas") adalah ilustrasi, bukan perilaku model asli.',
            'Tidak diklaim Sakelar AI punya fitur khusus "bandingkan prompt" — L17 hanya bilang kamu bisa coba prompt yang sama ke beberapa model (konsekuensi dari akses banyak model).',
            'Tidak menyebut hasil "pasti" lebih bagus — naskah memakai "bisa jadi" dan "pas sama selera".'],
    konfirmasi=['Nama model di SH15–SH18 masih placeholder ("Model A/B/C", contoh).',
                'Isi paket di SH18 masih "??M token (contoh)" — ganti kalau ada data resmi.'],
    softsell='SH15–SH18 + end card',
)
PRON = [('AI', 'ei-ai'), ('prompt', 'promt'), ('caption', 'kep-syen'), ('Sakelar', 'sa-ke-lar')]
VO_DIR = {'L01': 'santai, menirukan nyuruh singkat di "Bikinin caption", kecewa di "biasa banget"',
 'L02': 'menenangkan, sedikit jahil di "prompt-nya yang kurang jelas"',
 'L03': 'menjelaskan, jelas sebut "prompt" (promt)', 'L04': 'nada bercerita, ceria di "abang nasi goreng"',
 'L05': 'datar menirukan pesanan "nasi goreng satu", lalu santai', 'L06': 'ritmis menyebut pesanan detail, puas di "pas sama selera kamu"',
 'L07': 'tegas tapi lucu di "nggak bisa baca pikiran"', 'L08': 'tenang, menekankan "informasi yang kamu kasih"',
 'L09': 'nada "fakta seru", semangat di "Uniknya"', 'L10': 'ringan, sedikit geli di "dia yang nanya ke kamu"',
 'L11': 'energik, membuka daftar', 'L12': 'jelas, tekan "konteks"', 'L13': 'jelas, ritmis di "apa, buat siapa, berapa panjang"',
 'L14': 'ceria, tekan "format"', 'L15': 'nada "nah" naik, menjelaskan', 'L16': 'ramah, meyakinkan',
 'L17': 'santai, ceria di "paling cocok"', 'L18': 'menjelaskan, "M" tidak disebut — cukup "juta token"',
 'L19': 'menyimpulkan, mantap, tekan "jelas"',
 'L20': 'malu-malu manis, pelan, jeda di "Kayak aku ke kamu...", senyum di "aku suka"'}

# ---- naskah terkunci (1 item = 1 baris VO = L01, L02, ...) ----
LINES = [
 'Kamu nyuruh AI, "Bikinin caption," terus hasilnya biasa banget?',
 'Jangan buru-buru nyalahin AI-nya. Bisa jadi prompt-nya yang kurang jelas.',
 'Prompt itu pesan atau perintah yang kamu ketik ke AI.',
 'Ibaratnya kayak pesan makanan ke abang nasi goreng.',
 'Kalau cuma bilang "nasi goreng satu", ya kamu dapat yang standar.',
 'Tapi kalau bilang "pedas, telur dadar, tanpa acar", hasilnya pas sama selera kamu.',
 'AI juga gitu. Dia nggak bisa baca pikiran kamu.',
 'Dia cuma bisa kerja dari informasi yang kamu kasih.',
 'Uniknya, kamu bisa minta AI nanya balik dulu sebelum mulai.',
 'Jadi kalau ada yang kurang jelas, dia yang nanya ke kamu.',
 'Ini tiga bahan prompt yang bagus.',
 'Satu, konteks. Ceritain kamu siapa dan hasilnya buat apa.',
 'Dua, tugas yang jelas. Mau dibikinin apa, buat siapa, berapa panjang.',
 'Tiga, format. Mau bentuk poin, tabel, atau gaya bahasa santai.',
 'Nah, prompt yang sama bisa dijawab beda gaya sama model yang beda.',
 'Di Sakelar AI, kamu bisa akses banyak model lewat satu pintu.',
 'Jadi kamu bisa coba prompt yang sama ke beberapa model, terus pilih yang paling cocok.',
 'Tokennya dijual dalam paket per model, isinya sekian juta token.',
 'Jadi prompt yang bagus itu bukan yang paling panjang, tapi yang paling jelas.',
 'Kayak aku ke kamu... nggak pakai kode-kodean, langsung jelas: aku suka.',
]

# (id, scene, judul, [nomor baris], jeda_awal_s, jeda_akhir_s)
SHOTS = [
 ('SH01', 1, '"Bikinin caption" = hasil biasa', [1], 0.5, 0.2),
 ('SH02', 1, 'Bukan AI-nya, prompt-nya', [2], 0.15, 0.4),
 ('SH03', 2, 'Prompt = pesan ke AI', [3], 0.25, 0.2),
 ('SH04', 2, 'Pesan nasi goreng', [4], 0.15, 0.2),
 ('SH05', 2, '"Nasi goreng satu" = standar', [5], 0.15, 0.2),
 ('SH06', 2, 'Pesanan detail = pas selera', [6], 0.15, 0.4),
 ('SH07', 3, 'Nggak bisa baca pikiran', [7], 0.25, 0.2),
 ('SH08', 3, 'Kerja dari info yang dikasih', [8], 0.15, 0.4),
 ('SH09', 4, 'Minta AI nanya balik', [9], 0.25, 0.2),
 ('SH10', 4, 'AI yang nanya ke kamu', [10], 0.15, 0.4),
 ('SH11', 5, 'Tiga bahan prompt bagus', [11], 0.25, 0.15),
 ('SH12', 5, 'Bahan 1: konteks', [12], 0.1, 0.2),
 ('SH13', 5, 'Bahan 2: tugas jelas', [13], 0.1, 0.2),
 ('SH14', 5, 'Bahan 3: format', [14], 0.1, 0.4),
 ('SH15', 6, 'Prompt sama, gaya beda', [15], 0.25, 0.2),
 ('SH16', 6, 'Banyak model, satu pintu', [16], 0.1, 0.2),
 ('SH17', 6, 'Coba prompt ke beberapa model', [17], 0.1, 0.2),
 ('SH18', 6, 'Paket token per model', [18], 0.1, 0.4),
 ('SH19', 7, 'Bukan panjang, tapi jelas', [19], 0.25, 0.25),
 ('SH20', 7, 'Langsung jelas: aku suka', [20], 0.1, 0.6),
 ('SH21', 8, 'End card', [], 0.0, 2.5),
]

POSE = {'SH01': 'phone', 'SH02': 'arms34', 'SH03': 'desk', 'SH04': 'point_up', 'SH05': 'arms34', 'SH06': 'thumbs_up',
        'SH07': 'bust', 'SH08': 'point', 'SH09': 'point_up', 'SH10': 'phone', 'SH11': 'hands_on_hips',
        'SH12': 'point_up', 'SH13': 'point', 'SH14': 'thumbs_up', 'SH15': 'arms34', 'SH16': 'wave',
        'SH17': 'phone', 'SH18': 'thumbs_up', 'SH19': 'hands_on_hips', 'SH20': 'shy_lean', 'SH21': 'wave'}
SMILE = {'SH20'}   # shot yang pakai mulut senyum
EXPR = {'SH01': 'kecewa sambil lihat HP', 'SH02': 'menenangkan, analitis', 'SH03': 'fokus mengetik di monitor',
        'SH04': 'bercerita, ceria', 'SH05': 'datar, lucu', 'SH06': 'puas, jempol', 'SH07': 'penekanan, tangan bersilang',
        'SH08': 'serius, menunjuk penonton', 'SH09': 'semangat, "uniknya"', 'SH10': 'geli sambil lihat HP',
        'SH11': 'percaya diri', 'SH12': 'menjelaskan', 'SH13': 'menunjuk, tegas', 'SH14': 'ceria',
        'SH15': 'analitis', 'SH16': 'ramah, menyapa', 'SH17': 'menjelaskan sambil lihat HP', 'SH18': 'ceria, meyakinkan',
        'SH19': 'mantap, menutup', 'SH20': 'malu-malu, senyum (mulut smile)', 'SH21': 'ceria, melambai'}


# ---------------- helper lokal ----------------
def plate(l, cx, cy, s=1.0, egg=False, chili=False):
    """Piring nasi goreng flat. s = skala."""
    ell(l, cx, cy + 0.5 * s, 190 * s, 62 * s, F['ink'], a=40)
    ell(l, cx, cy, 190 * s, 62 * s, F['ink2'])
    ell(l, cx, cy - 0.15 * s, 182 * s, 56 * s, F['white'])
    ell(l, cx, cy - 1.0 * s, 120 * s, 58 * s, '#E3A857')
    ell(l, cx, cy - 1.4 * s, 100 * s, 44 * s, '#F0BF6E')
    for i, (dx, dy) in enumerate(((-4, -1.6), (2, -2.6), (5, -0.6), (-1, -0.2), (-6, -0.4))):
        circ(l, cx + dx * s, cy + dy * s, 6 * s, '#C98A3E')
    if egg:
        ell(l, cx + 4.5 * s, cy - 2.6 * s, 62 * s, 30 * s, '#FFF6DC')
        ell(l, cx + 4.5 * s, cy - 2.7 * s, 46 * s, 22 * s, F['yellow'])
    if chili:
        for i, (dx, dy) in enumerate(((-7, -2.2), (-3, -3.6), (0, -1.0), (-8.5, 0.2), (8.5, -0.4))):
            circ(l, cx + dx * s, cy + dy * s, 7 * s, F['red'])

def input_bar(l, x0, x1, y, s, size=34, caret=True, t=0.0):
    card(l, (x0, y - 2.6, x1, y + 2.6), r=40)
    txt(l, s, (x0 + 3, y), size, F['ink'], 'Medium', 'lm')
    circ(l, x1 - 4.2, y, 30, F['blue'])
    poly(l, [(x1 - 5.4, y - 1.0), (x1 - 2.8, y), (x1 - 5.4, y + 1.0)], F['white'])
    if caret and (t * 2) % 1 < 0.6:
        cw = tw_px(s, size, 'Medium') / W * 100
        rr(l, (x0 + 3.4 + cw, y - 1.2, x0 + 3.9 + cw, y + 1.2), 3, F['ink'])

def thought(l, cx, cy, wpx, hpx, s='', size=50):
    """Awan pikiran: elips putih + 2 titik kecil ke kiri bawah."""
    ell(l, cx, cy, wpx, hpx, F['white'])
    circ(l, cx - wpx / W * 100 * 0.55, cy + hpx / H * 100 * 1.25, 18, F['white'])
    circ(l, cx - wpx / W * 100 * 0.8, cy + hpx / H * 100 * 1.85, 10, F['white'])
    if s: txt(l, s, (cx, cy), size, F['ink'], 'Bold')

def door(l):
    rr(l, (64, 20, 84, 40), 22, F['ink']); rr(l, (66.5, 22.5, 81.5, 40), 14, F['blue'])
    circ(l, 79, 31, 10, F['yellow'])


def panel(t, sid, im):
    """Gambar panel visual (area y 7–47%) shot sid pada waktu t ke layer 2x im."""
    s = SH[sid]; u = t - s['start']; L = lambda lid, f=0.0: rel(lid, f)
    def G(t0, fn, anchor=(50, 25), d=0.35, dy=0.0):
        a, sc = appear(t, t0, d)
        if a <= 0: return
        lay = canvas(); fn(lay); comp(im, lay, a, sc, anchor, dy)
    def note(s_, y, t0, size=24):
        lay = canvas(); txt(lay, s_, (50, y), size, F['ink2'], 'Medium'); comp(im, lay, *appear(t, t0), (50, y))

    if sid == 'SH01':   # "Bikinin caption" -> bland result
        def q(l): bubble(l, (46, 9.5, 92, 14.8), 'Bikinin caption.', 'u', size=36)
        G(L('L01', 0.25), q, (69, 12))
        def ans(l):
            bubble(l, (8, 17.5, 74, 24.5), 'Ini caption-nya:\n"Hari yang indah."', 'a', size=34)
            txt(l, 'AI', (78, 21), 26, F['ink2'], 'SemiBold', 'lm')
        G(L('L01', 0.6), ans, (41, 21))
        a, sc = appear(t, L('L01', 0.8))
        lay = canvas(); badge(lay, 'kok biasa banget?', 50, 33.5, F['coral'], F['white'], 38); comp(im, lay, a, sc, (50, 33.5))
        a2, sc2 = appear(t, L('L01', 0.85))
        lay = canvas()
        for i, x in enumerate((24, 76)):
            txt(lay, '...', (x, 33.2 + 0.4 * math.sin(t * 3 + i)), 60, F['ink2'])
        comp(im, lay, a2, sc2, (50, 33.5))
        note('contoh chat (ilustrasi)', 44, L('L01', 0.6))

    elif sid == 'SH02':   # not the AI, the prompt
        def left(l):
            card(l, (7, 10, 43, 32), r=36)
            cross(l, 25, 16.5, 1.2)
            txt(l, 'AI-nya\nsalah?', (25, 25.6), 44, F['ink2'], 'Bold', spacing=4)
        G(L('L02', 0.15), left, (25, 21))
        def right(l):
            card(l, (47, 10, 93, 32), r=36, outline=F['mint'])
            check(l, 70, 16.5, 1.2)
            txt(l, 'prompt-nya\nkurang jelas', (70, 25.6), 40, F['ink'], 'Bold', spacing=4)
        G(L('L02', 0.6), right, (70, 21))
        a, sc = appear(t, L('L02', 0.8))
        lay = canvas(); badge(lay, 'bisa jadi ini penyebabnya', 50, 39.5, F['ink'], F['white'], 34); comp(im, lay, a, sc, (50, 39.5))

    elif sid == 'SH03':   # prompt = message to AI
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Prompt itu apa?', (50, 11), 48, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 11))
        a1, sc1 = appear(t, L('L03', 0.15))
        if a1 > 0:
            full = 'Bikinin caption...'
            n = int(clamp((t - L('L03', 0.15)) / 1.0) * len(full))
            lay = canvas(); input_bar(lay, 8, 60, 22, full[:n], 34, True, t); comp(im, lay, a1, sc1, (34, 22))
        a2, sc2 = appear(t, L('L03', 0.35))
        lay = canvas(); badge(lay, 'PROMPT', 22, 28.6, F['coral'], F['white'], 30); comp(im, lay, a2, sc2, (22, 28.6))
        k = clamp((t - L('L03', 0.6)) / 0.35)
        if k > 0:
            lay = canvas(); arrow(lay, 62, 22, 70, 22, k, F['ink2'], 8); comp(im, lay)
        def ai(l): ai_box(l, 81, 22, 0.55)
        G(L('L03', 0.75), ai, (81, 22))
        a3, sc3 = appear(t, L('L03', 0.8))
        lay = canvas(); badge(lay, '= pesan / perintah yang kamu ketik', 50, 37.5, F['mint'], F['white'], 32); comp(im, lay, a3, sc3, (50, 37.5))

    elif sid == 'SH04':   # nasi goreng analogy
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Ibarat pesan nasi goreng', (50, 11), 46, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 11))
        def cart(l):
            card(l, (14, 16, 86, 38), r=40)
            rr(l, (20, 19, 80, 23.5), 20, F['coral'])
            txt(l, 'NASI GORENG', (50, 21.25), 40, F['white'], 'Bold')
            plate(l, 50, 31.2, 1.0)
        G(L('L04', 0.45), cart, (50, 27))
        if t >= L('L04', 0.6):
            lay = canvas()
            for i in range(3):   # steam rising: pure function of t
                ph = ((t - L('L04', 0.6)) * 0.6 + i / 3.0) % 1.0
                x = 44 + 6 * i + 0.8 * math.sin(ph * 6 + i)
                circ(lay, x, 27.5 - 4 * ph, 10 + 8 * ph, F['ink2'], a=int(120 * clamp(min(ph / 0.15, (1 - ph) / 0.4))))
            comp(im, lay)
        a2, sc2 = appear(t, L('L04', 0.8))
        lay = canvas(); badge(lay, 'pesanan = prompt', 50, 43, F['ink'], F['white'], 32); comp(im, lay, a2, sc2, (50, 43))

    elif sid == 'SH05':   # "nasi goreng satu" -> standard
        def q(l): bubble(l, (30, 9.5, 92, 14.8), '"Nasi goreng satu."', 'u', size=36)
        G(L('L05', 0.2), q, (61, 12))
        def p(l):
            card(l, (22, 18, 78, 35), r=36)
            plate(l, 50, 27.6, 1.0)
        G(L('L05', 0.65), p, (50, 26.5))
        a, sc = appear(t, L('L05', 0.82))
        lay = canvas(); badge(lay, 'standar', 50, 40.5, F['ink2'], F['white'], 36); comp(im, lay, a, sc, (50, 40.5))

    elif sid == 'SH06':   # detailed order -> fits taste
        def q(l): bubble(l, (8, 9.5, 92, 14.8), '"Pedas, telur dadar, tanpa acar."', 'u', size=36)
        G(L('L06', 0.12), q, (50, 12))
        items = [('pedas', F['red']), ('telur dadar', F['yellow']), ('tanpa acar', F['mint'])]
        for i, (lab, col) in enumerate(items):
            def f(l, lab=lab, col=col, i=i): chip(l, lab, 21, 20.5 + i * 5.6, col, 32)
            G(L('L06', 0.2 + 0.12 * i), f, (21, 20.5 + i * 5.6))
        def p(l):
            card(l, (40, 17.5, 92, 35), r=36, outline=F['mint'])
            plate(l, 66, 27.4, 1.0, egg=True, chili=True)
        G(L('L06', 0.62), p, (66, 26))
        a, sc = appear(t, L('L06', 0.8))
        lay = canvas(); check(lay, 88, 18.8, 0.8); badge(lay, 'pas sama selera kamu', 50, 40.5, F['mint'], F['white'], 34)
        comp(im, lay, a, sc, (50, 35))

    elif sid == 'SH07':   # can't read your mind
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); ai_box(lay, 36, 27, 0.75); comp(im, lay, a, sc, (36, 27))
        def th(l): thought(l, 70, 16.5, 170, 80, '???', 60)
        G(L('L07', 0.35), th, (66, 18))
        a2, sc2 = appear(t, L('L07', 0.55))
        lay = canvas(); cross(lay, 82, 12.4, 0.75); comp(im, lay, a2, sc2, (82, 12.4))
        a3, sc3 = appear(t, L('L07', 0.7))
        lay = canvas(); badge(lay, 'nggak bisa baca pikiran', 50, 41, F['coral'], F['white'], 36); comp(im, lay, a3, sc3, (50, 41))

    elif sid == 'SH08':   # works only from info given
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); ai_box(lay, 76, 23, 0.75); comp(im, lay, a, sc, (76, 23))
        labs = ['siapa kamu', 'buat apa', 'gayanya']
        a1 = appear(t, L('L08', 0.3))[0]
        if a1 > 0:
            lay = canvas()
            for i, lab in enumerate(labs):   # info chips flowing into AI: pure function of t
                ph = ((t - L('L08', 0.3)) * 0.4 + i / 3.0) % 1.0
                x = 20 + 38 * ph; y = 15 + i * 8 + (23 - (15 + i * 8)) * ph * 0.6
                fade = clamp(min(ph / 0.12, (1 - ph) / 0.2))
                chip(lay, lab, x, y, CHIPC[i], 30, a=int(255 * fade))
            comp(im, lay, a1)
        a2, sc2 = appear(t, L('L08', 0.7))
        lay = canvas(); badge(lay, 'kerja dari info yang kamu kasih', 50, 40, F['ink'], F['white'], 34); comp(im, lay, a2, sc2, (50, 40))

    elif sid == 'SH09':   # ask AI to ask back
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Trik: minta AI nanya balik', (50, 11), 44, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 11))
        def q(l): bubble(l, (12, 16.5, 92, 24.5), 'Sebelum mulai, tanya aku dulu\nkalau ada yang kurang jelas ya.', 'u', size=32)
        G(L('L09', 0.4), q, (52, 20.5))
        a2, sc2 = appear(t, L('L09', 0.75))
        lay = canvas(); badge(lay, 'boleh banget!', 50, 32, F['yellow'], F['ink'], 36); comp(im, lay, a2, sc2, (50, 32))
        note('contoh prompt (ilustrasi)', 43, L('L09', 0.45))

    elif sid == 'SH10':   # AI asks you
        def ai(l): ai_box(l, 14, 21, 0.4)
        G(s['start'] + 0.05, ai, (14, 21))
        def b(l): bubble(l, (24, 15.5, 92, 26.5), 'Caption buat produk apa?\nGayanya mau lucu\natau elegan?', 'a', size=32)
        G(L('L10', 0.2), b, (58, 21))
        for i, (x, y) in enumerate(((80, 31.5), (88, 33.5))):
            def qq(l, x=x, y=y): txt(l, '?', (x, y), 60, F['coral'])
            G(L('L10', 0.5 + 0.1 * i), qq, (x, y), dy=0.3 * math.sin(t * 3 + i))
        a2, sc2 = appear(t, L('L10', 0.7))
        lay = canvas(); badge(lay, 'AI yang nanya ke kamu', 46, 36.5, F['blue'], F['white'], 34); comp(im, lay, a2, sc2, (46, 36.5))
        note('contoh chat (ilustrasi)', 43.5, L('L10', 0.3))

    elif sid == 'SH11':   # three ingredients
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, '3 BAHAN\nPROMPT BAGUS', (50, 19), 80, F['ink'], 'Bold', spacing=4); comp(im, lay, a, sc, (50, 19))
        for i in range(3):
            a, sc = appear(t, L('L11', 0.3 + 0.18 * i))
            lay = canvas(); circ(lay, 32 + 18 * i, 35, 52, CHIPC[i]); txt(lay, str(i + 1), (32 + 18 * i, 35.2), 60, F['white'])
            comp(im, lay, a, sc, (32 + 18 * i, 35))

    elif sid in ('SH12', 'SH13', 'SH14'):
        n = int(sid[-1]) - 1; lid = ['L12', 'L13', 'L14'][n - 1]
        title = ['Konteks', 'Tugas yang jelas', 'Format'][n - 1]
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        circ(lay, 13, 11.5, 46, CHIPC[n - 1]); txt(lay, str(n), (13, 11.7), 56, F['white'])
        txt(lay, title, (20.5, 11.5), 46, F['ink'], 'Bold', 'lm')
        comp(im, lay, a, sc, (40, 11.5))
        if n == 1:
            def who(l):
                card(l, (8, 17, 49, 31), r=34)
                circ(l, 17, 22, 34, F['lilac']); txt(l, '?', (17, 22.1), 40, F['white'])
                txt(l, 'kamu siapa', (23, 22), 32, F['ink'], 'Bold', 'lm')
                txt(l, '"Aku jualan\nkopi susu."', (28.5, 27.6), 28, F['ink2'], 'Medium', spacing=4)
            G(L(lid, 0.3), who, (28.5, 24))
            def why(l):
                card(l, (51, 17, 92, 31), r=34)
                circ(l, 60, 22, 34, F['blue']); txt(l, '!', (60, 22.1), 40, F['white'])
                txt(l, 'buat apa', (66, 22), 32, F['ink'], 'Bold', 'lm')
                txt(l, '"Buat posting\nInstagram."', (71.5, 27.6), 28, F['ink2'], 'Medium', spacing=4)
            G(L(lid, 0.7), why, (71.5, 24))
            a2, sc2 = appear(t, L(lid, 0.8))
            lay = canvas(); badge(lay, 'AI jadi paham situasinya', 50, 37.5, F['mint'], F['white'], 32); comp(im, lay, a2, sc2, (50, 37.5))
            note('contoh (ilustrasi)', 43.5, L(lid, 0.35))
        elif n == 2:
            rows = [('apa', '3 caption'), ('buat siapa', 'anak kuliahan'), ('berapa panjang', 'maks 20 kata')]
            for i, (k_, v_) in enumerate(rows):
                y = 19 + i * 6.2
                def f(l, k_=k_, v_=v_, y=y, i=i):
                    card(l, (8, y - 2.5, 92, y + 2.5), r=30)
                    chip(l, k_, 8 + 2 + (tw_px(k_, 30) + 44) / W * 50, y, CHIPC[i], 30)
                    txt(l, v_, (88, y), 34, F['ink'], 'SemiBold', 'rm')
                G(L(lid, 0.3 + 0.18 * i), f, (50, y))
            note('contoh (ilustrasi)', 39.5, L(lid, 0.35))
            a2, sc2 = appear(t, L(lid, 0.85))
            lay = canvas(); badge(lay, 'makin spesifik, makin pas', 50, 44, F['ink'], F['white'], 30); comp(im, lay, a2, sc2, (50, 44))
        else:
            fm = [('poin', 0.3), ('tabel', 0.45), ('gaya santai', 0.65)]
            def icon_pts(l):
                card(l, (8, 17, 34, 32), r=30)
                for i in range(3):
                    y = 20.4 + i * 3.4
                    circ(l, 13, y, 9, F['blue']); rr(l, (16, y - 0.35, 30 - 4 * (i == 2), y + 0.35), 4, F['ink2'])
                txt(l, 'poin', (21, 34.6), 30, F['ink'], 'SemiBold')
            def icon_tab(l):
                card(l, (37, 17, 63, 32), r=30)
                for i in range(4):
                    rr(l, (40, 19.5 + i * 2.8, 60, 19.6 + i * 2.8 + 0.12), 1, F['ink2'])
                rr(l, (40, 19.5, 60, 22.3), 4, F['coral'], a=200)
                line(l, 50, 19.5, 50, 28, F['ink2'], 3)
                txt(l, 'tabel', (50, 34.6), 30, F['ink'], 'SemiBold')
            def icon_gaya(l):
                card(l, (66, 17, 92, 32), r=30)
                bubble(l, (69, 20.5, 89, 25), '', 'a', fill=F['yellow'])
                txt(l, 'hai, guys!', (79, 22.75), 26, F['ink'], 'Medium')
                txt(l, ':)', (79, 28.6), 40, F['ink'], 'Bold')
                txt(l, 'gaya santai', (79, 34.6), 30, F['ink'], 'SemiBold')
            for (lab, f_), fn, ax in zip(fm, (icon_pts, icon_tab, icon_gaya), (21, 50, 79)):
                G(L(lid, f_), fn, (ax, 25))
            a2, sc2 = appear(t, L(lid, 0.85))
            lay = canvas(); badge(lay, 'bilang mau bentuk apa', 50, 41.5, F['yellow'], F['ink'], 32); comp(im, lay, a2, sc2, (50, 41.5))

    elif sid == 'SH15':   # same prompt, different style (illustration)
        def q(l): bubble(l, (24, 9, 76, 13.8), 'Prompt yang sama', 'u', size=34)
        G(s['start'] + 0.05, q, (50, 11.4))
        styles = [('Model A', 'kalem'), ('Model B', 'ceria'), ('Model C', 'ringkas')]
        for i, (m_, st) in enumerate(styles):
            x = 22 + 28 * i
            def f(l, m_=m_, st=st, x=x, i=i):
                card(l, (x - 12.5, 18.5, x + 12.5, 33), r=30)
                circ(l, x, 22.3, 30, CHIPC[i]); txt(l, 'ABC'[i], (x, 22.4), 36, F['white'])
                txt(l, m_, (x, 27), 30, F['ink'], 'SemiBold')
                txt(l, st, (x, 30.6), 28, F['ink2'], 'Medium')
            G(L('L15', 0.4 + 0.12 * i), f, (x, 25.5))
        k = clamp((t - L('L15', 0.3)) / 0.4)
        if k > 0:
            lay = canvas()
            for i in range(3): arrow(lay, 50, 14.6, lerp(50, 22 + 28 * i, 1.0), 17.8, k, F['ink2'], 5)
            comp(im, lay)
        a2, sc2 = appear(t, L('L15', 0.75))
        lay = canvas(); badge(lay, 'beda model, beda gaya jawab', 50, 38.5, F['ink'], F['white'], 32); comp(im, lay, a2, sc2, (50, 38.5))
        note('ilustrasi — nama & gaya model contoh', 44, L('L15', 0.5))

    elif sid == 'SH16':   # Sakelar AI: many models, one door
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); wordmark(lay, 50, 10.5, 200, tsize=42); comp(im, lay, a, sc, (50, 12))
        ys = (22.5, 29.5, 36.5)
        for i, y in enumerate(ys):
            def f(l, i=i, y=y): chip(l, 'Model ' + 'ABC'[i], 22, y, CHIPC[i], 36)
            G(L('L16', 0.35 + 0.1 * i), f, (22, y))
        k = clamp((t - L('L16', 0.6)) / 0.4)
        if k > 0:
            lay = canvas()
            for y in ys: arrow(lay, 36, y, 62, lerp(y, 29.5, 0.6), k, F['ink2'], 6)
            comp(im, lay)
        G(L('L16', 0.65), door, (74, 30))
        a2, sc2 = appear(t, L('L16', 0.75))
        lay = canvas(); badge(lay, 'satu pintu', 74, 43.5, F['blue'], F['white'], 30); comp(im, lay, a2, sc2, (74, 43.5))

    elif sid == 'SH17':   # try the same prompt on several models, pick
        def q(l): bubble(l, (24, 9, 76, 13.8), 'Prompt kamu', 'u', size=34)
        G(s['start'] + 0.05, q, (50, 11.4))
        k = clamp((t - L('L17', 0.25)) / 0.4)
        if k > 0:
            lay = canvas()
            for i in range(3): arrow(lay, 50, 14.6, 22 + 28 * i, 17.8, k, F['ink2'], 5)
            comp(im, lay)
        pick = t >= L('L17', 0.75)
        for i in range(3):
            x = 22 + 28 * i
            def f(l, i=i, x=x):
                on = pick and i == 2
                card(l, (x - 12.5, 18.5, x + 12.5, 31), r=30, outline=F['mint'] if on else None)
                circ(l, x, 22.6, 30, CHIPC[i]); txt(l, 'ABC'[i], (x, 22.7), 36, F['white'])
                txt(l, 'Model ' + 'ABC'[i], (x, 27.4), 30, F['ink'], 'SemiBold')
            G(L('L17', 0.3 + 0.08 * i), f, (x, 24.5))
        if pick:
            a, sc = appear(t, L('L17', 0.75))
            lay = canvas(); check(lay, 87.5, 18.8, 0.8); badge(lay, 'paling cocok', 78, 35, F['mint'], F['white'], 30)
            comp(im, lay, a, sc, (78, 27))
        note('contoh — nama model menyesuaikan', 41.5, L('L17', 0.4), 26)

    elif sid == 'SH18':   # token package per model
        def box(l):
            rr(l, (32, 18, 68, 31), 22, F['blue']); rr(l, (29.5, 15.2, 70.5, 19.4), 18, '#3561B3')
            rr(l, (47.8, 15.2, 52.2, 19.4), 6, F['yellow'])
            circ(l, 47.3, 14.5, 16, F['yellow']); circ(l, 52.7, 14.5, 16, F['yellow'])
            txt(l, 'PAKET TOKEN', (50, 25.2), 40, F['white'])
        G(L('L18', 0.1), box, (50, 23))
        a, sc = appear(t, L('L18', 0.4))
        lay = canvas(); chip(lay, 'per model', 50, 35, F['ink'], 32); comp(im, lay, a, sc, (50, 35))
        a2, sc2 = appear(t, L('L18', 0.65))
        lay = canvas(); badge(lay, 'Model C · ??M token (contoh)', 50, 41.5, F['yellow'], F['ink'], 30); comp(im, lay, a2, sc2, (50, 41.5))

    elif sid == 'SH19':   # not longest, but clearest
        def left(l):
            card(l, (7, 10, 47, 33), r=36)
            for i in range(5):
                rr(l, (12, 13.5 + i * 2.2, 42 - 6 * (i == 4), 14.1 + i * 2.2), 4, F['gray'])
            txt(l, 'paling panjang', (27, 28.6), 34, F['ink2'], 'Bold')
            line(l, 11, 28.8, 43, 28.8, F['red'], 7)
        G(L('L19', 0.35), left, (27, 21))
        def right(l):
            card(l, (53, 10, 93, 33), r=36, outline=F['mint'])
            check(l, 73, 17.5, 1.3)
            txt(l, 'paling jelas', (73, 28.6), 38, F['ink'], 'Bold')
        G(L('L19', 0.72), right, (73, 21))
        a, sc = appear(t, L('L19', 0.85))
        lay = canvas(); badge(lay, 'konteks + tugas + format', 50, 40.5, F['ink'], F['white'], 34); comp(im, lay, a, sc, (50, 40.5))

    elif sid == 'SH20':   # punchline
        a0, sc0 = appear(t, L('L20', 0.2))
        lay = canvas(); txt(lay, 'kode-kodean', (50, 20), 44, F['ink2'], 'Bold'); line(lay, 30, 20.2, 70, 20.2, F['red'], 7)
        comp(im, lay, a0 * (1 - clamp((t - L('L20', 0.7)) / 0.3)), sc0, (50, 20))
        for i, (x, y, s_, ph) in enumerate(((22, 32, 1.6, 0), (78, 26, 2.0, 1.1), (64, 41, 1.2, 2.2), (34, 22, 1.0, 3.1), (50, 33, 2.4, 0.5))):
            t0 = L('L20', 0.72 + 0.05 * i)
            if t < t0: continue
            p = t - t0; a = min(1, p * 3)
            lay = canvas(); heart(lay, x + 0.6 * math.sin(p * 2 + ph), y - p * 1.5, s_ * (0.7 + 0.3 * ease_out_back(clamp(p / 0.4))))
            comp(im, lay, a)
        a, sc = appear(t, L('L20', 0.85))
        lay = canvas(); txt(lay, 'aku suka', (50, 11), 64, F['coral'], 'Bold'); comp(im, lay, a, sc, (50, 11))

    elif sid == 'SH21':   # end card
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        card(lay, (10, 9, 90, 42), r=44)
        wordmark(lay, 50, 14.5, 240, tsize=50)
        txt(lay, 'Satu pintu, banyak model AI', (50, 25.5), 38, F['ink'], 'SemiBold')
        rr(lay, (18, 29.5, 82, 35), 40, F['blue']); txt(lay, 'app.sakelar.web.id', (50, 32.25), 42, F['white'], 'Bold')
        txt(lay, 'Ep 10 · Prompt yang Bagus Itu Kayak Gimana?', (50, 38.7), 26, F['ink2'], 'Medium')
        comp(im, lay, a, sc, (50, 25))


# Per-shot spec: purpose, objects, anim (list of (t_rel, text)), screen text, sfx (list of (t_rel, name, len, dB, fn)), qa
def spec(sid):
    s = SH[sid]; d = round(s['end'] - s['start'], 3)
    if sid == 'SH01': return dict(
        goal='Hook: minta "Bikinin caption", hasilnya biasa banget.',
        obj=['Bubble biru user x=46–92%, y=9.5–14.8% "Bikinin caption."',
             'Bubble putih AI x=8–74%, y=17.5–24.5% "Ini caption-nya:\\n\\"Hari yang indah.\\"" + label "AI" (78%,21%).',
             'Badge coral "kok biasa banget?" (50%,33.5%) diapit "..." abu.', 'Teks "contoh chat (ilustrasi)" (50%,44%).'],
        anim=[(r(sid, 'L01', 0.25), 'Bubble user pop-in (saat "Bikinin caption").'), (r(sid, 'L01', 0.6), 'Bubble AI pop-in + catatan.'),
              (r(sid, 'L01', 0.8), 'Badge + "..." pop-in (saat "biasa banget"); "..." goyang ±0.4%.')],
        text=['"Bikinin caption." Medium 36px putih.', '"Ini caption-nya: \\"Hari yang indah.\\"" Medium 34px navy.', '"kok biasa banget?" Medium 38px putih.', '"contoh chat (ilustrasi)" Medium 24px abu.'],
        sfx=[(r(sid, 'L01', 0.25), 'pop', 0.15, -16, 'bubble user'), (r(sid, 'L01', 0.6), 'blip', 0.3, -18, 'bubble AI'), (r(sid, 'L01', 0.8), 'boing', 0.25, -16, 'biasa banget')],
        qa=['Isi chat ilustrasi — label tampil.', 'Bubble tidak keluar panel (x ≤ 92%).'])
    if sid == 'SH02': return dict(
        goal='Koreksi: jangan nyalahin AI, bisa jadi prompt-nya kurang jelas.',
        obj=['Kartu kiri x=7–43%, y=10–32%: ✕ merah (25%,16.5%) + "AI-nya\\nsalah?" abu.',
             'Kartu kanan x=47–93% outline mint: ✓ hijau (70%,16.5%) + "prompt-nya\\nkurang jelas".', 'Badge navy "bisa jadi ini penyebabnya" (50%,39.5%).'],
        anim=[(r(sid, 'L02', 0.15), 'Kartu kiri pop-in (saat "nyalahin AI").'), (r(sid, 'L02', 0.6), 'Kartu kanan pop-in (saat "prompt-nya").'), (r(sid, 'L02', 0.8), 'Badge pop-in.')],
        text=['"AI-nya\\nsalah?" Bold 44px abu.', '"prompt-nya\\nkurang jelas" Bold 40px navy.', '"bisa jadi ini penyebabnya" Medium 34px putih.'],
        sfx=[(r(sid, 'L02', 0.15), 'buzz', 0.25, -18, '✕'), (r(sid, 'L02', 0.6), 'ding', 0.4, -16, '✓')],
        qa=['Pakai "bisa jadi" — tidak menyalahkan mutlak.'])
    if sid == 'SH03': return dict(
        goal='Definisi: prompt = pesan/perintah yang kamu ketik ke AI.',
        obj=['Judul "Prompt itu apa?" (50%,11%).', 'Kolom ketik putih x=8–60%, y≈22%: teks "Bikinin caption..." diketik huruf per huruf + kursor kedip + tombol kirim biru.',
             'Badge coral "PROMPT" (22%,28.6%).', 'Panah x 62→70%, chip AI skala 0.55 (81%,22%).', 'Badge mint "= pesan / perintah yang kamu ketik" (50%,37.5%).'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L03', 0.15), 'Kolom ketik pop-in; huruf muncul selama 1.0 s; kursor kedip 2 Hz.'), (r(sid, 'L03', 0.35), 'Badge PROMPT.'),
              (r(sid, 'L03', 0.6), 'Panah tumbuh 0.35 s.'), (r(sid, 'L03', 0.75), 'Chip AI pop-in.'), (r(sid, 'L03', 0.8), 'Badge definisi.')],
        text=['"Prompt itu apa?" Bold 48px.', '"Bikinin caption..." Medium 34px.', '"PROMPT" Medium 30px putih.', '"= pesan / perintah yang kamu ketik" Medium 32px putih.'],
        sfx=[(r(sid, 'L03', 0.15), 'clicks', 0.9, -18, 'mengetik'), (r(sid, 'L03', 0.6), 'whoosh', 0.3, -18, 'kirim'), (r(sid, 'L03', 0.8), 'ding', 0.4, -16, 'definisi')],
        qa=['Pose desk: monitor tidak menutupi subtitle.'])
    if sid == 'SH04': return dict(
        goal='Analogi: kayak pesan makanan ke abang nasi goreng.',
        obj=['Judul "Ibarat pesan nasi goreng" (50%,11%).', 'Kartu x=14–86%, y=16–38%: papan coral "NASI GORENG" + piring nasi goreng (50%,31.2%).',
             'Uap abu naik dari piring.', 'Badge navy "pesanan = prompt" (50%,43%).'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L04', 0.45), 'Kartu + piring pop-in (saat "pesan makanan").'),
              (r(sid, 'L04', 0.6), 'Uap: ph = (0.6u + i/3) mod 1, naik 4%, membesar, fade.'), (r(sid, 'L04', 0.8), 'Badge pop-in.')],
        text=['"Ibarat pesan nasi goreng" Bold 46px.', '"NASI GORENG" Bold 40px putih.', '"pesanan = prompt" Medium 32px putih.'],
        sfx=[(r(sid, 'L04', 0.45), 'pop', 0.15, -16, 'kartu'), (r(sid, 'L04', 0.6), 'hum', 0.8, -24, 'uap'), (r(sid, 'L04', 0.8), 'pop_hi', 0.15, -16, 'badge')],
        qa=['Badge di y 43% tidak menyentuh subtitle.'])
    if sid == 'SH05': return dict(
        goal='Pesan singkat "nasi goreng satu" → dapat yang standar.',
        obj=['Bubble biru user x=30–92%, y=9.5–14.8% "\\"Nasi goreng satu.\\""', 'Kartu x=22–78%, y=18–35% + piring polos (50%,27.6%).', 'Badge abu "standar" (50%,40.5%).'],
        anim=[(r(sid, 'L05', 0.2), 'Bubble pop-in.'), (r(sid, 'L05', 0.65), 'Piring pop-in (saat "dapat").'), (r(sid, 'L05', 0.82), 'Badge (saat "standar").')],
        text=['"\\"Nasi goreng satu.\\"" Medium 36px putih.', '"standar" Medium 36px putih.'],
        sfx=[(r(sid, 'L05', 0.2), 'pop', 0.15, -16, 'bubble'), (r(sid, 'L05', 0.65), 'clunk', 0.3, -18, 'piring'), (r(sid, 'L05', 0.82), 'pop', 0.15, -16, 'standar')],
        qa=['Piring polos tanpa telur/cabai.'])
    if sid == 'SH06': return dict(
        goal='Pesan detail → hasil pas sama selera.',
        obj=['Bubble biru user x=8–92%, y=9.5–14.8% "\\"Pedas, telur dadar, tanpa acar.\\""',
             'Chip di x=21%: "pedas" merah (y 20.5%), "telur dadar" kuning (26.1%), "tanpa acar" mint (31.7%).',
             'Kartu x=40–92%, y=17.5–35% outline mint + piring dengan telur dadar & cabai (66%,27.4%).', '✓ (88%,18.8%) + badge mint "pas sama selera kamu" (50%,40.5%).'],
        anim=[(r(sid, 'L06', 0.12), 'Bubble pop-in.'), (r(sid, 'L06', 0.2), 'Chip pop-in bergiliran +12%.'), (r(sid, 'L06', 0.62), 'Piring spesial pop-in.'),
              (r(sid, 'L06', 0.8), '✓ + badge pop-in (saat "pas sama selera").')],
        text=['Isi bubble Medium 36px putih (verbatim).', 'Chip Medium 32px.', '"pas sama selera kamu" Medium 34px putih.'],
        sfx=[(r(sid, 'L06', 0.2), 'pop', 0.15, -18, 'pedas'), (r(sid, 'L06', 0.32), 'pop', 0.15, -18, 'telur'), (r(sid, 'L06', 0.44), 'pop_hi', 0.15, -18, 'acar'),
             (r(sid, 'L06', 0.8), 'chime', 0.6, -16, 'pas')],
        qa=['Chip tidak menabrak kartu piring (chip x ≤ 38%).'])
    if sid == 'SH07': return dict(
        goal='AI nggak bisa baca pikiran kamu.',
        obj=['Chip AI skala 0.75 (36%,27%).', 'Awan pikiran putih (70%,16.5%) berisi "???" + 2 titik kecil.', '✕ merah kecil (82%,12.4%).', 'Badge coral "nggak bisa baca pikiran" (50%,41%).'],
        anim=[(0.1, 'Chip AI pop-in.'), (r(sid, 'L07', 0.35), 'Awan pikiran pop-in.'), (r(sid, 'L07', 0.55), '✕ pop-in (saat "nggak bisa").'), (r(sid, 'L07', 0.7), 'Badge.')],
        text=['"???" Bold 60px.', '"nggak bisa baca pikiran" Medium 36px putih.'],
        sfx=[(r(sid, 'L07', 0.35), 'blip', 0.3, -18, 'awan'), (r(sid, 'L07', 0.55), 'buzz', 0.25, -18, '✕')],
        qa=['Tanpa mata/wajah tambahan pada chip AI.'])
    if sid == 'SH08': return dict(
        goal='AI cuma bisa kerja dari informasi yang kamu kasih.',
        obj=['Chip AI skala 0.75 (76%,23%).', 'Chip info "siapa kamu" / "buat apa" / "gayanya" mengalir dari x≈20% ke AI.', 'Badge navy "kerja dari info yang kamu kasih" (50%,40%).'],
        anim=[(0.05, 'Chip AI pop-in.'), (r(sid, 'L08', 0.3), 'Chip info mengalir: ph = (0.4u + i/3) mod 1, x = 20 + 38ph, fade masuk/keluar.'), (r(sid, 'L08', 0.7), 'Badge pop-in.')],
        text=['Chip Medium 30px.', '"kerja dari info yang kamu kasih" Medium 34px putih.'],
        sfx=[(r(sid, 'L08', 0.3), 'swipe', 0.8, -20, 'info mengalir'), (r(sid, 'L08', 0.7), 'pop', 0.15, -16, 'badge')],
        qa=['Chip berhenti sebelum menabrak AI (x ≤ 58%).'])
    if sid == 'SH09': return dict(
        goal='Fakta unik: kamu bisa minta AI nanya balik dulu.',
        obj=['Judul "Trik: minta AI nanya balik" (50%,11%).', 'Bubble biru user x=12–92%, y=16.5–24.5% "Sebelum mulai, tanya aku dulu\\nkalau ada yang kurang jelas ya."',
             'Badge kuning "boleh banget!" (50%,32%).', '"contoh prompt (ilustrasi)" (50%,43%).'],
        anim=[(0.05, 'Judul pop-in ("Uniknya").'), (r(sid, 'L09', 0.4), 'Bubble pop-in.'), (r(sid, 'L09', 0.45), 'Catatan.'), (r(sid, 'L09', 0.75), 'Badge.')],
        text=['Judul Bold 44px.', 'Isi bubble Medium 32px (verbatim).', '"boleh banget!" Medium 36px navy.'],
        sfx=[(0.05, 'ding', 0.4, -16, '"Uniknya"'), (r(sid, 'L09', 0.4), 'pop', 0.15, -16, 'bubble'), (r(sid, 'L09', 0.75), 'sparkle', 0.6, -18, 'boleh banget')],
        qa=['Teks bubble 2 baris tidak keluar bubble.'])
    if sid == 'SH10': return dict(
        goal='Jadi AI yang nanya balik kalau ada yang kurang jelas.',
        obj=['Chip AI skala 0.4 (14%,21%).', 'Bubble putih AI x=24–92%, y=15.5–26.5% "Caption buat produk apa?\\nGayanya mau lucu\\natau elegan?"',
             'Dua "?" coral (80,31.5) & (88,33.5).', 'Badge biru "AI yang nanya ke kamu" (46%,36.5%).', '"contoh chat (ilustrasi)" (50%,43.5%).'],
        anim=[(0.05, 'Chip AI pop-in.'), (r(sid, 'L10', 0.2), 'Bubble pop-in.'), (r(sid, 'L10', 0.3), 'Catatan.'), (r(sid, 'L10', 0.5), '"?" pop-in +10%.'), (r(sid, 'L10', 0.7), 'Badge.')],
        text=['Isi bubble Medium 32px navy (verbatim).', '"AI yang nanya ke kamu" Medium 34px putih.'],
        sfx=[(r(sid, 'L10', 0.2), 'blip', 0.3, -18, 'bubble AI'), (r(sid, 'L10', 0.5), 'boing', 0.25, -18, '?')],
        qa=['Isi chat ilustrasi — label tampil.'])
    if sid == 'SH11': return dict(
        goal='Transisi ke tips: tiga bahan prompt yang bagus.',
        obj=['Judul 2 baris "3 BAHAN / PROMPT BAGUS" Bold 80px navy (50%,19%).', 'Tiga lingkaran r=52px di (32,35), (50,35), (68,35): biru, coral, kuning.'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L11', 0.3), 'Lingkaran 1 pop-in, 2 & 3 tiap +18%.')],
        text=['"3 BAHAN\\nPROMPT BAGUS"', '"1", "2", "3"'],
        sfx=[(r(sid, 'L11', 0.3), 'pop_hi', 0.6, -14, 'angka')], qa=['Judul tidak terpotong (lebar < 92%).'])
    if sid in ('SH12', 'SH13', 'SH14'):
        n = int(sid[-1]) - 1; lid = ['L12', 'L13', 'L14'][n - 1]
        head = f'Header: lingkaran nomor "{n}" r=46px di (13%,11.5%) + judul Bold 46px di x=20.5% left.'
        base = dict(goal=['Bahan 1: konteks — kamu siapa & hasilnya buat apa.', 'Bahan 2: tugas jelas — apa, buat siapa, berapa panjang.', 'Bahan 3: format — poin, tabel, gaya bahasa.'][n - 1])
        if n == 1: base.update(
            obj=[head, 'Kartu kiri x=8–49%, y=17–31%: ikon "?" lilac + "kamu siapa" + "\\"Aku jualan\\nkopi susu.\\""',
                 'Kartu kanan x=51–92%: ikon "!" biru + "buat apa" + "\\"Buat posting\\nInstagram.\\""', 'Badge mint "AI jadi paham situasinya" (50%,37.5%).', '"contoh (ilustrasi)" (50%,43.5%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.3), 'Kartu kiri pop-in (saat "kamu siapa").'), (r(sid, lid, 0.35), 'Catatan.'),
                  (r(sid, lid, 0.7), 'Kartu kanan pop-in (saat "buat apa").'), (r(sid, lid, 0.8), 'Badge.')],
            text=['"Konteks"', '"kamu siapa" / "buat apa" Bold 32px.', 'Contoh Medium 28px abu (verbatim).', 'Badge Medium 32px.'],
            sfx=[(r(sid, lid, 0.3), 'pop', 0.15, -16, 'kartu 1'), (r(sid, lid, 0.7), 'pop_hi', 0.15, -16, 'kartu 2'), (r(sid, lid, 0.8), 'ding', 0.4, -16, 'badge')])
        if n == 2: base.update(
            obj=[head, 'Tiga baris kartu x=8–92% di y=19/25.2/31.4%: chip "apa"/"buat siapa"/"berapa panjang" kiri + nilai kanan "3 caption"/"anak kuliahan"/"maks 20 kata".',
                 '"contoh (ilustrasi)" (50%,39.5%).', 'Badge navy "makin spesifik, makin pas" (50%,44%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.3), 'Baris 1 pop-in, 2 & 3 tiap +18% (ikut kata).'), (r(sid, lid, 0.35), 'Catatan.'), (r(sid, lid, 0.85), 'Badge.')],
            text=['"Tugas yang jelas"', 'Chip Medium 30px; nilai SemiBold 34px.', 'Badge Medium 30px.'],
            sfx=[(r(sid, lid, 0.3), 'tick', 0.2, -16, 'baris 1'), (r(sid, lid, 0.48), 'tick', 0.2, -16, 'baris 2'), (r(sid, lid, 0.66), 'tick', 0.2, -16, 'baris 3'), (r(sid, lid, 0.85), 'pop', 0.15, -16, 'badge')])
        if n == 3: base.update(
            obj=[head, 'Tiga kartu ikon y=17–32%: "poin" (x 8–34%, 3 bullet), "tabel" (37–63%, grid header coral), "gaya santai" (66–92%, bubble kuning "hai, guys!" + ":)").',
                 'Label di y=34.6%.', 'Badge kuning "bilang mau bentuk apa" (50%,41.5%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.3), 'Kartu poin (saat "poin").'), (r(sid, lid, 0.45), 'Kartu tabel.'), (r(sid, lid, 0.65), 'Kartu gaya santai.'), (r(sid, lid, 0.85), 'Badge.')],
            text=['"Format"', '"poin" / "tabel" / "gaya santai" SemiBold 30px.', '"hai, guys!" Medium 26px.', 'Badge Medium 32px navy.'],
            sfx=[(r(sid, lid, 0.3), 'pop', 0.15, -16, 'poin'), (r(sid, lid, 0.45), 'pop', 0.15, -16, 'tabel'), (r(sid, lid, 0.65), 'pop_hi', 0.15, -16, 'gaya'), (r(sid, lid, 0.85), 'ding', 0.4, -16, 'badge')])
        base['qa'] = ['Nomor bahan sama dengan urutan dialog.', 'Contoh teks ditulis persis.']
        return base
    if sid == 'SH15': return dict(
        goal='Jembatan ke soft sell: prompt sama bisa dijawab beda gaya oleh model berbeda.',
        obj=['Bubble biru "Prompt yang sama" x=24–76%, y=9–13.8%.', 'Tiga panah dari (50%,14.6%) ke tiap kartu.',
             'Tiga kartu lebar 25% di x=22/50/78%, y=18.5–33%: lingkaran huruf + "Model A/B/C" + gaya "kalem/ceria/ringkas".',
             'Badge navy "beda model, beda gaya jawab" (50%,38.5%).', '"ilustrasi — nama & gaya model contoh" (50%,44%).'],
        anim=[(0.05, 'Bubble pop-in.'), (r(sid, 'L15', 0.3), 'Panah tumbuh 0.4 s.'), (r(sid, 'L15', 0.4), 'Kartu pop-in tiap +12%.'), (r(sid, 'L15', 0.5), 'Catatan.'), (r(sid, 'L15', 0.75), 'Badge.')],
        text=['"Prompt yang sama" Medium 34px.', '"Model A/B/C" SemiBold 30px — PLACEHOLDER.', '"kalem/ceria/ringkas" — ILUSTRASI.', 'Badge Medium 32px.'],
        sfx=[(r(sid, 'L15', 0.3), 'whoosh', 0.4, -18, 'panah'), (r(sid, 'L15', 0.4), 'pop', 0.5, -18, 'kartu'), (r(sid, 'L15', 0.75), 'ding', 0.4, -16, 'badge')],
        qa=['Gaya model ilustrasi — label tampil.', 'Tidak menyebut nama model asli.'])
    if sid == 'SH16': return dict(
        goal='Soft sell: di Sakelar AI banyak model lewat satu pintu.',
        obj=['Logo Sakelar (gelap) 200px + "Sakelar AI" Bold 42px di (50%,10.5%).',
             'Chip "Model A" biru / "Model B" coral / "Model C" kuning di x=22%, y=22.5/29.5/36.5%.',
             'Tiga panah x 36→62% menyatu ke pintu.', 'Pintu: kusen navy x=64–84%, y=20–40%; daun biru; gagang kuning.', 'Badge biru "satu pintu" (74%,43.5%).'],
        anim=[(0.05, 'Logo pop-in.'), (r(sid, 'L16', 0.35), 'Chip model pop-in tiap +10%.'), (r(sid, 'L16', 0.6), 'Panah tumbuh 0.4 s.'),
              (r(sid, 'L16', 0.65), 'Pintu pop-in.'), (r(sid, 'L16', 0.75), 'Badge "satu pintu".')],
        text=['"Sakelar AI"', '"Model A/B/C" Medium 36px (placeholder).', '"satu pintu" Medium 30px putih.'],
        sfx=[(0.05, 'jingle', 0.6, -14, 'logo'), (r(sid, 'L16', 0.35), 'pop', 0.4, -18, 'chip'), (r(sid, 'L16', 0.65), 'chime', 0.6, -14, 'satu pintu')],
        qa=['Logo file asli Sakelar, tidak diubah bentuk.', 'Tidak menyebut nama model asli.'])
    if sid == 'SH17': return dict(
        goal='Coba prompt yang sama ke beberapa model, pilih yang paling cocok.',
        obj=['Bubble biru "Prompt kamu" x=24–76%, y=9–13.8%.', 'Tiga panah ke tiga kartu model lebar 25% di x=22/50/78%, y=18.5–31%.',
             'Saat dipilih: kartu C outline mint, ✓ (87.5%,18.8%), badge mint "paling cocok" (78%,35%).', 'Catatan "contoh — nama model menyesuaikan" (50%,41.5%).'],
        anim=[(0.05, 'Bubble pop-in.'), (r(sid, 'L17', 0.25), 'Panah tumbuh 0.4 s.'), (r(sid, 'L17', 0.3), 'Kartu pop-in tiap +8%.'), (r(sid, 'L17', 0.4), 'Catatan.'),
              (r(sid, 'L17', 0.75), 'Kartu C terpilih + ✓ + badge (saat "pilih").')],
        text=['"Prompt kamu" Medium 34px.', '"Model A/B/C" SemiBold 30px — PLACEHOLDER.', '"paling cocok" Medium 30px.', 'Catatan Medium 26px abu.'],
        sfx=[(r(sid, 'L17', 0.25), 'whoosh', 0.4, -18, 'kirim'), (r(sid, 'L17', 0.3), 'pop', 0.4, -18, 'kartu'), (r(sid, 'L17', 0.75), 'ding', 0.4, -16, 'terpilih')],
        qa=['Nama model placeholder.', 'Tidak mengklaim fitur "bandingkan" khusus.'])
    if sid == 'SH18': return dict(
        goal='Token dijual dalam paket per model.',
        obj=['Kotak "PAKET TOKEN" biru x=32–68%, y=18–31%, tutup x=29.5–70.5%, pita + simpul kuning.',
             'Chip navy "per model" (50%,35%).', 'Badge kuning "Model C · ??M token (contoh)" (50%,41.5%).'],
        anim=[(r(sid, 'L18', 0.1), 'Kotak paket pop-in.'), (r(sid, 'L18', 0.4), 'Chip "per model".'), (r(sid, 'L18', 0.65), 'Badge isi paket.')],
        text=['"PAKET TOKEN" Bold 40px putih.', '"per model" Medium 32px.', '"Model C · ??M token (contoh)" Medium 30px — PLACEHOLDER.'],
        sfx=[(r(sid, 'L18', 0.1), 'coins', 0.8, -18, 'paket'), (r(sid, 'L18', 0.65), 'kaching', 0.5, -18, 'isi paket')],
        qa=['Isi paket placeholder "??M (contoh)".'])
    if sid == 'SH19': return dict(
        goal='Rangkuman: prompt bagus bukan yang paling panjang, tapi yang paling jelas.',
        obj=['Kartu kiri x=7–47%, y=10–33%: 5 garis teks abu + "paling panjang" dicoret merah.',
             'Kartu kanan x=53–93% outline mint: ✓ besar (73%,17.5%) + "paling jelas".', 'Badge navy "konteks + tugas + format" (50%,40.5%).'],
        anim=[(r(sid, 'L19', 0.35), 'Kartu kiri pop-in (saat "paling panjang").'), (r(sid, 'L19', 0.72), 'Kartu kanan pop-in (saat "paling jelas").'), (r(sid, 'L19', 0.85), 'Badge.')],
        text=['"paling panjang" Bold 34px abu + coret.', '"paling jelas" Bold 38px.', '"konteks + tugas + format" Medium 34px putih.'],
        sfx=[(r(sid, 'L19', 0.35), 'scratch', 0.3, -18, 'coret'), (r(sid, 'L19', 0.72), 'ding', 0.4, -16, 'jelas')],
        qa=['Coretan tepat di kata.'])
    if sid == 'SH20': return dict(
        goal='Punchline manis: Reina nggak pakai kode-kodean — langsung jelas "aku suka".',
        obj=['Kata "kode-kodean" abu Bold 44px dicoret merah (50%,20%), lalu memudar.', '5 hati coral naik di (22,32), (78,26), (64,41), (34,22), (50,33).', 'Teks "aku suka" Bold 64px coral (50%,11%).'],
        anim=[(r(sid, 'L20', 0.2), '"kode-kodean" + coret pop-in.'), (r(sid, 'L20', 0.7), '"kode-kodean" fade out 0.3 s.'),
              (r(sid, 'L20', 0.72), 'Hati muncul tiap +5%; naik 1.5%/s, goyang ±0.6%.'), (r(sid, 'L20', 0.85), '"aku suka" pop-in.')],
        text=['"kode-kodean" Bold 44px abu.', '"aku suka" Bold 64px coral.'],
        sfx=[(r(sid, 'L20', 0.2), 'scratch', 0.3, -18, 'coret'), (r(sid, 'L20', 0.72), 'sparkle', 1.0, -18, 'hati'), (r(sid, 'L20', 0.85), 'pop_hi', 0.2, -16, 'aku suka')],
        qa=['Mulut memakai sprite smile.', 'Hati di y ≤ 47%, tidak menutupi wajah.'])
    if sid == 'SH21': return dict(
        goal='End card: ajakan mencoba Sakelar AI.',
        obj=['Kartu putih x=10–90%, y=9–42%, radius 44px.', 'Logo 240px + "Sakelar AI" Bold 50px (pusat 50%,14.5%).',
             '"Satu pintu, banyak model AI" (50%,25.5%).', 'Tombol biru x=18–82%, y=29.5–35% "app.sakelar.web.id".', '"Ep 10 · Prompt yang Bagus Itu Kayak Gimana?" (50%,38.7%).'],
        anim=[(0.05, 'Kartu pop-in 0.35 s.'), (round(d - 0.5, 3), 'Seluruh frame fade ke #F6F1E7 dalam 0.5 s.')],
        text=['"Sakelar AI"', '"Satu pintu, banyak model AI" Medium 38px.', '"app.sakelar.web.id" Bold 42px putih.', '"Ep 10 · Prompt yang Bagus Itu Kayak Gimana?" Medium 26px abu.'],
        sfx=[(0.05, 'stinger', 1.2, -12, 'end card'), (0.1, 'jingle', 0.6, -16, 'logo')], qa=['URL tertulis persis "app.sakelar.web.id".', 'Video berakhir di frame latar polos.'])
