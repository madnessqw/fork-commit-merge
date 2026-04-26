# Playbook: P2P Invoice Generator API

## Proje Amacı
Bu projenin amacı, kullanıcıların PayPal veya Akbank IBAN bağlantılarını içeren profesyonel faturaları (PDF/HTML formatında) doğrudan oluşturabilmesini sağlayan bir P2P Fatura Oluşturucu API (Python FastAPI) geliştirmektir. 
Önemli olan bu API hizmetinin kendisinin bir "402 Payment Required" kısıtlamasına sahip olmasıdır; kullanıcılar API'yi kullanabilmek için mikro ödeme yapmak veya bir bakiye yüklemek zorundadır.

## Görevler ve DAG (Directed Acyclic Graph)
Bu proje `backend-engineer` ve `frontend-engineer` ajanları arasında paralelleştirilmiştir.

- **[T1] API Temelleri ve Fatura Üretimi (Agent: `backend-engineer`)**
  - FastAPI uygulamasını ayağa kaldır.
  - JSON olarak alınan fatura verilerinden (gönderen, alıcı, kalemler, IBAN/PayPal) HTML/PDF çıktısı oluşturacak motoru yaz.
  - **Durum:** BEKLEMEDE
  - **Bağımlılıklar:** Yok

- **[T2] 402 Payment Required Middleware (Agent: `backend-engineer`)**
  - API uç noktalarına erişimi "402 Payment Required" mantığı ile sınırlandır. Basit bir API kredi/token sistemi entegre et.
  - **Durum:** BEKLEMEDE
  - **Bağımlılıklar:** T1

- **[T3] Kullanıcı Arayüzü / Demo Dashboard (Agent: `frontend-engineer`)**
  - Kullanıcıların fatura bilgilerini girebileceği ve API'yi test edebileceği hafif bir UI (React/Vue/HTML) geliştir.
  - Arayüz, 402 yanıtını algılamalı ve kullanıcıyı API kredisi yükleme / ödeme sayfasına yönlendirmelidir.
  - **Durum:** BEKLEMEDE
  - **Bağımlılıklar:** Yok (T1 ile eşzamanlı başlanabilir, `hive_mind.md` içerisindeki Data Contract mock veriyle UI geliştirmesine olanak tanır).
