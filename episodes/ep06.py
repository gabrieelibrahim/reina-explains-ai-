"""Reina Explains AI — Episode 06: "Token Itu Apa Sih?" (contoh episode lengkap / template).
Satu file = satu episode: naskah, shot, pose, visual panel(t), spec storyboard + SFX, arahan VO.
Jalankan:  python run.py stage1 episodes/ep06.py   lalu   python run.py stage2 episodes/ep06.py <zip_suara>"""
import math
from PIL import Image, ImageDraw
from reina import *

EP = 6
TITLE = 'Token Itu Apa Sih?'
SCENES = {1: 'Hook', 2: 'Apa itu token', 3: 'Kenapa dihitung', 4: 'Fakta unik bahasa', 5: 'Tips hemat',
          6: 'Soft sell Sakelar AI', 7: 'Closing', 8: 'End card'}
META = dict(
    tujuan='Menjelaskan token & kenapa AI dihitung per token; soft sell paket token Sakelar AI',
    konsep=('Hook pakai label harga "per sejuta token" yang sering bikin bingung → analogi koin arcade → penjelasan token sebagai '
            'potongan teks → kenapa dihitung (komputasi, input vs output) → fakta unik bahasa Indonesia → 3 tips hemat → '
            'soft sell paket token Sakelar AI (setelah edukasi selesai) → punchline manis.'),
    fakta=['Topik: token dan kenapa AI dihitung per token.', 'Di Sakelar AI, model dijual dalam paket berisi sekian juta token ("M").',
           'CTA URL: app.sakelar.web.id.'],
    asumsi=['Pemotongan token di layar (SH04, SH06, SH10) adalah ilustrasi; tokenizer asli tiap model berbeda — label "ilustrasi" selalu tampil.',
            'Kalimat "bahasa Indonesia bisa butuh lebih banyak token" memakai kata "bisa" (tidak mutlak).'],
    konfirmasi=['Nama model & isi paket asli (SH16 masih "Model A/B/C — 5M/10M/20M token", angka contoh).',
                'Apakah harga boleh ditampilkan? SH01 sekarang "Rp ???".'],
    softsell='SH15–SH18 + end card',
)
PRON = [('AI', 'ei-ai'), ('token', 'to-ken'), ('prompt', 'prom'), ('arcade', 'ar-keid'), ('M (juta token)', 'em'), ('Sakelar', 'sa-ke-lar')]
VO_DIR = {'L01': 'santai, nada tanya naik di "token"', 'L02': 'bingung lucu, "koin arcade?" sedikit dilebih-lebihkan',
 'L03': 'yakin, pendek, senyum kecil', 'L04': 'menjelaskan, tekan "keping-keping kecil" dan "token"', 'L05': 'ritmis, tiga bagian dipisah jelas',
 'L06': 'jelas, kutip "makan" dan "memakan-makanan" dengan pelan', 'L07': 'serius tapi ringan, tekan "makin banyak" dan "makin besar"',
 'L08': 'jelas, beri jeda kecil di "alias pertanyaan" dan "alias jawaban"', 'L09': 'menekankan "lebih mahal"',
 'L10': 'nada "fakta seru", semangat di "Dan nih"', 'L11': 'agak bercanda di "mahal"', 'L12': 'energik, seperti membuka daftar',
 'L13': 'tegas, "nggak usah basa-basi" santai', 'L14': 'ringan', 'L15': 'tegas tapi ramah', 'L16': 'ramah, nada "nah" naik',
 'L17': 'menjelaskan, "M" dieja "em"', 'L18': 'santai, "pakai sampai habis" lega', 'L19': 'tanya-jawab sendiri, nada naik di tiap "?"',
 'L20': 'mantap, menutup', 'L21': 'menyimpulkan, gantung di "kebutuhan..."', 'L22': 'malu-malu manis, pelan, senyum di "aku rela kok"'}

# ---- naskah terkunci (1 item = 1 baris VO = L01, L02, ...) ----
LINES = [
 'Pernah lihat harga AI ditulis "per sejuta token"?',
 'Terus bingung, token itu apa? Kayak koin arcade?',
 'Bukan, tapi mirip.',
 'AI nggak baca kalimat utuh. Dia memotongnya jadi keping-keping kecil, namanya token.',
 'Satu token bisa satu kata, setengah kata, atau cuma satu tanda baca.',
 'Contohnya "makan" mungkin satu token, tapi "memakan-makanan" bisa pecah jadi beberapa.',
 'Setiap token yang AI baca dan tulis butuh tenaga komputasi. Jadi makin banyak token, makin besar biayanya.',
 'Yang dihitung ada dua: token yang kamu kirim, alias pertanyaan, dan token yang AI tulis, alias jawaban.',
 'Biasanya, harga jawaban lebih mahal.',
 'Dan nih, bahasa Indonesia bisa butuh lebih banyak token dibanding bahasa Inggris, untuk arti yang sama.',
 'Jadi kalimat yang sama, bisa lebih "mahal".',
 'Tiga cara hemat.',
 'Satu, tulis prompt yang padat, nggak usah basa-basi.',
 'Dua, minta jawaban singkat kalau memang cukup.',
 'Tiga, jangan kirim ulang seluruh obrolan kalau nggak perlu.',
 'Nah, di Sakelar AI, token itu dijual dalam bentuk paket.',
 'Tiap model punya paket sendiri, dan kamu dapat sekian juta token, atau "M" kalau di daftar harganya.',
 'Jadi nggak perlu hitung-hitungan ribet. Tinggal pilih model, pilih paket, lalu pakai sampai habis.',
 'Tugas ringan? Pakai model yang hemat. Tugas berat? Baru pakai model yang lebih jago.',
 'Semuanya lewat satu pintu.',
 'Jadi token itu kayak koin. Pakai sesuai kebutuhan...',
 '...eh, tapi ngobrol sama kamu semua, aku rela kok.',
]

# (id, scene, judul, [nomor baris], jeda_awal_s, jeda_akhir_s)
SHOTS = [
 ('SH01', 1, 'Label harga per sejuta token', [1], 0.5, 0.2),
 ('SH02', 1, 'Koin arcade?', [2], 0.15, 0.2),
 ('SH03', 1, 'Bukan, tapi mirip', [3], 0.15, 0.3),
 ('SH04', 2, 'Kalimat dipotong jadi token', [4], 0.2, 0.3),
 ('SH05', 2, 'Kata, setengah kata, tanda baca', [5], 0.15, 0.2),
 ('SH06', 2, 'makan vs memakan-makanan', [6], 0.15, 0.4),
 ('SH07', 3, 'Token = tenaga komputasi', [7], 0.25, 0.2),
 ('SH08', 3, 'Input dan output', [8], 0.15, 0.2),
 ('SH09', 3, 'Output lebih mahal', [9], 0.15, 0.4),
 ('SH10', 4, 'Indonesia vs Inggris', [10, 11], 0.25, 0.4),
 ('SH11', 5, 'Tiga cara hemat', [12], 0.25, 0.15),
 ('SH12', 5, 'Tips 1: prompt padat', [13], 0.1, 0.2),
 ('SH13', 5, 'Tips 2: jawaban singkat', [14], 0.1, 0.2),
 ('SH14', 5, 'Tips 3: jangan kirim ulang', [15], 0.1, 0.4),
 ('SH15', 6, 'Paket token Sakelar AI', [16], 0.25, 0.2),
 ('SH16', 6, 'Paket per model, juta token', [17], 0.1, 0.2),
 ('SH17', 6, 'Pilih model, pilih paket', [18], 0.1, 0.2),
 ('SH18', 6, 'Ringan vs berat, satu pintu', [19, 20], 0.1, 0.4),
 ('SH19', 7, 'Token itu kayak koin', [21], 0.25, 0.25),
 ('SH20', 7, 'Aku rela kok', [22], 0.1, 0.6),
 ('SH21', 8, 'End card', [], 0.0, 2.5),
]

