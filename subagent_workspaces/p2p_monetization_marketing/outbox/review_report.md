QA REVIEW: FAIL

Hangi dosya/satırda sorun var? 
- `marketing_copy.md` içindeki `{{FirstName}}` yer tutucusu.
- `p2p_distributor.py` içindeki formatlama işlemi.

Hata ne?
Script çalışıyor ve crash olmuyor (Exit 0). Ancak `marketing_copy.md` içindeki template `{{FirstName}}` kullandığı için Python'ın `.format()` metodu bunu kaçış karakteri olarak algılayıp doğrudan `{FirstName}` olarak basıyor. Tüm mailler kişiselleştirme olmadan "Hi {FirstName}," olarak oluşturuluyor. Ayrıca compliance (PayPal/Akbank) açısından sorun yok, sadece P2P self-hosted servis olarak sunulduğu için kurallara uyuyor.

Çözüm Önerisi:
`marketing_copy.md` içindeki `{{FirstName}}` ifadesini, scriptin içindeki lead yapısına uygun olarak `{name}` olarak değiştirin veya scriptin formatlama mantığını güncelleyin.
