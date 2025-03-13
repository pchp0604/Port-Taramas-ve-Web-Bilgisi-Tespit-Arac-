# Port Taraması ve Web Bilgisi Tespit Aracı

Bu proje, bir hedef domain üzerinde port taraması yapmak, DNS kayıtlarını sorgulamak, IP adresi tespiti yapmak, Cloudflare ve hosting sağlayıcısı bilgilerini edinmek için kullanılan bir Python aracıdır.

## Özellikler:
- Hedef domain için **port taraması** (1-500 portları)
- **Gerçek IP adresi** tespiti ve **Cloudflare** kontrolü
- **Telnet testi** (Port 25 için)
- **Web teknolojileri tespiti** (API kullanarak)
- **DNS kayıtları sorgulaması**
- **Hosting sağlayıcısı** bilgisi (WHOIS sorgulaması)

## Gereksinimler:
- Python 3.x
- Aşağıdaki Python kütüphaneleri:
  - `socket`
  - `requests`
  - `dns.resolver`
  - `whois`
  - `termcolor`
  - `tqdm`
  - `tabulate`

## Kurulum:
Projeyi kullanmak için öncelikle gerekli kütüphaneleri yüklemeniz gerekir. Aşağıdaki komutu kullanarak kütüphaneleri yükleyebilirsiniz:

```bash
pip install requests dns.resolver whois termcolor tqdm tabulate
