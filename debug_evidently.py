import sys
import os

print("--- PYTHON ORTAMI ---")
print(f"Python Yolu: {sys.executable}")
print(f"Çalışma Dizini: {os.getcwd()}")

print("\n--- KÜTÜPHANE KONTROLÜ ---")
try:
    import evidently
    print("✅ 'import evidently' BAŞARILI")
    print(f"Versiyon: {evidently.__version__}")
    print(f"Dosya Konumu: {evidently.__file__}")
    
    print("\n--- ALT MODÜL KONTROLÜ ---")
    try:
        from evidently import report
        print("✅ 'from evidently import report' BAŞARILI")
    except ImportError as e:
        print(f"❌ 'report' modülü yüklenemedi: {e}")
        print("Evidently içindeki mevcut modüller:")
        print(dir(evidently))

except ImportError as e:
    print(f"❌ 'evidently' hiç yüklenemedi: {e}")
    print("Sanal ortamda olduğundan emin ol.")

print("\n--- SİSTEM YOLLARI (SYS.PATH) ---")
for p in sys.path:
    print(p)