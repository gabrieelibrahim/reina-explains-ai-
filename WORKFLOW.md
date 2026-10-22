# REINA EXPLAINS AI — Workflow Produksi (tema "clean")

Kit ini berisi semua yang dibutuhkan untuk bikin satu episode dari nol: aset Reina, latar kantor, font, logo,
engine render (`frame(t)` = fungsi murni dari waktu), efek suara sintetis, dan generator storyboard/prompt VO.
Butuh: Python 3 + `numpy` + `pillow`, dan `ffmpeg`. (Tidak butuh internet untuk render.)

```
pip install numpy pillow --break-system-packages   # kalau belum ada
python run.py check  episodes/epXX.py              # validasi + keyframe (±30 detik)
python run.py stage1 episodes/epXX.py              # storyboard + gambar scene + prompt VO + zip
python run.py stage2 episodes/epXX.py suara.zip    # potong jeda, sinkron, SFX, render video
```

---

## Alur kerja (versi cepat)

| # | Langkah | Siapa | Hasil |
|---|---|---|---|
| 1 | Pilih topik + tulis naskah | Claude (sendiri, tanpa tanya) | `episodes/epXX.py` |
| 2 | Storyboard + visual tiap shot | Claude | `check` sampai semua gambar rapi |
| 3 | **Kirim sekaligus**: storyboard .md + gambar tiap scene + prompt VO .md + zip | Claude → user | `out/epXX/` (stage1) |
| 4 | Rekam suara per baris (L01.wav, L02.wav, …) → kirim zip | user | — |
| 5 | Render final: potong jeda, tempo 1.10×, lip sync, SFX, video | Claude | `reina_epXX.mp4` + `epXX_final_pack.zip` (stage2) |

Langkah 3 dan 4 lama (cek gambar dulu, baru minta prompt VO) **digabung**: gambar scene dan prompt VO dikirim
dalam satu kali kirim. User boleh langsung rekam; revisi visual tetap bisa kapan saja sebelum stage2.

### Langkah 1 — Pilih topik & tulis naskah
1. Baca **Log episode** (bagian bawah file ini + doc project `claude/reina_episode_log.md` kalau ada). Jangan ulang topik.
2. Pilih topik dari backlog atau topik AI yang lagi relevan. Kalau menyebut fakta yang bisa berubah (harga, fitur, rilis model), cek dulu lewat web search; kalau ragu, pakai kata "bisa/biasanya" atau jangan sebut.
3. Tulis naskah mengikuti **Panduan naskah** di bawah.

### Langkah 2 — Bikin file episode
1. `cp episodes/ep06.py episodes/epXX.py`, lalu ganti: `EP`, `TITLE`, `SCENES`, `META`, `PRON`, `VO_DIR`, `LINES`, `SHOTS`, `POSE`, `SMILE`, `EXPR`, `panel()`, `spec()`.
2. `python run.py check episodes/epXX.py` → **lihat SETIAP gambar `out/epXX/epXX_sceneN_*.png`** (pakai Read). Perbaiki teks terpotong, tumpang tindih, elemen keluar panel, lalu ulangi `check`.
3. Kriteria lolos: teks tidak keluar panel krem (x 4–96%, y 7–47%), tidak ada yang menutupi wajah Reina atau subtitle, label "contoh"/"ilustrasi" ada di angka yang bukan data resmi.

### Langkah 3 — Kirim paket stage1
`python run.py stage1 episodes/epXX.py` lalu kirim ke user dalam **satu** kirim (SendUserFile):
`epXX_storyboard.md`, `epXX_vo_prompt.md`, semua `epXX_sceneN_*.png`, dan `epXX_stage1_storyboard.zip`.
Pesan singkat (bahasa Indonesia): topik, durasi estimasi, placeholder yang perlu dicek, minta suara per baris.

### Langkah 5 — Render final (setelah user kirim suara)
1. Taruh file episode `.py` dari zip stage1 di `episodes/` (kalau sesi baru).
2. `python run.py stage2 episodes/epXX.py <zip_suara> --preview 8` → cek cepat sinkron & SFX (opsional).
3. `python run.py stage2 episodes/epXX.py <zip_suara>` → kirim `reina_epXX.mp4` + `epXX_final_pack.zip`.
   Render ±0.3–0.8 detik per frame per core (90 detik video ≈ 10–15 menit di 2 core). Jalankan di background lalu tunggu.