POSE = {'SH01': 'phone', 'SH02': 'think', 'SH03': 'point_up', 'SH04': 'point', 'SH05': 'point_up', 'SH06': 'hands_on_hips',
        'SH07': 'desk', 'SH08': 'arms34', 'SH09': 'point_up', 'SH10': 'point', 'SH11': 'hands_on_hips',
        'SH12': 'point_up', 'SH13': 'thumbs_up', 'SH14': 'arms34', 'SH15': 'wave', 'SH16': 'phone', 'SH17': 'point_up',
        'SH18': 'thumbs_up', 'SH19': 'hands_on_hips', 'SH20': 'shy_lean', 'SH21': 'wave'}
SMILE = {'SH20'}   # shot yang pakai mulut senyum
EXPR = {'SH01': 'penasaran, alis sedikit naik', 'SH02': 'bingung, tangan di dagu', 'SH03': 'yakin, menjelaskan',
        'SH04': 'serius, menunjuk penonton', 'SH05': 'menjelaskan', 'SH06': 'santai, percaya diri',
        'SH07': 'fokus ke monitor', 'SH08': 'datar, analitis', 'SH09': 'menekankan', 'SH10': 'semangat, "dan nih"',
        'SH11': 'percaya diri', 'SH12': 'menjelaskan', 'SH13': 'ceria', 'SH14': 'tegas', 'SH15': 'ramah, menyapa',
        'SH16': 'menjelaskan sambil lihat HP', 'SH17': 'menjelaskan', 'SH18': 'ceria, meyakinkan',
        'SH19': 'santai, menutup', 'SH20': 'malu-malu, senyum (mulut smile)', 'SH21': 'ceria, melambai'}


