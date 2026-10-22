# REINA EXPLAINS AI — Kit Produksi (tema clean)

Satu zip berisi semuanya: aset Reina, latar kantor, logo, font, engine render, efek suara, generator storyboard & prompt VO,
dan contoh episode lengkap (Ep06).

- **Mulai dari sini:** `WORKFLOW.md` (alur, aturan, panduan naskah, daftar pose & SFX, log episode).
- **Tugas terjadwal:** `PROMPT_TERJADWAL.md` (prompt sekali jalan).
- **Perintah:**
  ```
  python run.py check  episodes/epXX.py
  python run.py stage1 episodes/epXX.py              # storyboard + gambar scene + prompt VO (dikirim sekaligus)
  python run.py stage2 episodes/epXX.py suara.zip    # video final + SFX
  ```
Butuh Python 3 (`numpy`, `pillow`) dan `ffmpeg`.