4. Ambil 4–5 frame dari video (ffmpeg -ss) dan lihat sebelum kirim.
- Suara boleh: zip/folder berisi `L01..LNN` (wav/mp3/m4a), atau satu file utuh (dipecah otomatis di jeda terpanjang — cek hasilnya).
- Default: jeda di dalam baris maks 0.2 s, tempo 1.10× (orang cepat bosan → video harus padat). Ubah dengan `--cap` / `--speed`.

---

## Aturan tetap (jangan dilanggar)

- **Reina**: rambut hitam panjang bergelombang, poni asimetris, headband biru, mata cokelat, garis tipis di pipi kiri, kaos biru oversized, celana pendek hitam list putih. **Kostum tidak pernah berubah.** Wajah selalu asli — **jangan tempel sprite mata**; lip sync hanya mulut.
- Pose tanpa titik mulut (`think`, `back`, `side_left`, `side_right`, `hands_face`) = tidak ada gerak bibir → pakai hanya untuk shot pendek/tanpa banyak dialog.
- **Tema clean**: latar kantor blur (`assets/bg/office.png`), panel krem di atas, kartu/chip flat vector, font Poppins. **Tanpa lingkaran/dekor di belakang Reina.** Tanpa efek pixel.
- 9:16, 1080×1920, 30 fps. Target durasi final **75–95 detik**.
- **Selalu ada SFX** (otomatis dari `spec()['sfx']`). Tanpa BGM kecuali diminta.
- Semua teks layar & dialog ditulis persis. Jangan mengarang harga, statistik, fitur, nama model, testimoni. Angka contoh wajib diberi label "contoh"/"ilustrasi".
- Balasan ke user: **singkat, bahasa Indonesia santai.**

## Fakta Sakelar AI yang boleh dipakai
- Sakelar AI = satu pintu (gateway) untuk banyak model AI.
- Token dijual dalam **paket per model**, isinya sekian juta token ("M" = juta token).
- URL: **app.sakelar.web.id**. Logo ada di `assets/brand/`.
- **Belum ada data resmi**: nama model, isi paket, harga → selalu placeholder ("Model A / 5M token — contoh", "Rp ???").

---

## Panduan naskah

- **Panjang**: 18–24 baris (`LINES`), tiap baris 1 kalimat pendek–sedang (≤ 140 karakter, idealnya 8–20 kata). Total estimasi 80–100 s (setelah VO dipercepat jadi ±75–95 s).
- **Bahasa**: Indonesia santai, logat Jakarta ringan (aku/kamu/kalian, "nggak", "nih", "sih"), tanpa istilah berat tanpa analogi.
- **Struktur scene** (contoh Ep06):
  1. **Hook** (2–3 baris): situasi sehari-hari / pertanyaan yang bikin penasaran. Detik pertama harus langsung masuk.
  2. **Inti konsep** (3–4 baris): jelaskan dengan analogi sederhana + contoh konkret.
  3. **Kenapa/bagaimana** (2–3 baris).
  4. **Fakta unik / twist** (1–2 baris).
  5. **Tips praktis** (3–4 baris, biasanya "3 cara …").
  6. **Soft sell Sakelar AI** (3–5 baris, SETELAH edukasi, nyambung ke topik, tidak hard selling).
  7. **Closing** (1–2 baris): rangkuman + punchline lucu/manis khas Reina.
  8. **End card** (tanpa dialog, 2.5 s): logo + app.sakelar.web.id.
- Soft sell maksimal ±25% durasi. Edukasi harus tetap berguna walau penonton tidak pakai Sakelar.
- Hindari klaim mutlak ("selalu", "pasti") untuk hal teknis yang tergantung model.

## Panduan shot & visual

- 1 shot ≈ 1 baris (boleh 2 baris pendek per shot). `SHOTS`: `(id, scene, judul, [nomor baris], jeda_awal, jeda_akhir)`; jeda biasa 0.1–0.25 s, akhir scene 0.4 s, end card `[]` dengan jeda_akhir 2.5.
- Ganti pose tiap 1–3 shot supaya hidup. Pose: lihat tabel di bawah.
- Visual tiap shot di `panel(t, sid, im)`: gambar di area **y 7–47%** (panel krem). Subtitle otomatis di y≈52%, Reina di bawah.
- Sinkron ke kata: pakai `rel('Lxx', f)` (waktu absolut pada fraksi f baris Lxx). Pola standar:
  ```python
  G(L('L05', 0.45), fungsi_gambar, anchor)   # pop-in elemen saat ±45% baris L05
  ```