def panel(t, sid, im):
    """Gambar panel visual (area y 7–47%) shot sid pada waktu t ke layer 2x im."""
    s = SH[sid]; u = t - s['start']; L = lambda lid, f=0.0: rel(lid, f)
    def G(t0, fn, anchor=(50, 25), d=0.35, dy=0.0):
        a, sc = appear(t, t0, d)
        if a <= 0: return
        lay = canvas(); fn(lay); comp(im, lay, a, sc, anchor, dy)

    if sid == 'SH01':   # price label "per sejuta token"
        def f(l):
            card(l, (12, 11, 88, 34), r=40)
            rr(l, (12, 11, 88, 16.5), 40, F['ink']); rr(l, (12, 14, 88, 16.5), 0, F['ink'])
            txt(l, 'Daftar Harga Model AI', (50, 13.7), 38, F['white'], 'SemiBold')
            for i, y in enumerate((20.2, 26.4)):
                rr(l, (16, y - 2.2, 84, y + 2.2), 22, F['bg'])
                hk = ease_out_cubic(clamp((t - L('L01', 0.55)) / 0.3))
                if hk > 0: rr(l, (68.3, y - 1.4, 68.3 + 13.5 * hk, y + 1.4), 14, F['yellow'], a=200)
                txt(l, f'Model {"AB"[i]}', (19, y), 36, F['ink'], 'SemiBold', 'lm')
                txt(l, 'Rp ???', (60, y), 38, F['ink'], 'Bold', 'rm')
                txt(l, '/ 1 juta token', (61, y), 30, F['ink2'], 'Medium', 'lm')
            txt(l, '(contoh tampilan)', (50, 31.6), 26, F['ink2'], 'Medium')
        G(0.15, f, (50, 22))
        if t >= L('L01', 0.55):   # highlight "token"
            a, sc = appear(t, L('L01', 0.75))
            lay = canvas(); circ(lay, 85, 10, 46, F['coral']); txt(lay, '?', (85, 10), 60, F['white']); comp(im, lay, a, sc, (85, 10))

    elif sid == 'SH02':   # arcade coin?
        def f(l):
            card(l, (22, 9, 78, 44), F['ink'], r=44)
            rr(l, (27, 12, 73, 22), 26, '#2C3A63')
            txt(l, 'INSERT COIN', (50, 17), 54, F['yellow'], 'Bold')
            rr(l, (44, 24, 56, 35), 16, '#2C3A63')
            for i, c in enumerate((F['coral'], F['mint'], F['blue'])): circ(l, 37 + i * 13, 39.5, 30, c)
        G(0.1, f, (50, 26))
        if t >= L('L02', 0.45):
            k = t - L('L02', 0.45)
            lay = canvas(); coin(lay, 50, lerp(31, 29.5, ease_out_cubic(clamp(k / 0.4))), 95, squash=math.cos(k * 6.0), size=30)
            comp(im, lay, min(1, k * 4))
        for i, (x, y, ph) in enumerate(((20, 12, 0), (81, 15, 1.4), (76, 40, 2.6))):
            a, sc = appear(t, L('L02', 0.1 + 0.12 * i))
            lay = canvas(); txt(lay, '?', (x, y + 0.6 * math.sin(t * 3 + ph)), 90, F['coral']); comp(im, lay, a, sc, (x, y))

    elif sid == 'SH03':   # coin -> token chip: "Bukan, tapi mirip"
        k = clamp((u - 0.25) / 0.6)
        lay = canvas(); coin(lay, 34, 26, 120, squash=max(0.05, 1 - ease_inout_cubic(k) * 0.3)); comp(im, lay, 1)
        a, sc = appear(t, s['start'] + 0.15)
        lay = canvas(); txt(lay, '≈', (50, 26), 120, F['ink2']); comp(im, lay, a, sc, (50, 26))
        a, sc = appear(t, L('L03', 0.5))
        lay = canvas(); chip(lay, 'token', 69, 26, F['blue'], 64); comp(im, lay, a, sc, (69, 26))
        a, sc = appear(t, L('L03', 0.3))
        lay = canvas(); badge(lay, 'mirip, bukan sama', 50, 38, F['coral'], F['white'], 32); comp(im, lay, a, sc, (50, 38))

    elif sid == 'SH04':   # sentence gets cut into tokens
        pieces = ['Aku', ' suka', ' makan', ' bak', 'so', '.']
        a, sc = appear(t, s['start'] + 0.1)
        lay = canvas(); txt(lay, 'AI nggak baca kalimat utuh', (50, 11.5), 42, F['ink'], 'Bold'); comp(im, lay, a, sc, (50, 11.5))
        k_cut = clamp((t - L('L04', 0.40)) / 0.5)
        lay = canvas()
        card(lay, (8, 16, 92, 25.5), r=32)
        if k_cut <= 0: txt(lay, 'Aku suka makan bakso.', (50, 20.75), 52, F['ink'], 'SemiBold')
        else:
            chip_row(lay, pieces, 20.75, 40, gap=1.2, k=1.0, spread=ease_out_back(k_cut),
                     cols=[F['white']] * 6 if k_cut < 0.3 else None)
        comp(im, lay, a, sc, (50, 20))
        if 0 < k_cut < 1:   # scissor sweep line
            lay = canvas(); x = lerp(8, 92, k_cut); line(lay, x, 15, x, 26.5, F['coral'], 8); comp(im, lay)
        a2, sc2 = appear(t, L('L04', 0.80))
        lay = canvas()
        arrow(lay, 50, 27.5, 50, 32, 1, F['ink2'])
        badge(lay, '= 6 token  (ilustrasi)', 50, 36.5, F['ink'], F['white'], 34)
        comp(im, lay, a2, sc2, (50, 34))

    elif sid == 'SH05':   # word / half word / punctuation
        rows = [('suka', F['blue'], 'satu kata', 0.15), ('bak', F['coral'], 'setengah kata', 0.45), ('.', F['mint'], 'tanda baca', 0.8)]
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, '1 token bisa...', (50, 11), 46, F['ink']); comp(im, lay, a, sc, (50, 11))
        for i, (p, c, lab, f_) in enumerate(rows):
            y = 19 + i * 8.5
            def f(l, p=p, c=c, lab=lab, y=y):
                card(l, (12, y - 3.3, 88, y + 3.3), r=30)
                chip(l, p, 26, y, c, 50); arrow(l, 37, y, 47, y, 1, F['ink2'], 6)
                txt(l, lab, (51, y), 44, F['ink'], 'SemiBold', 'lm')
            G(L('L05', f_), f, (50, y))

    elif sid == 'SH06':   # makan vs memakan-makanan
        a, sc = appear(t, s['start'] + 0.05)
        def f1(l):
            card(l, (8, 10, 92, 21), r=32)
            txt(l, '"makan"', (14, 15.5), 44, F['ink'], 'SemiBold', 'lm')
            chip(l, 'makan', 60, 15.5, F['blue'], 44); badge(l, '1 token', 81, 15.5, F['ink'], F['white'], 26)
        G(L('L06', 0.05), f1, (50, 15))
        def f2(l):
            card(l, (8, 23.5, 92, 38), r=32)
            txt(l, '"memakan-makanan"', (50, 27.2), 44, F['ink'], 'SemiBold')
            chip_row(l, ['mem', 'akan', '-', 'makan', 'an'], 33, 40, gap=1.2, k=clamp((t - L('L06', 0.7)) / 0.5))
        G(L('L06', 0.5), f2, (50, 30))
        a3, sc3 = appear(t, L('L06', 0.85))
        lay = canvas(); badge(lay, 'beberapa token', 50, 41.5, F['coral'], F['white'], 32)
        txt(lay, 'ilustrasi — cara memotong tiap model beda', (50, 45.3), 26, F['ink2'], 'Medium'); comp(im, lay, a3, sc3, (50, 43))

    elif sid == 'SH07':   # tokens -> compute -> cost
        a, sc = appear(t, s['start'] + 0.1)
        fast = clamp((t - L('L07', 0.55)) / 0.4)
        speed = lerp(9, 22, fast)
        lay = canvas()
        card(lay, (5, 9, 95, 34), r=40)
        ai_box(lay, 50, 20.5, 0.75)
        # stream: chip positions are pure functions of t (phase = t*speed)
        ph = (t - s['start']) * speed
        for i in range(-1, 4):
            x = 9 + ((ph + i * 9.0) % 36)
            if x < 39: chip(lay, ['tok', 'en', 'ka', 'ta', '.', 'AI'][i % 6], x, 20.5, CHIPC[i % 5], 30, a=255 * clamp((39 - x) / 4))
        txt(lay, 'tenaga komputasi', (50, 30.5), 30, F['ink2'], 'SemiBold')
        # cost meter on the right
        n_tok = int(clamp((t - s['start']) / (s['end'] - s['start'])) ** 1.6 * 2400)
        rr(lay, (64, 13, 90, 28), 24, F['bg'])
        txt(lay, 'token', (77, 15.5), 28, F['ink2'], 'Medium'); txt(lay, f'{n_tok:,}'.replace(',', '.'), (77, 19), 44, F['ink'])
        fill = clamp(n_tok / 2400)
        rr(lay, (67, 23, 87, 25.5), 14, F['gray']); rr(lay, (67, 23, 67 + 20 * fill, 25.5), 14, F['coral'])
        txt(lay, 'biaya', (77, 26.8), 24, F['coral'], 'SemiBold')
        comp(im, lay, a, sc, (50, 21))
        a2, sc2 = appear(t, L('L07', 0.62))
        lay = canvas(); badge(lay, 'makin banyak token = makin besar biaya', 50, 39.5, F['coral'], F['white'], 32)
        comp(im, lay, a2, sc2, (50, 39.5))

    elif sid == 'SH08':   # input & output
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Yang dihitung ada 2', (50, 10.5), 46, F['ink']); comp(im, lay, a, sc, (50, 10.5))
        lay = canvas(); ai_box(lay, 80, 26, 0.55); comp(im, lay, a, sc, (80, 26))
        for k_, (y, lab, sub, col, f_, rev) in enumerate([(19, 'INPUT', 'pertanyaan kamu', F['blue'], 0.2, False),
                                                           (33, 'OUTPUT', 'jawaban AI', F['coral'], 0.62, True)]):
            t0 = L('L08', f_)
            if t < t0: continue
            al, scl = appear(t, t0)
            lay = canvas()
            card(lay, (5, y - 4.2, 64, y + 4.2), r=30)
            badge(lay, lab, 15, y - 1.6, col, F['white'], 28)
            txt(lay, sub, (8, y + 1.9), 32, F['ink'], 'SemiBold', 'lm')
            ph = (t - t0) * 10
            for i in range(4):
                p = ((ph + i * 6) % 24) / 24
                x = lerp(30, 62, p) if not rev else lerp(62, 30, p)
                chip(lay, 'tok', x, y - 1.6, col, 26, a=255 * min(1, 4 * p, 4 * (1 - p)))
            arrow(lay, 64.5, y, 71, y if not rev else y, 1, F['ink2'], 6) if not rev else arrow(lay, 71, y, 64.5, y, 1, F['ink2'], 6)
            comp(im, lay, al, scl, (35, y))

    elif sid == 'SH09':   # output usually pricier: balance
        a, sc = appear(t, s['start'] + 0.05)
        tilt = ease_out_back(clamp((t - L('L09', 0.35)) / 0.6)) * 9   # degrees, output side goes down
        lay = canvas()
        cx, cy = 50, 18.5
        poly(lay, [(cx, cy), (cx - 6, 40), (cx + 6, 40)], F['ink'])
        rr(lay, (30, 39.5, 70, 41.5), 10, F['ink'])
        ang = math.radians(tilt); arm = 30
        lx, ly = cx - arm * math.cos(ang), cy - arm * math.sin(ang) * W / H
        rx_, ry = cx + arm * math.cos(ang), cy + arm * math.sin(ang) * W / H
        line(lay, lx, ly, rx_, ry, F['ink'], 12); circ(lay, cx, cy, 20, F['coral'])
        for (px, py, lab, n, col) in ((lx, ly, 'INPUT', 1, F['blue']), (rx_, ry, 'OUTPUT', 3, F['coral'])):
            line(lay, px, py, px - 7, py + 9, F['ink2'], 4); line(lay, px, py, px + 7, py + 9, F['ink2'], 4)
            ImageDraw.Draw(lay).chord([X(px - 10), Y(py + 7.5), X(px + 10), Y(py + 12.5)], 0, 180, fill=rgba(col))
            coin_stack(lay, px, py + 8.5, n, 40)
            badge(lay, lab, px, py + 15, col, F['white'], 28)
        comp(im, lay, a, sc, (50, 26))
        a2, sc2 = appear(t, L('L09', 0.0))
        lay = canvas(); badge(lay, 'biasanya', 50, 10.5, F['yellow'], F['ink'], 32); comp(im, lay, a2, sc2, (50, 10.5))

    elif sid == 'SH10':   # Indonesian vs English token count (illustration)
        rows = [('ID', 'Apa kabar hari ini?', ['Apa', ' ka', 'bar', ' hari', ' ini', '?'], 13.5, F['coral'], 0.15),
                ('EN', 'How are you today?', ['How', ' are', ' you', ' today', '?'], 27.5, F['blue'], 0.4)]
        for lab, sent, pcs, y, col, f_ in rows:
            def f(l, lab=lab, sent=sent, pcs=pcs, y=y, col=col, f_=f_):
                card(l, (5, y - 5.5, 95, y + 5.5), r=34)
                badge(l, lab, 11.5, y - 2.6, col, F['white'], 30)
                txt(l, f'"{sent}"', (17, y - 2.6), 38, F['ink'], 'SemiBold', 'lm')
                chip_row(l, pcs, y + 2.4, 32, gap=1.0, k=clamp((t - L('L10', f_ + 0.15)) / 0.5), x_mid=46)
                if t >= L('L10', 0.85):
                    badge(l, f'{len(pcs)} token', 86, y + 2.4, F['ink'], F['white'], 26)
            G(L('L10', f_), f, (50, y))
        a, sc = appear(t, L('L10', 0.9))
        lay = canvas(); txt(lay, 'ilustrasi — jumlah asli tergantung model', (50, 35.2), 26, F['ink2'], 'Medium'); comp(im, lay, a, sc)
        if t >= L('L11', 0.0):
            k = clamp((t - L('L11', 0.1)) / 0.9)
            lay = canvas()
            coin_stack(lay, 30, 44.5, 1 + int(k * 3.99), 40); coin_stack(lay, 70, 44.5, 1 + int(k * 2.99), 40)
            txt(lay, 'ID', (30, 46.2), 28, F['coral']); txt(lay, 'EN', (70, 46.2), 28, F['blue'])
            comp(im, lay, min(1, (t - L('L11', 0.0)) * 4))
            a, sc = appear(t, L('L11', 0.7))
            lay = canvas(); badge(lay, 'lebih "mahal"', 50, 40, F['coral'], F['white'], 32); comp(im, lay, a, sc, (50, 40))

    elif sid == 'SH11':   # three ways
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, '3 CARA\nHEMAT TOKEN', (50, 19), 86, F['ink'], 'Bold', spacing=4); comp(im, lay, a, sc, (50, 19))
        for i in range(3):
            a, sc = appear(t, L('L12', 0.2 + 0.25 * i))
            lay = canvas(); circ(lay, 32 + 18 * i, 35, 52, CHIPC[i]); txt(lay, str(i + 1), (32 + 18 * i, 35.2), 60, F['white'])
            comp(im, lay, a, sc, (32 + 18 * i, 35))

    elif sid in ('SH12', 'SH13', 'SH14'):
        n = int(sid[-1]) - 1; lid = ['L13', 'L14', 'L15'][n - 1]
        title = ['Prompt yang padat', 'Minta jawaban singkat', 'Jangan kirim ulang semua'][n - 1]
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        circ(lay, 15, 11.5, 46, CHIPC[n - 1]); txt(lay, str(n), (15, 11.7), 56, F['white'])
        txt(lay, title, (23, 11.5), 46, F['ink'], 'Bold', 'lm')
        comp(im, lay, a, sc, (40, 11.5))
        if n == 1:
            def bad(l):
                bubble(l, (8, 17, 84, 23.5), '', 'u', size=30, fill=F['gray'], tcol=F['ink'])
                txt(l, 'Halo AI, apa kabar? Jadi gini, aku mau', (11.2, 19.0), 30, F['ink'], 'Medium', 'lm')
                txt(l, 'minta tolong, kalau bisa sih...', (11.2, 21.5), 30, F['ink'], 'Medium', 'lm')
                cross(l, 88, 20.2, 0.9)
            G(L(lid, 0.15), bad, (50, 20))
            def good(l):
                bubble(l, (8, 27, 84, 33.5), 'Buat 3 ide caption kopi, maks 10 kata.', 'u', size=30)
                check(l, 88, 30.2, 0.9)
            G(L(lid, 0.55), good, (50, 30))
        elif n == 2:
            def f(l):
                bubble(l, (8, 16.5, 80, 22.5), 'Jawab singkat, 3 poin saja.', 'u', size=32)
            G(L(lid, 0.2), f, (50, 19))
            def g(l):
                card(l, (20, 25, 92, 41), r=30)
                for i in range(3):
                    circ(l, 25, 29 + i * 4.3, 12, CHIPC[i]); rr(l, (28, 28.2 + i * 4.3, 28 + [44, 36, 50][i], 29.8 + i * 4.3), 10, F['gray'])
                check(l, 88, 26, 0.8)
            G(L(lid, 0.5), g, (55, 32))
        else:
            k = clamp((t - L(lid, 0.15)) / 0.8)
            lay = canvas()
            for i in range(int(k * 7)):   # chat history piling up, re-sent
                y = 34 - i * 2.4
                rr(lay, (10 + (i % 2) * 6, y - 1.0, 52 + (i % 2) * 6, y + 1.0), 14, F['blue'] if i % 2 == 0 else F['white'])
            comp(im, lay)
            a2, sc2 = appear(t, L(lid, 0.3))
            lay = canvas(); arrow(lay, 64, 27, 76, 27, 1, F['ink2']); ai_box(lay, 85, 27, 0.4)
            txt(lay, 'seluruh obrolan', (33, 39), 30, F['ink2'], 'SemiBold'); comp(im, lay, a2, sc2, (75, 27))
            a3, sc3 = appear(t, L(lid, 0.6))
            lay = canvas(); cross(lay, 70, 19, 1.2); badge(lay, 'kalau nggak perlu', 70, 43, F['coral'], F['white'], 28)
            comp(im, lay, a3, sc3, (70, 19))

    elif sid == 'SH15':   # Sakelar AI package
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); wordmark(lay, 50, 10.5, 220, tsize=44)
        comp(im, lay, a, sc, (50, 12))
        a2, sc2 = appear(t, L('L16', 0.55))
        def box(l):
            rr(l, (30, 24, 70, 42), 22, F['blue']); rr(l, (27, 21, 73, 26), 18, '#3561B3')
            rr(l, (47.5, 21, 52.5, 42), 6, F['yellow'])
            txt(l, 'PAKET TOKEN', (50, 34.5), 44, F['white'])
        G(L('L16', 0.55), box, (50, 32))
        for i in range(5):   # chips dropping into the box (pure function of t)
            t0 = L('L16', 0.6) + i * 0.18
            if t < t0: continue
            p = clamp((t - t0) / 0.5); y = lerp(17.5, 23, p * p)
            lay = canvas(); chip(lay, 'tok', 38 + i * 6, y, CHIPC[i], 26, a=255 * (1 - clamp((p - 0.85) / 0.15))); comp(im, lay)

    elif sid == 'SH16':   # packages per model (placeholder values)
        rows = [('Model A', '5M token', F['blue']), ('Model B', '10M token', F['coral']), ('Model C', '20M token', F['mint'])]
        for i, (m, q, col) in enumerate(rows):
            y = 13 + i * 8.6
            def f(l, m=m, q=q, col=col, y=y):
                card(l, (8, y - 3.5, 92, y + 3.5), r=30)
                circ(l, 14.5, y, 30, col)
                txt(l, m, (19, y), 40, F['ink'], 'SemiBold', 'lm')
                chip(l, q, 77, y, col, 36)
            G(L('L17', 0.08 + 0.12 * i), f, (50, y))
        a, sc = appear(t, L('L17', 0.65))
        lay = canvas(); badge(lay, 'M = juta token', 50, 40, F['yellow'], F['ink'], 36)
        txt(lay, 'angka contoh — sesuaikan paket asli', (50, 44.5), 26, F['ink2'], 'Medium'); comp(im, lay, a, sc, (50, 41))

    elif sid == 'SH17':   # choose model -> choose package -> use until empty
        steps = [('1', 'Pilih\nmodel', 0.4), ('2', 'Pilih\npaket', 0.55), ('3', 'Pakai', 0.72)]
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas(); txt(lay, 'Nggak perlu hitung ribet', (50, 10.5), 44, F['ink']); comp(im, lay, a, sc, (50, 10.5))
        for i, (n, lab, f_) in enumerate(steps):
            x = 20 + 30 * i
            def f(l, n=n, lab=lab, x=x, i=i):
                card(l, (x - 12, 15, x + 12, 29), r=30)
                circ(l, x, 18.6, 30, CHIPC[i]); txt(l, n, (x, 18.7), 36, F['white'])
                txt(l, lab, (x, 24.6), 34, F['ink'], 'SemiBold', spacing=2)
                if i < 2: arrow(l, x + 12.5, 22, x + 17.5, 22, 1, F['ink2'], 6)
            G(L('L18', f_), f, (x, 22))
        if t >= L('L18', 0.72):
            k = clamp((t - L('L18', 0.75)) / max(0.5, s['end'] - L('L18', 0.75) - 0.1))
            lay = canvas()
            txt(lay, 'sisa token', (12, 35), 30, F['ink2'], 'SemiBold', 'lm')
            rr(lay, (12, 37.5, 88, 41.5), 20, F['gray']); rr(lay, (12, 37.5, 12 + 76 * (1 - k), 41.5), 20, F['mint'])
            txt(lay, f'{(1 - k) * 10:.1f}M', (88, 35), 30, F['ink'], 'Bold', 'rm')
            comp(im, lay, min(1, (t - L('L18', 0.72)) * 5))

    elif sid == 'SH18':   # light vs heavy task -> one door
        rows = [('Tugas ringan', 'Model hemat', F['mint'], 15, 'L19', 0.05), ('Tugas berat', 'Model jago', F['coral'], 29, 'L19', 0.55)]
        for lab, mod, col, y, lid, f_ in rows:
            def f(l, lab=lab, mod=mod, col=col, y=y):
                card(l, (4, y - 4, 40, y + 4), r=28); txt(l, lab, (22, y), 36, F['ink'], 'SemiBold')
                arrow(l, 41, y, 47, y, 1, F['ink2'], 6)
                chip(l, mod, 58.5, y, col, 34)
            G(L(lid, f_), f, (25, y))
        if t >= L('L20', 0.0):
            k = clamp((t - L('L20', 0.0)) / 0.5)
            lay = canvas()
            arrow(lay, 69, 15, 78, 20.5, k, F['ink2'], 6); arrow(lay, 69, 29, 78, 23.5, k, F['ink2'], 6)
            comp(im, lay)
            def door(l):
                rr(l, (79, 12, 96, 33), 22, F['ink']); rr(l, (81.5, 14.5, 93.5, 33), 14, F['blue'])
                circ(l, 91, 24, 10, F['yellow'])
                badge(l, 'Sakelar AI', 87.5, 36.5, F['blue'], F['white'], 28)
                txt(l, 'satu pintu', (87.5, 40.2), 28, F['ink'], 'Bold')
            G(L('L20', 0.1), door, (87.5, 25))

    elif sid == 'SH19':   # token = coin
        k = t - s['start']
        lay = canvas(); coin(lay, 50, 22, 150, squash=math.cos(k * 2.2) if k < 1.43 else 1.0); comp(im, lay, min(1, k * 4))
        a, sc = appear(t, L('L21', 0.5))
        lay = canvas(); badge(lay, 'pakai sesuai kebutuhan', 50, 39.5, F['ink'], F['white'], 36); comp(im, lay, a, sc, (50, 39.5))

    elif sid == 'SH20':   # "aku rela kok"
        for i, (x, y, s_, ph) in enumerate(((22, 30, 1.6, 0), (78, 24, 2.0, 1.1), (64, 40, 1.2, 2.2), (34, 16, 1.0, 3.1), (50, 22, 2.6, 0.5))):
            t0 = L('L22', 0.25 + 0.1 * i)
            if t < t0: continue
            p = t - t0; a = min(1, p * 3)
            lay = canvas(); heart(lay, x + 0.6 * math.sin(p * 2 + ph), y - p * 1.5, s_ * (0.7 + 0.3 * ease_out_back(clamp(p / 0.4))))
            comp(im, lay, a)
        a, sc = appear(t, L('L22', 0.6))
        lay = canvas(); txt(lay, 'aku rela kok', (50, 10.5), 50, F['coral'], 'Bold'); comp(im, lay, a, sc, (50, 10.5))

    elif sid == 'SH21':   # end card
        a, sc = appear(t, s['start'] + 0.05)
        lay = canvas()
        card(lay, (10, 9, 90, 42), r=44)
        wordmark(lay, 50, 14.5, 240, tsize=50)
        txt(lay, 'Satu pintu, banyak model AI', (50, 25.5), 38, F['ink'], 'SemiBold')
        rr(lay, (18, 29.5, 82, 35), 40, F['blue']); txt(lay, 'app.sakelar.web.id', (50, 32.25), 42, F['white'], 'Bold')
        txt(lay, 'Ep 06 · Token Itu Apa Sih?', (50, 38.7), 30, F['ink2'], 'Medium')
        comp(im, lay, a, sc, (50, 25))


