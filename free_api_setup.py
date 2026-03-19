"""
VUC-2026 Free API Key Setup Guide
Pixabay ve Pexels için ücretsiz API key alma
"""

import webbrowser

class FreeAPIKeySetup:
    """Ücretsiz API key kurulum rehberi"""
    
    def __init__(self):
        self.api_setup_urls = {
            'pixabay': {
                'signup': 'https://pixabay.com/accounts/register/',
                'api_docs': 'https://pixabay.com/api/docs/',
                'dashboard': 'https://pixabay.com/accounts/dashboard/',
                'purpose': 'Stock videos, images, thumbnails'
            },
            'pexels': {
                'signup': 'https://www.pexels.com/join/',
                'api_docs': 'https://www.pexels.com/api/',
                'dashboard': 'https://www.pexels.com/dashboard/',
                'purpose': 'Stock photos, high-quality images'
            }
        }
    
    def setup_pixabay(self):
        """Pixabay API key kurulumu"""
        print("🖼️ PIXABAY API KEY KURULUMU")
        print("=" * 50)
        
        steps = [
            {
                'step': 1,
                'title': 'Kayıt Ol',
                'action': 'https://pixabay.com/accounts/register/',
                'details': 'Free account - Email ile kayıt'
            },
            {
                'step': 2,
                'title': 'Email Onayı',
                'action': 'Emaildeki confirmation link',
                'details': 'Gelen kutusunu kontrol et'
            },
            {
                'step': 3,
                'title': 'Dashboard Git',
                'action': 'https://pixabay.com/accounts/dashboard/',
                'details': 'API Key bölümünü bul'
            },
            {
                'step': 4,
                'title': 'API Key Kopyala',
                'action': 'Copy API Key',
                'details': 'Key format: xxxxxx-xxxxxx-xxxxxx'
            },
            {
                'step': 5,
                'title': 'VUC-2026 Ekle',
                'action': '.env dosyasına ekle',
                'details': 'PIXABAY_API_KEY=your_key_here'
            }
        ]
        
        for step in steps:
            print(f"\n📍 ADIM {step['step']}: {step['title']}")
            print(f"   🔗 Link: {step['action']}")
            print(f"   📝 Detay: {step['details']}")
        
        # Pixabay dashboard aç
        print(f"\n🌐 PIXABAY DASHBOARD:")
        print(f"   {self.api_setup_urls['pixabay']['dashboard']}")
        
        return self.api_setup_urls['pixabay']
    
    def setup_pexels(self):
        """Pexels API key kurulumu"""
        print("\n📸 PEXELS API KEY KURULUMU")
        print("=" * 50)
        
        steps = [
            {
                'step': 1,
                'title': 'Kayıt Ol',
                'action': 'https://www.pexels.com/join/',
                'details': 'Free account - Email ile kayıt'
            },
            {
                'step': 2,
                'title': 'Email Onayı',
                'action': 'Emaildeki confirmation link',
                'details': 'Gelen kutusunu kontrol et'
            },
            {
                'step': 3,
                'title': 'Dashboard Git',
                'action': 'https://www.pexels.com/dashboard/',
                'details': 'Your API Key bölümünü bul'
            },
            {
                'step': 4,
                'title': 'API Key Kopyala',
                'action': 'Copy API Key',
                'details': 'Key format: xxxxxxxxxxxxxxxxxxxx'
            },
            {
                'step': 5,
                'title': 'VUC-2026 Ekle',
                'action': '.env dosyasına ekle',
                'details': 'PEXELS_API_KEY=your_key_here'
            }
        ]
        
        for step in steps:
            print(f"\n📍 ADIM {step['step']}: {step['title']}")
            print(f"   🔗 Link: {step['action']}")
            print(f"   📝 Detay: {step['details']}")
        
        # Pexels dashboard aç
        print(f"\n🌐 PEXELS DASHBOARD:")
        print(f"   {self.api_setup_urls['pexels']['dashboard']}")
        
        return self.api_setup_urls['pexels']
    
    def update_env_file(self, pixabay_key=None, pexels_key=None):
        """.env dosyasını güncelle"""
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        env_file_path = '.env'
        
        # .env dosyasını oku
        with open(env_file_path, 'r') as f:
            lines = f.readlines()
        
        # API key'leri güncelle
        updated_lines = []
        for line in lines:
            if line.startswith('PIXABAY_API_KEY=') and pixabay_key:
                updated_lines.append(f'PIXABAY_API_KEY={pixabay_key}\n')
            elif line.startswith('PEXELS_API_KEY=') and pexels_key:
                updated_lines.append(f'PEXELS_API_KEY={pexels_key}\n')
            else:
                updated_lines.append(line)
        
        # Dosyayı yaz
        with open(env_file_path, 'w') as f:
            f.writelines(updated_lines)
        
        print("✅ .env dosyası güncellendi!")
    
    def test_api_keys(self, pixabay_key=None, pexels_key=None):
        """API key'leri test et"""
        print("\n🧪 API KEY TEST")
        print("=" * 30)
        
        if pixabay_key:
            try:
                import requests
                url = f"https://pixabay.com/api/?key={pixabay_key}&q=baby&per_page=3"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Pixabay API: {len(data.get('hits', []))} sonuç bulundu")
                else:
                    print(f"❌ Pixabay API Hatası: {response.status_code}")
            except Exception as e:
                print(f"❌ Pixabay Test Hatası: {str(e)}")
        
        if pexels_key:
            try:
                import requests
                headers = {'Authorization': pexels_key}
                url = "https://api.pexels.com/v1/search?query=baby&per_page=3"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Pexels API: {len(data.get('photos', []))} fotoğraf bulundu")
                else:
                    print(f"❌ Pexels API Hatası: {response.status_code}")
            except Exception as e:
                print(f"❌ Pexels Test Hatası: {str(e)}")

def main():
    """Main setup function"""
    setup = FreeAPIKeySetup()
    
    print("🚀 VUC-2026 ÜCRETSİZ API KEY KURULUM")
    print("=" * 60)
    print("Pixabay ve Pexels için ücretsiz API key'ler")
    print()
    
    # Pixabay kurulum
    pixabay_info = setup.setup_pixabay()
    
    # Pexels kurulum  
    pexels_info = setup.setup_pexels()
    
    print("\n🎯 KURULUM SONRASI ADIMLAR:")
    print("=" * 40)
    print("1. Her iki siteye de kayıt olun")
    print("2. API key'leri kopyalayın")
    print("3. Aşağıdaki formatta .env dosyasına ekleyin:")
    print()
    print("PIXABAY_API_KEY=your_pixabay_key_here")
    print("PEXELS_API_KEY=your_pexels_key_here")
    print()
    print("4. Sistemi yeniden başlatın")
    
    # Dashboard'ları aç
    print("\n🌐 HIZLI ERİŞİM:")
    print(f"📸 Pixabay Dashboard: {pixabay_info['dashboard']}")
    print(f"🖼️ Pexels Dashboard: {pexels_info['dashboard']}")
    
    # Linkleri aç
    try:
        import webbrowser
        webbrowser.open(pixabay_info['signup'])
        webbrowser.open(pexels_info['signup'])
        print("\n✅ Kayıt sayfaları tarayıcıda açıldı!")
    except:
        print("\n📋 Linkleri manuel açın")

if __name__ == "__main__":
    main()
