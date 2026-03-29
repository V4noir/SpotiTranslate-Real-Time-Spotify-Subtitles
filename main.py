import requests
import spotipy
from deep_translator import GoogleTranslator
import customtkinter
import json
import os


client_id = ""
secret_id= ""
redirect_url=""

scope="user-read-currently-playing"

CONFIG_FILE = "config.json"

def ayarları_yukle():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def ayarları_kaydet(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)


sarki_cumleler=[]
sarki_rehber = {}
sarki_rehber_tr = {}
yeni_sarki = "Vanoir"
eski_soz = "Vanoir"
spoti = None



def sarkiGetir(sarki_adi,sarkici,sarki_album,toplam_sure):
    print("sarki degisti")
    girdiler={
    "track_name":sarki_adi,
    "artist_name":sarkici,
    "album_name":sarki_album,
    "duration":toplam_sure
}
    global yeni_sarki 
    yeni_sarki=sarki_adi
    istekLink="https://lrclib.net/api/get"
    cumle=requests.get(istekLink,params=girdiler)
    sarkı_sozler=cumle.json()

    if "syncedLyrics" not in sarkı_sozler or sarkı_sozler["syncedLyrics"] is None:
        print("Sözler bulunamadı.")
        sarki_rehber.clear()
        sarki_rehber_tr.clear()
        return
    sarki_cumleler=sarkı_sozler["syncedLyrics"].strip().split("\n")
    
    zamanlamalar_tr=[]
    sozler_liste_ceviri=[]
    for cumle in sarki_cumleler:
        if "]" in cumle:
            saniye=0
            zaman=cumle.split("]")
            zaman[0]=zaman[0].replace("[","")
            
            soz=zaman[1]
            sozler_liste_ceviri.append(zaman[1])
            saniyeList=zaman[0].split(":")
            try:
                saniye=(float(saniyeList[0])*60)+float(saniyeList[1])
                zamanlamalar_tr.append(saniye)
                sarki_rehber[saniye]=soz
            except(ValueError, IndexError):
                print("Bozuk satır atlandı:")
    ceviri="\n".join(sozler_liste_ceviri)
    translated = GoogleTranslator(source='auto', target='tr').translate(ceviri)
    sarkiListTR=translated.split("\n")
    i=0
    for trCumle in sarkiListTR:
        sarki_rehber_tr[zamanlamalar_tr[i]]=trCumle
        i=i+1
        
    
        
        



class SubtitleApp(customtkinter.CTk):
    def __init__(self,ayarlar):
        super().__init__()
        self.ayarlar=ayarlar
        try:
            secili_font = int(self.ayarlar.get("font_size", 50))
            y_offset = int(self.ayarlar.get("y_offset", 100))
        except:
            secili_font = 50
            y_offset = 100
        ekran_genislik = self.winfo_screenwidth()
        ekran_yukseklik = self.winfo_screenheight()

        pencere_genislik = 1800
        pencere_yukseklik = 400

        x_konum = int((ekran_genislik - pencere_genislik) / 2)
        y_konum = ekran_yukseklik - pencere_yukseklik -y_offset 

        self.geometry(f"{pencere_genislik}x{pencere_yukseklik}+{x_konum}+{y_konum}")

        self.title("Spoti Translate")
        self.attributes("-topmost", True)
        self.config(bg='black')
        
        self.overrideredirect(True)

        self.configure(fg_color="black")
        self.attributes("-transparentcolor", "black")

        self.label_en = customtkinter.CTkLabel(self, text="Spotify Bekleniyor...", font=("Helvetica", secili_font, "bold"),text_color="#ffffff", wraplength=1500)
        self.label_en.pack(pady=(40, 10))
        self.label_tr = customtkinter.CTkLabel(self, text="", font=("Helvetica", secili_font, "bold"), text_color="#9EBBCE", wraplength=1500)
        self.label_tr.pack(pady=10)

            
        self.spotify_kontrol()

        # add methods to app
    def spotify_kontrol(self):
        global eski_soz
        aktif_soz=""
        aktif_soz_tr=""
        gelen_veri=spoti.currently_playing()
        eski_sarki=gelen_veri["item"]["name"]
        if gelen_veri and gelen_veri.get("is_playing"):
            saniye=float(gelen_veri["progress_ms"])/1000
            if eski_sarki==yeni_sarki:
                for s in sarki_rehber:
                    if saniye>float(s):
                        aktif_soz=sarki_rehber[s]
                        aktif_soz_tr=sarki_rehber_tr.get(s,"")
                    else:
                        break
                if aktif_soz != eski_soz:
                    print()

                    print(aktif_soz)
                    print(aktif_soz_tr)
                    self.label_tr.configure(text=aktif_soz_tr)
                    self.label_en.configure(text=aktif_soz)
                    eski_soz=aktif_soz
                
            else:
                sarki_rehber.clear()
                sarkiGetir(sarki_adi=eski_sarki,
                    sarkici=gelen_veri["item"]["artists"][0]["name"],
                    sarki_album=gelen_veri["item"]["album"]["name"],
                    toplam_sure=gelen_veri["item"]["duration_ms"] / 1000)
        else:
            print("müzik durdu ya da yok")
        self.after(300, self.spotify_kontrol)