# Per-shot spec: purpose, objects, anim (list of (t_rel, text)), screen text, sfx (list of (t_rel, name, len, dB, fn)), qa
def spec(sid):
    s = SH[sid]; d = round(s['end'] - s['start'], 3)
    if sid == 'SH01': return dict(
        goal='Membuka dengan hal yang sering dilihat: harga AI ditulis "per sejuta token".',
        obj=['Kartu "Daftar Harga Model AI": box x=12–88%, y=11–34%, putih, radius 40px, drop shadow navy 13% offset y+0.45%. Header navy y=11–16.5%.',
             'Baris "Model A" y=20.2% dan "Model B" y=26.4%: pill krem x=16–84%, tinggi 4.4%.',
             'Highlight kuning di belakang teks "1 juta token": x=68.3% → lebar 0→13.5%, tinggi 2.8%, opacity 78%.',
             'Bubble "?" coral: lingkaran r=46px di x=85%, y=10%.'],
        anim=[(0.15, 'Kartu pop-in: scale 0.90→1.00 easeOutBack 0.35 s, opacity 0→1 dalam 0.16 s (anchor 50%,22%).'),
              (r(sid, 'L01', 0.55), 'Highlight kuning tumbuh dari kiri ke kanan 0.30 s easeOutCubic (tepat saat kata "token").'),
              (r(sid, 'L01', 0.75), 'Bubble "?" pop-in 0.35 s easeOutBack.')],
        text=['"Daftar Harga Model AI" — Poppins Medium 38px, putih, center (50%,13.7%).',
              '"Model A" / "Model B" — Poppins Medium 36px, navy, left (19%, y baris).',
              '"Rp ???" — Poppins Bold 38px, navy, right-aligned di x=60%.',
              '"/ 1 juta token" — Poppins Medium 30px, abu #5A6684, left x=61%.',
              '"(contoh tampilan)" — Poppins Medium 26px, abu, center (50%,31.6%).', '"?" — Poppins Bold 60px, putih (85%,10%).'],
        sfx=[(0.15, 'pop', 0.15, -16, 'kartu muncul'), (r(sid, 'L01', 0.55), 'swipe', 0.3, -18, 'highlight'),
             (r(sid, 'L01', 0.75), 'boing', 0.25, -16, 'tanda tanya')],
        qa=['Harga tertulis "Rp ???", bukan angka karangan.', 'Highlight berada DI BELAKANG teks, teks tetap terbaca.'])
    if sid == 'SH02': return dict(
        goal='Membuat penonton menebak: token = koin arcade?',
        obj=['Mesin arcade: box navy x=22–78%, y=9–44%, radius 44px. Layar dalam x=27–73%, y=12–22% (#2C3A63).',
             'Slot koin x=44–56%, y=24–35%. Tiga tombol bulat r=30px di (37,39.5) coral, (50,39.5) mint, (63,39.5) biru.',
             'Koin "TOKEN": elips kuning r=95px di x=50%, y 31%→29.5%; rim #D99A1E.',
             'Tiga "?" coral Poppins Bold 90px di (20,12), (81,15), (76,40).'],
        anim=[(0.1, 'Mesin arcade pop-in 0.35 s easeOutBack.'),
              (r(sid, 'L02', 0.1), '"?" pertama pop-in, berikutnya tiap +12% durasi L02; semua bergoyang y ±0.6% sin(3t).'),
              (r(sid, 'L02', 0.45), 'Koin muncul (opacity 0→1 dalam 0.25 s), naik y 31→29.5% 0.4 s easeOutCubic, berputar: lebar = r·|cos(6·u)|.')],
        text=['"INSERT COIN" — Poppins Bold 54px, kuning #FFC94A, center (50%,17%).', '"TOKEN" pada koin — Bold, cokelat #9A6A10, hilang saat koin tipis (|cos|<0.45).', '"?" ×3.'],
        sfx=[(0.1, 'blip', 0.2, -18, 'mesin muncul'), (r(sid, 'L02', 0.45), 'coin', 0.6, -14, 'koin')],
        qa=['Koin tidak menutupi tulisan INSERT COIN.', 'Rotasi koin kontinu (fungsi waktu), tanpa lompatan.'])
    if sid == 'SH03': return dict(
        goal='Koreksi: token bukan koin, tapi mirip.',
        obj=['Koin r=120px di (34%,26%).', 'Simbol "≈" Poppins Bold 120px abu di (50%,26%).', 'Chip "token" biru di (69%,26%), font 64px.', 'Badge coral "mirip, bukan sama" di (50%,38%).'],
        anim=[(0.15, '"≈" pop-in.'), (0.25, 'Koin menipis horizontal: lebar ×(1 − 0.3·easeInOut(k)), k 0→1 dalam 0.6 s.'),
              (r(sid, 'L03', 0.3), 'Badge pop-in.'), (r(sid, 'L03', 0.5), 'Chip "token" pop-in easeOutBack.')],
        text=['"≈"', '"token" — Poppins Medium 64px putih di chip biru.', '"mirip, bukan sama" — Poppins Medium 32px putih di badge coral.'],
        sfx=[(r(sid, 'L03', 0.0), 'scratch', 0.3, -18, '"Bukan"'), (r(sid, 'L03', 0.5), 'pop', 0.15, -14, 'chip token')],
        qa=['Badge tidak overlap subtitle (badge y=38%, subtitle y≈52%).'])
    if sid == 'SH04': return dict(
        goal='Menunjukkan AI memotong kalimat jadi keping kecil (token).',
        obj=['Judul "AI nggak baca kalimat utuh" (50%,11.5%).', 'Kartu kalimat x=8–92%, y=16–25.5%.',
             'Kalimat contoh "Aku suka makan bakso." → 6 chip: [Aku][suka][makan][bak][so][.] di y=20.75%, warna bergilir biru/coral/kuning/mint/lilac.',
             'Garis potong coral (8px) menyapu x 8→92%.', 'Panah ke bawah (50%,27.5→32%) dan badge navy "= 6 token (ilustrasi)" (50%,36.5%).'],
        anim=[(0.1, 'Judul dan kartu pop-in.'), (r(sid, 'L04', 0.40), 'Potong: garis menyapu kiri→kanan 0.5 s; chip berpisah (jarak 0→1.2% easeOutBack); 30% awal chip masih putih lalu berwarna.'),
              (r(sid, 'L04', 0.80), 'Panah + badge "= 6 token" pop-in.')],
        text=['"AI nggak baca kalimat utuh" — Bold 42px navy.', '"Aku suka makan bakso." — Medium 52px (sebelum dipotong).', 'Chip: Medium 40px.', '"= 6 token  (ilustrasi)" — Medium 34px putih di badge navy.'],
        sfx=[(r(sid, 'L04', 0.40), 'snip', 0.5, -14, 'pemotongan'), (r(sid, 'L04', 0.80), 'pop', 0.15, -16, 'badge')],
        qa=['Semua 6 chip muat di kartu (x 8–92%).', 'Label "(ilustrasi)" wajib tampil — jumlah token asli tergantung tokenizer model.'])
    if sid == 'SH05': return dict(
        goal='Satu token bisa satu kata, setengah kata, atau tanda baca.',
        obj=['Judul "1 token bisa..." (50%,11%).', 'Tiga kartu x=12–88%, tinggi 6.6%, pusat y=19%, 27.5%, 36%.',
             'Kiri: chip ("suka" biru, "bak" coral, "." mint) di x=26%; panah x 37→47%; label kanan di x=51% left.'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L05', 0.15), 'Kartu 1 pop-in.'), (r(sid, 'L05', 0.45), 'Kartu 2 pop-in.'), (r(sid, 'L05', 0.80), 'Kartu 3 pop-in.')],
        text=['"1 token bisa..." — Bold 46px.', '"satu kata" / "setengah kata" / "tanda baca" — Medium 44px navy.'],
        sfx=[(r(sid, 'L05', 0.15), 'pop', 0.15, -16, 'kartu 1'), (r(sid, 'L05', 0.45), 'pop', 0.15, -16, 'kartu 2'), (r(sid, 'L05', 0.80), 'pop_hi', 0.15, -16, 'kartu 3')],
        qa=['Kartu muncul sinkron dengan kata yang diucapkan.'])
    if sid == 'SH06': return dict(
        goal='Contoh: kata pendek 1 token, kata panjang pecah jadi beberapa.',
        obj=['Kartu 1 x=8–92%, y=10–21%: teks "\\"makan\\"" kiri, chip "makan" biru (60%,15.5%), badge "1 token" (81%,15.5%).',
             'Kartu 2 x=8–92%, y=23.5–38%: "\\"memakan-makanan\\"" (50%,27.2%) + 5 chip [mem][akan][-][makan][an] di y=33%.',
             'Badge coral "beberapa token" (50%,41.5%) + catatan kecil (50%,45.3%).'],
        anim=[(r(sid, 'L06', 0.05), 'Kartu 1 pop-in.'), (r(sid, 'L06', 0.5), 'Kartu 2 pop-in.'), (r(sid, 'L06', 0.7), 'Chip kartu 2 muncul berurutan dalam 0.5 s (stagger), tiap chip turun 1.2% → 0 easeOutBack.'),
              (r(sid, 'L06', 0.85), 'Badge + catatan pop-in.')],
        text=['"makan", "memakan-makanan" — Medium 44px.', '"1 token" — badge navy 26px.', '"beberapa token" — badge coral 32px.', '"ilustrasi — cara memotong tiap model beda" — Medium 26px abu.'],
        sfx=[(r(sid, 'L06', 0.7), 'snips', 0.5, -16, 'pecah jadi chip')],
        qa=['Potongan chip disebut ilustrasi, bukan hasil tokenizer sungguhan.'])
    if sid == 'SH07': return dict(
        goal='Tiap token butuh komputasi → makin banyak token makin mahal.',
        obj=['Kartu besar x=5–95%, y=9–34%.', 'Chip AI navy (ikon prosesor) skala 0.75 di (50%,20.5%).',
             'Aliran chip kecil di y=20.5% bergerak dari x=9% → 39% (masuk ke AI), fade 4% terakhir.',
             'Panel meter kanan x=64–90%, y=13–28%: label "token", angka penghitung, bar biaya x=67–87% y=23–25.5% coral.',
             'Badge coral "makin banyak token = makin besar biaya" (50%,39.5%).'],
        anim=[(0.1, 'Kartu pop-in.'), (0.1, f'Posisi chip: x = 9 + ((u·speed + i·9) mod 36). speed 9%/s, naik ke 22%/s mulai {r(sid, "L07", 0.55)} s (ramp 0.4 s).'),
              (0.0, f'Angka token = floor(2400·(u/{d})^1.6), format titik ribuan; bar = angka/2400.'),
              (r(sid, 'L07', 0.62), 'Badge pop-in.')],
        text=['"AI" Bold 48px putih.', '"tenaga komputasi" Medium 30px abu.', '"token" 28px; angka Bold 44px navy; "biaya" 24px coral.', '"makin banyak token = makin besar biaya" Medium 32px putih.'],
        sfx=[(0.1, 'hum', d - 0.1, -24, 'komputasi'), (r(sid, 'L07', 0.55), 'tick', 1.5, -20, 'angka naik'), (r(sid, 'L07', 0.62), 'kaching', 0.4, -16, 'biaya')],
        qa=['Angka penghitung naik monoton.', 'Pose desk: monitor di kanan tidak menutupi subtitle.'])
    if sid == 'SH08': return dict(
        goal='Yang dihitung ada dua: input (pertanyaan) dan output (jawaban).',
        obj=['Judul "Yang dihitung ada 2" (50%,10.5%).', 'Chip AI skala 0.55 di (80%,26%).',
             'Jalur INPUT: kartu x=5–64%, y=14.8–23.2%; badge biru "INPUT"; teks "pertanyaan kamu"; chip "tok" biru mengalir kiri→kanan; panah 64.5→71%.',
             'Jalur OUTPUT: kartu y=28.8–37.2%; badge coral "OUTPUT"; "jawaban AI"; chip coral mengalir kanan→kiri; panah 71→64.5%.'],
        anim=[(0.05, 'Judul + chip AI pop-in.'), (r(sid, 'L08', 0.2), 'Jalur INPUT pop-in; chip: p = ((u·10 + i·6) mod 24)/24, x = 30→62%.'),
              (r(sid, 'L08', 0.62), 'Jalur OUTPUT pop-in; chip arah sebaliknya.')],
        text=['"Yang dihitung ada 2" Bold 46px.', '"INPUT"/"OUTPUT" badge 28px.', '"pertanyaan kamu" / "jawaban AI" Medium 32px.'],
        sfx=[(r(sid, 'L08', 0.2), 'whoosh', 0.4, -18, 'input'), (r(sid, 'L08', 0.62), 'whoosh', 0.4, -18, 'output')],
        qa=['Arah aliran jelas: input menuju AI, output keluar dari AI.'])
    if sid == 'SH09': return dict(
        goal='Harga output biasanya lebih mahal.',
        obj=['Timbangan: tiang navy segitiga dari (50,18.5) ke alas y=40%; alas x=30–70%, y=39.5–41.5%.',
             'Lengan 12px panjang 30% dari pivot (50%,18.5%), pivot lingkaran coral r=20px.',
             'Piring kiri biru + 1 koin + badge "INPUT"; piring kanan coral + 3 koin + badge "OUTPUT".', 'Badge kuning "biasanya" (50%,10.5%).'],
        anim=[(0.0, 'Badge "biasanya" pop-in di awal L09.'), (0.05, 'Timbangan pop-in.'),
              (r(sid, 'L09', 0.35), 'Lengan miring 0°→9° (sisi OUTPUT turun) 0.6 s easeOutBack.')],
        text=['"biasanya" Medium 32px navy di badge kuning.', '"INPUT" / "OUTPUT" badge 28px.'],
        sfx=[(r(sid, 'L09', 0.35), 'clunk', 0.3, -14, 'miring'), (r(sid, 'L09', 0.5), 'coins', 0.4, -18, 'koin')],
        qa=['Ada kata "biasanya" di layar — bukan klaim mutlak.'])
    if sid == 'SH10': return dict(
        goal='Bahasa Indonesia bisa butuh lebih banyak token daripada bahasa Inggris.',
        obj=['Kartu ID x=5–95%, y=8–19%: badge coral "ID" (11.5%,10.9%), kalimat "Apa kabar hari ini?", chip 6 [Apa][ka][bar][hari][ini][?] y=15.9%, badge "6 token" (86%).',
             'Kartu EN y=22–33%: badge biru "EN", "How are you today?", chip 5 [How][are][you][today][?] y=29.9%, badge "5 token".',
             'Catatan "ilustrasi — jumlah asli tergantung model" (50%,35.2%).',
             'L11: tumpukan koin kiri (30%) naik 1→4 koin, kanan (70%) 1→3 koin, alas y=44.5%; badge coral "lebih \\"mahal\\"" (50%,40%).'],
        anim=[(r(sid, 'L10', 0.15), 'Kartu ID pop-in; chip mulai +0.15·L10, stagger 0.5 s.'), (r(sid, 'L10', 0.4), 'Kartu EN pop-in, chip menyusul.'),
              (r(sid, 'L10', 0.85), 'Badge jumlah token muncul.'), (r(sid, 'L10', 0.9), 'Catatan ilustrasi muncul.'),
              (r(sid, 'L11', 0.1), 'Koin bertambah satu per satu selama 0.9 s.'), (r(sid, 'L11', 0.7), 'Badge "lebih mahal" pop-in.')],
        text=['"ID" / "EN"', '"\\"Apa kabar hari ini?\\"" / "\\"How are you today?\\"" Medium 38px.', '"6 token" / "5 token" badge 26px.', 'Catatan Medium 26px abu.', '"lebih \\"mahal\\"" Medium 32px.'],
        sfx=[(r(sid, 'L10', 0.0), 'ding', 0.4, -16, '"Dan nih"'), (r(sid, 'L11', 0.1), 'coins', 0.9, -16, 'koin')],
        qa=['Angka 6 vs 5 ditandai ilustrasi.', 'Tumpukan koin tidak menabrak subtitle.'])
    if sid == 'SH11': return dict(
        goal='Transisi ke tips: 3 cara hemat.',
        obj=['Judul 2 baris "3 CARA / HEMAT TOKEN" Bold 86px navy di (50%,19%).', 'Tiga lingkaran r=52px di (32,35), (50,35), (68,35): biru, coral, kuning, angka 1/2/3 putih 60px.'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L12', 0.2), 'Lingkaran 1 pop-in, 2 dan 3 menyusul tiap +25% durasi L12.')],
        text=['"3 CARA\\nHEMAT TOKEN"', '"1", "2", "3"'],
        sfx=[(r(sid, 'L12', 0.2), 'pop_hi', 0.6, -14, 'angka')], qa=['Judul tidak terpotong safe area.'])
    if sid in ('SH12', 'SH13', 'SH14'):
        n = int(sid[-1]) - 1; lid = ['L13', 'L14', 'L15'][n - 1]
        base = dict(goal=['Tips 1: tulis prompt padat.', 'Tips 2: minta jawaban singkat.', 'Tips 3: jangan kirim ulang seluruh obrolan.'][n - 1])
        head = f'Header: lingkaran nomor "{n}" r=46px di (15%,11.5%) + judul Bold 46px di x=23% left.'
        if n == 1: base.update(
            obj=[head, 'Bubble abu "Halo AI, apa kabar? Jadi gini, aku mau / minta tolong, kalau bisa sih..." x=8–84%, y=17–23.5% + ikon ✕ merah (88%,20.2%).',
                 'Bubble biru "Buat 3 ide caption kopi, maks 10 kata." x=8–84%, y=27–33.5% + ikon ✓ hijau (88%,30.2%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.15), 'Bubble buruk + ✕ pop-in.'), (r(sid, lid, 0.55), 'Bubble bagus + ✓ pop-in.')],
            text=['"Prompt yang padat"', 'Isi bubble Medium 30px (verbatim di atas).'],
            sfx=[(r(sid, lid, 0.15), 'buzz', 0.25, -18, '✕'), (r(sid, lid, 0.55), 'ding', 0.3, -16, '✓')])
        if n == 2: base.update(
            obj=[head, 'Bubble biru "Jawab singkat, 3 poin saja." x=8–80%, y=16.5–22.5%.', 'Kartu jawaban x=20–92%, y=25–41%: 3 baris bullet (titik warna + bar abu), ✓ (88%,26%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.2), 'Bubble prompt pop-in.'), (r(sid, lid, 0.5), 'Kartu jawaban pop-in.')],
            text=['"Minta jawaban singkat"', '"Jawab singkat, 3 poin saja." Medium 32px putih.'],
            sfx=[(r(sid, lid, 0.2), 'whoosh', 0.3, -18, 'prompt'), (r(sid, lid, 0.5), 'ding', 0.3, -16, 'jawaban')])
        if n == 3: base.update(
            obj=[head, 'Tumpukan bubble obrolan (bergantian biru/putih) x≈10–58%, mulai y=34% naik 2.4% per bubble, maks 7.', 'Panah 64→76% di y=27% ke chip AI kecil (85%,27%).',
                 'Label "seluruh obrolan" (33%,39%).', 'Ikon ✕ besar (70%,19%) + badge coral "kalau nggak perlu" (70%,43%).'],
            anim=[(0.05, 'Header pop-in.'), (r(sid, lid, 0.15), 'Bubble bertambah satu-satu selama 0.8 s.'), (r(sid, lid, 0.3), 'Panah + AI + label pop-in.'), (r(sid, lid, 0.6), '✕ + badge pop-in.')],
            text=['"Jangan kirim ulang semua"', '"seluruh obrolan" Medium 30px abu.', '"kalau nggak perlu" Medium 28px putih.'],
            sfx=[(r(sid, lid, 0.15), 'stack', 0.8, -18, 'bubble menumpuk'), (r(sid, lid, 0.6), 'buzz', 0.25, -16, '✕')])
        base['qa'] = ['Nomor tips sama dengan urutan dialog.', 'Contoh prompt ditulis persis.']
        return base
    if sid == 'SH15': return dict(
        goal='Masuk soft sell: di Sakelar AI token dijual dalam paket.',
        obj=['Logo Sakelar (versi gelap) lebar 220px di (50%,10.5%) + wordmark "Sakelar AI" Bold 44px di bawahnya.',
             'Kotak paket biru x=30–70%, y=24–42%; tutup x=27–73%, y=21–26%; pita kuning x=47.5–52.5%. Tulisan "PAKET TOKEN".',
             '5 chip "tok" jatuh ke kotak di x=38,44,50,56,62%.'],
        anim=[(0.05, 'Logo pop-in.'), (r(sid, 'L16', 0.55), 'Kotak pop-in.'), (r(sid, 'L16', 0.6), 'Chip jatuh y 17.5→23% (ease-in kuadrat, 0.5 s), stagger 0.18 s, fade di 15% akhir.')],
        text=['"Sakelar AI"', '"PAKET TOKEN" Bold 44px putih.', '"tok" chip 26px.'],
        sfx=[(0.05, 'jingle', 0.6, -14, 'logo'), (r(sid, 'L16', 0.6), 'coins', 1.0, -18, 'chip masuk kotak')],
        qa=['Logo memakai file asli Sakelar, tidak diubah bentuk.'])
    if sid == 'SH16': return dict(
        goal='Tiap model punya paket sendiri, isinya juta token ("M").',
        obj=['Tiga kartu x=8–92%, tinggi 7%, pusat y=13%, 21.6%, 30.2%: titik warna (14.5%), nama model (19% left), chip jumlah (77%).',
             'Badge kuning "M = juta token" (50%,40%) + catatan "angka contoh — sesuaikan paket asli" (50%,44.5%).'],
        anim=[(r(sid, 'L17', 0.08), 'Kartu Model A pop-in, B dan C tiap +12% durasi L17.'), (r(sid, 'L17', 0.65), 'Badge M + catatan pop-in (saat kata "M").')],
        text=['"Model A" / "Model B" / "Model C" Medium 40px.', '"5M token" / "10M token" / "20M token" — PLACEHOLDER, ganti dengan paket asli.', '"M = juta token" Medium 36px.', 'Catatan Medium 26px abu.'],
        sfx=[(r(sid, 'L17', 0.08), 'swipe', 0.6, -18, 'kartu'), (r(sid, 'L17', 0.65), 'ding', 0.3, -16, 'M')],
        qa=['Nama model & jumlah token masih placeholder sampai ada data resmi Sakelar AI.'])
    if sid == 'SH17': return dict(
        goal='Alurnya simpel: pilih model → pilih paket → pakai sampai habis.',
        obj=['Judul "Nggak perlu hitung ribet" (50%,10.5%).', 'Tiga kartu langkah lebar 24% di x=20,50,80%, y=15–29%: lingkaran nomor (y=18.6%), label (y=24.6%), panah antar kartu.',
             'Bar "sisa token": x=12–88%, y=37.5–41.5%, isi mint; label kiri "sisa token", kanan angka "10.0M"→"0.0M".'],
        anim=[(0.05, 'Judul pop-in.'), (r(sid, 'L18', 0.4), 'Langkah 1 pop-in.'), (r(sid, 'L18', 0.55), 'Langkah 2 pop-in.'), (r(sid, 'L18', 0.72), 'Langkah 3 pop-in + bar muncul.'),
              (r(sid, 'L18', 0.75), f'Bar menyusut linear 100%→0% sampai {round(d - 0.1, 2)} s; angka = 10·(1−k) M (contoh).')],
        text=['"Nggak perlu hitung ribet" Bold 44px.', '"Pilih\\nmodel", "Pilih\\npaket", "Pakai" Medium 34px.', '"sisa token" 30px; angka Bold 30px.'],
        sfx=[(r(sid, 'L18', 0.4), 'clicks', 0.8, -16, 'langkah'), (r(sid, 'L18', 0.75), 'whoosh', 1.0, -22, 'bar menyusut')],
        qa=['"10M" ditandai contoh (lihat catatan SH16).'])
    if sid == 'SH18': return dict(
        goal='Pilih model sesuai tugas; semuanya lewat satu pintu.',
        obj=['Kartu "Tugas ringan" x=4–40%, y=11–19% → panah → chip mint "Model hemat" (58.5%,15%).',
             'Kartu "Tugas berat" y=25–33% → panah → chip coral "Model jago" (58.5%,29%).',
             'Dua panah menyatu ke pintu: (69,15)→(78,20.5) dan (69,29)→(78,23.5).',
             'Pintu: kusen navy x=79–96%, y=12–33%; daun biru; gagang kuning (91%,24%); badge "Sakelar AI" (87.5%,36.5%) + "satu pintu" (87.5%,40.2%).'],
        anim=[(r(sid, 'L19', 0.05), 'Baris "ringan" pop-in.'), (r(sid, 'L19', 0.55), 'Baris "berat" pop-in.'),
              (r(sid, 'L20', 0.0), 'Panah tumbuh 0→100% dalam 0.5 s.'), (r(sid, 'L20', 0.1), 'Pintu + badge pop-in.')],
        text=['"Tugas ringan" / "Tugas berat" Medium 36px.', '"Model hemat" / "Model jago" chip 34px.', '"Sakelar AI" badge 28px; "satu pintu" Bold 28px.'],
        sfx=[(r(sid, 'L19', 0.05), 'pop', 0.15, -16, 'baris 1'), (r(sid, 'L19', 0.55), 'pop', 0.15, -16, 'baris 2'), (r(sid, 'L20', 0.1), 'chime', 0.6, -14, 'satu pintu')],
        qa=['Tidak menyebut nama model asli (belum ada daftar resmi).'])
    if sid == 'SH19': return dict(
        goal='Rangkuman: token itu kayak koin, pakai sesuai kebutuhan.',
        obj=['Koin "TOKEN" r=150px di (50%,22%).', 'Badge navy "pakai sesuai kebutuhan" (50%,39.5%).'],
        anim=[(0.0, 'Koin fade-in 0.25 s, berputar lebar = r·cos(2.2u) sampai u=1.43 s lalu diam menghadap depan.'), (r(sid, 'L21', 0.5), 'Badge pop-in.')],
        text=['"TOKEN" Bold di koin.', '"pakai sesuai kebutuhan" Medium 36px putih.'],
        sfx=[(0.0, 'coin', 1.4, -14, 'koin')], qa=['Putaran koin berhenti tepat menghadap depan.'])
    if sid == 'SH20': return dict(
        goal='Punchline manis: ngobrol sama penonton, Reina rela.',
        obj=['5 hati coral (flat) di (22,30), (78,24), (64,40), (34,16), (50,22), skala 1.0–2.6.', 'Teks "aku rela kok" Bold 50px coral (50%,10.5%).'],
        anim=[(r(sid, 'L22', 0.25), 'Hati muncul satu-satu tiap +10% durasi L22; tiap hati naik 1.5%/s, goyang x ±0.6% sin(2p+φ), skala 0.7→1.0 easeOutBack 0.4 s.'),
              (r(sid, 'L22', 0.6), 'Teks pop-in.')],
        text=['"aku rela kok" Bold 50px coral.'],
        sfx=[(r(sid, 'L22', 0.25), 'sparkle', 1.0, -18, 'hati'), (r(sid, 'L22', 0.6), 'pop_hi', 0.2, -16, 'teks')],
        qa=['Mulut memakai sprite smile (mouth_smile_talk / smile_closed).'])
    if sid == 'SH21': return dict(
        goal='End card: ajakan mencoba Sakelar AI.',
        obj=['Kartu putih x=10–90%, y=9–42%, radius 44px.', 'Logo 240px + "Sakelar AI" Bold 50px (pusat 50%,14.5%).',
             '"Satu pintu, banyak model AI" (50%,25.5%).', 'Tombol biru x=18–82%, y=29.5–35% berisi "app.sakelar.web.id".', '"Ep 06 · Token Itu Apa Sih?" (50%,38.7%).'],
        anim=[(0.05, 'Kartu pop-in 0.35 s.'), (round(d - 0.5, 3), 'Seluruh frame fade ke warna latar #F6F1E7 dalam 0.5 s (linear).')],
        text=['"Sakelar AI"', '"Satu pintu, banyak model AI" Medium 38px.', '"app.sakelar.web.id" Bold 42px putih.', '"Ep 06 · Token Itu Apa Sih?" Medium 30px abu.'],
        sfx=[(0.05, 'stinger', 1.2, -12, 'end card')], qa=['URL tertulis persis "app.sakelar.web.id".', 'Video berakhir di frame latar polos.'])