- Helper siap pakai (engine/reina.py): `card, rr, circ, ell, txt, chip, chip_row, badge, bubble, check, cross, heart, coin, coin_stack, ai_box, arrow, line, poly, wordmark, appear, comp`. Warna: `F['blue'|'coral'|'yellow'|'mint'|'lilac'|'ink'|'ink2'|'white'|'gray'|'red'|'green']`.
- Semua gerak harus rumus dari `t` (tanpa state). Contoh aliran: `x = 9 + ((u*speed + i*9) % 36)`.
- `spec(sid)` mengisi storyboard **dan** SFX: `dict(goal, obj, anim=[(t_rel, teks)], text, sfx=[(t_rel, key, durasi, dB, fungsi)], qa)`. Pakai `r(sid, 'Lxx', f)` untuk t relatif shot.

### Pose tersedia
| Pose | Jenis | Lip sync | Cocok untuk |
|---|---|---|---|
| wave | setengah badan | ya | sapaan, end card, soft sell |
| thumbs_up | setengah badan | ya | tips, setuju |
| point_up | setengah badan | ya | menjelaskan, "nah" |
| hands_on_hips | setengah badan | ya | percaya diri, rangkuman |
| phone | setengah badan | ya | lihat app/harga |
| shy_lean | setengah badan | ya (mulut miring) | punchline manis (pakai `SMILE`) |
| desk | di meja + monitor | ya (kecil) | kerja/komputasi |
| hands_face | setengah badan | tidak | malu/kaget (tanpa dialog) |
| back, side_left, side_right | setengah badan | tidak | transisi tanpa dialog |
| bust | close-up tangan bersilang | ya | penekanan |
| arms34, point, down | badan sampai paha | ya | analitis, menunjuk penonton, netral |
| think | badan sampai paha | tidak | bingung (dialog sebaiknya pendek) |

### SFX tersedia (`engine/sfx.py`)
`pop, pop_hi, ding, chime, buzz, whoosh, coin, coins, kaching, snip, snips, click, clicks, tick, sparkle, boing, clunk, hum, blip, scratch, stack, jingle, stinger, swipe`
Level tipikal: pop −16 dB, ding/chime −14…−16, whoosh −18, hum −24, stinger end card −12.
Wajib minimal: pop/ding saat elemen penting muncul, jingle saat logo Sakelar, stinger di end card.

---

## Isi kit
```
run.py                 pipeline (check / stage1 / stage2)
WORKFLOW.md            file ini
PROMPT_TERJADWAL.md    prompt sekali jalan untuk tugas terjadwal
engine/reina.py        engine render + helper gambar + timeline + lip sync
engine/sfx.py          efek suara sintetis
engine/docs.py         generator storyboard .md & prompt VO .md
episodes/ep06.py       contoh episode lengkap (template)
assets/poses/          pose Reina (PNG transparan) + poses.json (lebar, titik mulut)
assets/mouth_patches/  potongan area mulut yang sudah di-inpaint (untuk lip sync)
assets/sprites/        sprite mulut (+ mata/efek, tidak dipakai di wajah)
assets/bg/office.png   latar kantor
assets/brand/          logo Sakelar (gelap/putih)
assets/fonts/          Poppins (SIL OFL)
```

---

## Log episode
| Ep | Judul / topik | Status |
|---|---|---|
| 03 | Halusinasi AI | selesai (tema pixel) |
| 04 | AI gratis vs berbayar, langganan vs token API | selesai (tema pixel) |
| 05 | Context window — kenapa AI bisa "lupa" | selesai (tema pixel) |
| 06 | Token itu apa sih? | selesai (tema clean, tanpa SFX) |

### Backlog topik
- Kenapa jawaban AI beda-beda padahal pertanyaannya sama? (temperature/acak)
- Prompt yang bagus itu kayak gimana?
- AI bisa baca data aku nggak sih? (privasi — hati-hati klaim)
- Model AI kecil vs besar, mana yang lebih bagus?
- AI agent vs chatbot biasa
- AI "baca dokumen" kita (RAG) dengan bahasa awam
- API key itu apa & kenapa harus dijaga
- Open-source vs model tertutup
- AI multimodal: bisa lihat gambar & dengar suara
- Kenapa AI kadang nolak permintaan?
- Knowledge cutoff: kenapa AI nggak tahu berita terbaru