# --- AYARLAR / GİRİŞ EKRANI ---
class ConfigApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Spoti Translate Ayarlar")
        self.geometry("400x550")
        customtkinter.set_appearance_mode("dark")

        # Giriş Alanları
        self.label = customtkinter.CTkLabel(self, text="Spotify API Ayarları", font=("Helvetica", 20, "bold"))
        self.label.pack(pady=20)

        self.entry_client_id = customtkinter.CTkEntry(self, placeholder_text="Client ID", width=300)
        self.entry_client_id.pack(pady=10)

        self.entry_secret_id = customtkinter.CTkEntry(self, placeholder_text="Secret ID", width=300, show="*")
        self.entry_secret_id.pack(pady=10)

        self.label_url = customtkinter.CTkLabel(self, text="Redirect URL (Dashboard ile aynı olmalı)", font=("Helvetica", 12))
        self.label_url.pack(pady=(5, 0))
        self.entry_redirect_url = customtkinter.CTkEntry(self, placeholder_text="Redirect URL", width=350)
        self.entry_redirect_url.pack(pady=10)
        

        self.label_ui = customtkinter.CTkLabel(self, text="Görünüm Ayarları", font=("Helvetica", 16, "bold"))
        self.label_ui.pack(pady=20)

        self.entry_font_size = customtkinter.CTkEntry(self, placeholder_text="Yazı Boyutu (örn: 45)", width=300)
        self.entry_font_size.pack(pady=10)

        self.entry_y_offset = customtkinter.CTkEntry(self, placeholder_text="Yükseklik Payı (örn: 100)", width=300)
        self.entry_y_offset.pack(pady=10)

        self.btn_kaydet = customtkinter.CTkButton(self, text="Kaydet ve Başlat", command=self.baslat)
        self.btn_kaydet.pack(pady=30)

        # Mevcut ayarları yükle
        mevcut = ayarları_yukle()
        if mevcut:
            self.entry_client_id.insert(0, mevcut.get("client_id", ""))
            self.entry_secret_id.insert(0, mevcut.get("secret_id", ""))
            self.entry_font_size.insert(0, mevcut.get("font_size", "45"))
            self.entry_y_offset.insert(0, mevcut.get("y_offset", "100"))
            self.entry_redirect_url.insert(0, mevcut.get("redirect_url", "http://127.0.0.1:8888/callback"))

    def baslat(self):
        data = {
            "client_id": self.entry_client_id.get(),
            "secret_id": self.entry_secret_id.get(),
            "font_size": self.entry_font_size.get(),
            "redirect_url": self.entry_redirect_url.get(),
            "y_offset": self.entry_y_offset.get()
        }
        ayarları_kaydet(data)
        self.destroy() # Ayar penceresini kapat

# --- PROGRAM AKIŞI ---
if __name__ == "__main__":
    # Önce ayar penceresini aç
    config_penceresi = ConfigApp()
    config_penceresi.mainloop()

    # Ayarlar kaydedildikten sonra devam et
    ayarlar = ayarları_yukle()
    if ayarlar:
        # Spotify Bağlantısını Kur
        scope = "user-read-currently-playing"
        sp_oauth = spotipy.SpotifyOAuth(
            client_id=ayarlar["client_id"],
            client_secret=ayarlar["secret_id"],
            redirect_uri=ayarlar["redirect_url"],
            scope=scope
        )
        spoti = spotipy.Spotify(auth_manager=sp_oauth)

        # Ana Uygulamayı Başlat
        app = SubtitleApp(ayarlar)
        app.mainloop()
  