# Vercel Deploy Fix - 4 Ürün

## Sorun
4 ürün Vercel Deployment Protection nedeniyle HTTP 401 veriyor:
- dataflip
- http-pulse
- regex-tester-pro
- webhook-tester

## Çözüm

Her ürünün vercel.json dosyasında `deploymentProtection.enabled: false` ayarı yapıldı.

### Manuel Deploy Adımları:

```bash
# 1. Repo'ya git
cd /home/gokhan/UniverseCreator

# 2. Vercel login (tarayıcıda auth)
vercel login

# 3. Her ürünü deploy et
cd products/dataflip && vercel --yes --prod
cd ../http-pulse && vercel --yes --prod
cd ../regex-tester-pro && vercel --yes --prod
cd ../webhook-tester && vercel --yes --prod

# 4. Health check
for url in \
  https://dataflip-43r9mku65-madnessqws-projects.vercel.app/api/health \
  https://http-pulse-beta.vercel.app/api/health \
  https://regex-tester-kab15rjzb-madnessqws-projects.vercel.app/api/health \
  https://webhook-tester-51g3opoo0-madnessqws-projects.vercel.app/api/health; do
  echo "Testing $url"
  curl -sf "$url" -o /dev/null -w "%{http_code}\n"
done
```

## Alternative: Vercel Dashboard
1. https://vercel.com/dashboard git
2. Her projeyi seç
3. Settings → Deployment Protection
4. "Disable" seç
5. Re-deploy tetikle (git push ile)
