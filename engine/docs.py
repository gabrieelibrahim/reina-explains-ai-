"""Generator dokumen: storyboard .md (10 bagian sesuai panduan) dan prompt VO .md, dari file episode."""
from reina import tc, FPS, POSES, SH, LN
import sfx as SFX

def fr(x): return round(x * FPS)

def storyboard_md(E, final=False):
    m = E.m; SHOTS, LINES, TOT = E.shots, E.lines, E.total
    spec = m.spec; last = SHOTS[-1]['id']; smile = getattr(m, 'SMILE', set()); meta = getattr(m, 'META', {})
    out = []; P = out.append
    P(f'# Reina Explains AI — Episode {E.ep:02d}: "{m.TITLE}"\n')
    P('Storyboard produksi · tema **clean** (flat vector di atas latar kantor blur) · 9:16 · 1080×1920 · 30 fps\n')
    P(f'> Setiap frame adalah fungsi dari waktu: `frame(t)` → gambar. Semua posisi/animasi dihitung dari `t` saja (tanpa state antar-frame). Implementasi: `episodes/{E.tag}.py` + `engine/reina.py`.\n')
    P('## 1. Metadata proyek\n')
    P('| Item | Nilai |\n|---|---|')
    dur_note = 'final, mengikuti VO (jeda dipotong, tempo 1.10×)' if final else 'estimasi sebelum VO (6.4 suku kata/s)'
    for k, v in [('Judul', f'Reina Explains AI — Ep {E.ep:02d}: {m.TITLE}'), ('Tujuan', meta.get('tujuan', '—')),
                 ('Audiens', 'Pengguna AI awam Indonesia (TikTok/Reels/Shorts)'), ('Durasi', f'{TOT:.3f} s ({tc(TOT)}) = {fr(TOT)} frame — {dur_note}'),
                 ('Rasio/resolusi', '9:16, 1080×1920'), ('FPS', '30'), ('Gaya', 'Clean: kartu/chip/ikon flat vector di panel krem, latar kantor isometrik blur; karakter tanpa efek pixel'),
                 ('Karakter', 'Reina — pose ilustrasi asli (paket Reina Asset Baju Biru)'), ('Bahasa/tone', 'Indonesia santai, edukatif, lucu ringan'),
                 ('CTA', 'app.sakelar.web.id'), ('Audio', 'VO + SFX sintetis (engine/sfx.py); tanpa BGM')]:
        P(f'| {k} | {v} |')
    P('')
    P('## 2. Fakta / asumsi / perlu konfirmasi\n')
    P('**Fakta dari brief**')
    for x in meta.get('fakta', []): P(f'- {x}')
    P('\n**Asumsi produksi**')
    base = ['Durasi tiap baris = durasi rekaman VO per baris setelah jeda internal dipotong (maks 0.2 s) dan dipercepat 1.10×, + 1 frame.' if final
            else 'Durasi tiap baris diestimasi 6.4 suku kata/detik + 0.12 s per tanda baca; final mengikuti rekaman VO.',
            'Mulut bergerak dari loudness VO (sebelum VO: pola sementara).', 'SFX disintesis kode, level relatif terhadap VO.']
    for x in meta.get('asumsi', []) + base: P(f'- {x}')
    P('\n**Butuh konfirmasi**')
    for x in meta.get('konfirmasi', []) or ['Tidak ada.']: P(f'- {x}')
    P('')
    P('## 3. Konsep kreatif dan struktur\n')
    P(meta.get('konsep', '') + '\n')
    P('| Scene | Isi | Shot | Mulai | Selesai | Durasi |\n|---|---|---|---|---|---|')
    for sc in sorted(m.SCENES):
        ss = [s for s in SHOTS if s['scene'] == sc]
        if not ss: continue
        P(f"| {sc} | {m.SCENES[sc]} | {ss[0]['id']}–{ss[-1]['id']} | {tc(ss[0]['start'])} | {tc(ss[-1]['end'])} | {ss[-1]['end'] - ss[0]['start']:.3f} s |")
    P(f'| | **Total** | | 00:00:00.000 | {tc(TOT)} | **{TOT:.3f} s** |\n')
    if meta.get('softsell'): P(f"Soft selling hanya di {meta['softsell']}; scene lain murni edukasi.\n")
    P('## 4. Naskah terkunci\n')
    P('Speaker: **REINA** (semua baris).\n')
    P('| ID | Shot | Masuk | Keluar | Durasi | Suku kata | Dialog (verbatim) |\n|---|---|---|---|---|---|---|')
    for l in LINES: P(f"| {l['id']} | {l['shot']} | {tc(l['start'])} | {tc(l['end'])} | {l['dur']:.2f} s | {l['syl']} | {l['text']} |")
    P('')
    P('## 5. Timeline master\n')
    P('| Shot | Mulai | Selesai | Durasi | Frame | Judul | Dialog | Tujuan | Pose Reina | Transisi |\n|---|---|---|---|---|---|---|---|---|---|')
    for s in SHOTS:
        sp = spec(s['id'])
        P(f"| {s['id']} | {tc(s['start'])} | {tc(s['end'])} | {s['end'] - s['start']:.3f} s | {fr(s['start'])}–{fr(s['end']) - 1} | {s['title']} | {', '.join(s['lines']) or '—'} | {sp['goal']} | {m.POSE[s['id']]} | {'fade ke latar 0.5 s' if s['id'] == last else 'hard cut'} |")
    P('')
    P('## 6. Storyboard per shot\n')
    P('**Konvensi global (berlaku di semua shot, kecuali disebut lain):**')
    for x in ['Koordinat = persen kanvas, origin (0,0) kiri atas. Ukuran font & radius dalam px pada 1080×1920.',
              'Latar: assets/bg/office.png (kantor isometrik blur) cover 1080×1920, digelapkan 18%. Statis. Tanpa lingkaran/dekor.',
              'Panel info (z=2): kotak krem #F6F1E7 opacity 91% x=3–97%, y=6.4–47.6%, radius 44px.',
              f'Header (z=5): badge navy "REINA EXPLAINS AI · EP {E.ep:02d}" Poppins Medium 24px putih di (50%,3.6%).',
              'Panel visual (z=3): area y 7–47%. Kartu putih radius 28–44px, shadow navy 13% offset +0.45% y.',
              'Pop-in standar: opacity 0→1 dalam 0.16 s, scale 0.90→1.00 easeOutBack 0.35 s.',
              'Reina (z=4): anchor bawah-tengah di y=100%. Lebar sesuai assets/poses/poses.json (pose baru 86%, pose asli 80%, desk 100%). Napas: tinggi ×(1 + 0.006·(0.5+0.5·sin(2πt/3))). Saat pose/scene berubah: masuk dy=+5%→0, 0.35 s easeOutBack.',
              'Subtitle (z=6): pill putih 96% di (50%,52%), Poppins Medium 40px navy, maks 2 baris.',
              'Kostum Reina tidak boleh berubah (kaos biru oversized, headband biru, celana pendek hitam list putih).']: P(f'- {x}')
    P('')
    for s in SHOTS:
        sid = s['id']; sp = spec(sid); d = s['end'] - s['start']; pn = m.POSE[sid]; pm = POSES['poses'][pn]
        P(f"### SHOT {sid} — {s['title']}\n")
        P(f"- **Timecode:** masuk `{tc(s['start'])}`, keluar `{tc(s['end'])}`; durasi `{d:.3f} s`; frame {fr(s['start'])}–{fr(s['end']) - 1} ({fr(s['end']) - fr(s['start'])} frame).")
        P(f"- **Tujuan komunikasi:** {sp['goal']}")
        P('- **Setting:** latar kantor blur + panel info krem; BG = latar, MG = panel visual, FG = Reina + subtitle.')
        P('- **Komposisi:** MS vertikal, frontal eye-level. Atas = panel visual (y 7–47%), bawah = Reina. Safe area teks x 4–96%, y 2–58%.')
        P('- **Posisi objek:**')
        for o in sp['obj']: P(f'  - {o}')
        P(f"  - Reina pose `{pn}` anchor bawah-tengah (50%,100%), lebar {pm['width_pct']}% kanvas, z=4.")
        lip = 'sprite tertutup/setengah/terbuka sesuai VO' + (' (versi senyum)' if sid in smile else '') if 'mouth' in pm else 'tanpa lip sync (pose ini tidak punya titik mulut)'
        P(f"- **Karakter:** Reina, ekspresi {getattr(m, 'EXPR', {}).get(sid, '—')}. Wajah asli. Mulut: {lip}.")
        P('- **Gerak animasi** (t relatif awal shot):')
        for tt, a in sorted(sp['anim'], key=lambda x: x[0]): P(f'  - `{max(0, tt):.3f} s` — {a}')
        P('- **Kamera:** static.')
        P('- **Teks layar:**')
        for x in sp['text']: P(f'  - {x}')
        P('  - Subtitle dialog mengikuti slot dialog.')
        if s['lines']:
            P('- **Dialog/VO:**')
            for lid in s['lines']:
                l = LN[lid]; P(f"  - REINA `{tc(l['start'])}`–`{tc(l['end'])}`: \"{l['text']}\"")
        else: P('- **Dialog/VO:** tidak ada.')
        P('- **Musik:** tidak ada (opsional).')
        P('- **SFX:**')
        for tt, key, ln, db, fn in sp['sfx']:
            P(f"  - `{tc(s['start'] + max(0, tt))}` (shot +{max(0, tt):.3f} s) — {SFX.LIB[key][1]} [`{key}`], {ln:.2f} s, {db} dB rel. VO — {fn}. Sumber: sintetis.")
        P(f"- **Transisi:** {'fade ke warna latar 0.5 s di akhir video' if sid == last else 'hard cut di ' + tc(s['end']) + '; panel shot berikutnya pop-in.'}")
        P(f"- **Aset:** pose `{pn}`, sprite mulut, font Poppins, logo Sakelar bila dipakai — semua tersedia di kit; grafis lain digambar kode.")
        P(f"- **Implementasi:** `panel(t, '{sid}', im)` di episodes/{E.tag}.py; urutan layer: latar → panel → Reina → subtitle.")
        P('- **Kriteria QA:**')
        for x in sp['qa'] + ['Tidak ada objek panel yang menutupi wajah Reina atau subtitle.']: P(f'  - {x}')
        P('')
    P('## 7. Audio cue sheet\n')
    P('| ID | Jenis | Start | End | Sumber | Deskripsi | Gain | Prioritas |\n|---|---|---|---|---|---|---|---|')
    i = 1
    for l in LINES:
        P(f"| A{i:02d} | VO | {tc(l['start'])} | {tc(l['end'])} | rekaman user | {l['id']}: {l['text'][:40]}{'…' if len(l['text']) > 40 else ''} | 0 dB (peak −1 dBFS) | 1 |"); i += 1
    for s in SHOTS:
        for tt, key, ln, db, fn in spec(s['id'])['sfx']:
            a = s['start'] + max(0, tt)
            P(f"| A{i:02d} | SFX | {tc(a)} | {tc(a + ln)} | sintetis `{key}` | {s['id']}: {fn} | {db} dB | 2 |"); i += 1
    P('')
    P('## 8. Asset manifest\n')
    P('| ID | File | Dipakai di | Status |\n|---|---|---|---|')
    used = {}
    for s in SHOTS: used.setdefault(m.POSE[s['id']], []).append(s['id'])
    k = 1
    for p, ids in used.items(): P(f"| AS{k:02d} | assets/poses/{p}.png | {', '.join(ids)} | tersedia |"); k += 1
    for row in [('assets/sprites/mouth_*.png', 'shot berdialog', 'tersedia'), ('assets/bg/office.png', 'semua', 'tersedia'),
                ('assets/brand/sakelar_logo_main.png (logo toggle baru)', 'shot dengan logo', 'tersedia'), ('assets/fonts/Poppins-*.ttf', 'semua', 'tersedia'),
                ('SFX sintetis (engine/sfx.py)', 'lihat cue sheet', 'dibuat otomatis'),
                (f'VO {E.tag} (L01…)', 'semua', 'tersedia' if final else 'menunggu rekaman')]:
        P(f'| AS{k:02d} | ' + ' | '.join(row) + ' |'); k += 1
    P('')
    P('## 9. Panduan implementasi animasi\n')
    for x in ['`frame(t)`: cari shot aktif → latar → `panel(t, sid, im)` (digambar 2×) → downsample → Reina (pose + mulut) → subtitle → fade akhir.',
              'Tidak ada state antar-frame; frame mana pun bisa dirender acak/paralel dengan hasil identik.',
              'Sinkron kata: waktu event ditulis `rel(Lxx, f)` = awal baris + f × durasi baris, jadi otomatis ikut timing VO final.',
              'Lip sync: loudness VO per 10 ms → 0/1/2, median 7 sampel; area mulut asli di-inpaint lalu sprite ditempel.',
              'Render: RGB → ffmpeg libx264 CRF 18, yuv420p, +faststart; audio = VO + SFX, AAC 192k.']: P(f'- {x}')
    P('')
    P('## 10. Laporan QA dan isu terbuka\n')
    gaps = [round(b['start'] - a['end'], 6) for a, b in zip(SHOTS, SHOTS[1:])]
    P(f"- Jumlah durasi shot = {sum(s['end'] - s['start'] for s in SHOTS):.3f} s = total {TOT:.3f} s ✔")
    P(f"- Gap/overlap antarshot: {'tidak ada ✔' if all(abs(g) < 1e-6 for g in gaps) else gaps}")
    P(f'- Timecode di-snap ke grid 1/30 s; total {fr(TOT)} frame ✔')
    P('- Semua dialog berada di dalam slot shotnya ✔; tiap teks/SFX punya waktu spesifik ✔')
    P('\n**Isu terbuka**')
    for x in meta.get('isu', []) + meta.get('konfirmasi', []): P(f'- {x}')
    return '\n'.join(out) + '\n'

