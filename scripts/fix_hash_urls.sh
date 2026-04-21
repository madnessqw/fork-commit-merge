#!/bin/bash
# Hash URL'li ürünler için alias ayarlama scripti
# Vercel auth tamamlandıktan sonra çalıştır

echo "=== HASH URL ALIAS AYARLAMA ==="

# pdf-forge
echo "pdf-forge alias ayarlanıyor..."
env -u VERCEL_TOKEN vercel alias set https://pdf-forge-7lpqmc4pl-madnessqws-projects.vercel.app https://pdf-forge.vercel.app --yes || true

# diffmaster
echo "diffmaster alias ayarlanıyor..."
env -u VERCEL_TOKEN vercel alias set https://diffmaster-neoexql9p-madnessqws-projects.vercel.app https://diffmaster.vercel.app --yes || true

# secretguard
echo "secretguard alias ayarlanıyor..."
env -u VERCEL_TOKEN vercel alias set https://secretguard-cbg7x1j1t-madnessqws-projects.vercel.app https://secretguard.vercel.app --yes || true

echo "=== ALIAS AYARLAMA TAMAMLANDI ==="
