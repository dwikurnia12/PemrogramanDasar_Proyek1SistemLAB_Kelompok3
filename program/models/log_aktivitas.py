from datetime import datetime

class LogAktivitas:
    def __init__(self):
        self.logs = []
    def tambah(self, pesan):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.logs.append(f"[{waktu}] {pesan}")
    def tampilkan(self):
        if not self.logs:
            print("Belum ada log aktivitas.")
            return
        print("\n=== LOG AKTIVITAS ===")
        for log in self.logs:
            print(log)