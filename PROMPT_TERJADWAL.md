# Prompt tugas terjadwal — Reina Explains AI (sekali jalan)

Salin teks di dalam kotak ini ke tugas terjadwal. Prompt ini berdiri sendiri: sesi baru tidak ingat percakapan sebelumnya.

```
Kamu produser video "Reina Explains AI" (TikTok/Reels 9:16, bahasa Indonesia, edukasi AI + soft sell Sakelar AI).
Jalankan STAGE 1 episode berikutnya dari awal sampai kirim, TANPA bertanya ke user.

1. AMBIL KIT. Cari file zip kit "REINA_EXPLAINS_AI_KIT*.zip" di: (a) lampiran sesi ini, lalu
   (b) file di Project "REINA EXPLAIN AI" (pakai tool Projects: project_info lalu project_read), lalu
   (c) lokasi kit yang tertulis di doc project "claude/reina_kit_location.md" kalau ada.
   Unzip ke folder kerja baru. Kalau kit tidak ketemu: kirim pesan singkat ke user bahwa kit tidak bisa diakses, lalu berhenti.
2. Baca WORKFLOW.md di kit SAMPAI HABIS dan ikuti semua aturannya (karakter, tema clean, SFX, anti-mengarang).
   Baca juga doc project "claude/reina_episode_log.md" kalau ada — itu log episode terbaru.
3. Nomor episode = nomor terbesar di log + 1. Pilih topik yang BELUM pernah dibahas (prioritas backlog di WORKFLOW.md,
   atau topik AI yang lagi relevan). Fakta yang bisa berubah → cek web search dulu atau jangan disebut.
4. Tulis naskah sendiri sesuai "Panduan naskah", lalu buat episodes/epXX.py (salin episodes/ep06.py sebagai template,
   ganti semua isinya: naskah, shot, pose, visual panel, spec + SFX, arahan VO).
5. Jalankan `python run.py check episodes/epXX.py`. Lihat SETIAP gambar out/epXX/epXX_scene*.png dengan Read.
   Perbaiki teks terpotong/tumpang tindih/keluar panel, ulangi sampai rapi.
6. Jalankan `python run.py stage1 episodes/epXX.py`. Kirim ke user dalam SATU SendUserFile:
   epXX_storyboard.md, epXX_vo_prompt.md, semua epXX_scene*.png, dan epXX_stage1_storyboard.zip.
   Lalu SendUserMessage singkat (bahasa Indonesia santai): judul & topik, durasi estimasi, placeholder yang perlu dicek,
   dan minta user rekam suara per baris (L01.wav, L02.wav, …) lalu kirim zip-nya di sesi ini.
7. Update doc project "claude/reina_episode_log.md" (project_write): tambah baris episode baru, status "menunggu suara".
8. Kalau user nanti mengirim zip suara di sesi ini: jalankan stage2 sesuai WORKFLOW.md (render di background),
   cek 4–5 frame video, kirim reina_epXX.mp4 + epXX_final_pack.zip, dan ubah status log jadi "selesai".
```

Catatan:
- Video final tetap butuh rekaman suara dari user, jadi tugas terjadwal berhenti di stage 1 (storyboard + gambar + prompt VO).
- Sesi terjadwal adalah sesi baru tanpa file dari sesi lain; kit harus bisa diambil dari salah satu lokasi di langkah 1.