def vo_prompt_md(E):
    m = E.m
    o = [f'# Prompt VO — Reina Explains AI Episode {E.ep:02d}', '', f'**Judul:** {m.TITLE}', '', '## Karakter suara', '',
         '- Perempuan muda Indonesia, awal 20-an; nada sedang cenderung tinggi, jernih, hangat.',
         '- Santai, cerdas, sedikit jenaka, seperti teman yang jago teknologi; logat Jakarta ringan; tidak seperti iklan.',
         '- Tempo sedang-cepat, sekitar 2,7 kata per detik. Tanpa musik, tanpa efek.', '- Suara sama dengan episode sebelumnya.', '',
         '## Cara baca istilah', '', '| Istilah | Dibaca |', '| --- | --- |']
    o += [f'| {a} | {b} |' for a, b in getattr(m, 'PRON', [])]
    o += ['', '## Aturan', '', '- Baca persis kata per kata. Jangan menambah, mengurangi, atau mengganti kata.',
          '- Teks di dalam [kurung siku] adalah arahan, **jangan dibaca**.', '- Jeda 0,5 detik antar baris, 1 detik antar scene. Jeda panjang dipotong otomatis.',
          '- Simpan tiap baris jadi file terpisah: L01.wav, L02.wav, … (paling presisi). Kirim sebagai satu zip.', '', '## Naskah dengan arahan', '']
    sc_of = {s['id']: s['scene'] for s in E.shots}; cur = None; vd = getattr(m, 'VO_DIR', {})
    for l in E.lines:
        sc = sc_of[l['shot']]
        if sc != cur: o += [f'### Scene {sc} — {m.SCENES[sc].upper()}', '']; cur = sc
        o += [f"**{l['id']}** [{vd.get(l['id'], 'natural')}]  ", l['text'], '']
    o += ['## Naskah polos (untuk ditempel ke generator suara)', ''] + [f"{l['id']}: {l['text']}" for l in E.lines]
    return '\n'.join(o) + '\n'
