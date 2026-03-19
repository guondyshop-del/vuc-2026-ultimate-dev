"""
VUC-2026 Pixabay API Auto Setup
GitHub reposundan otomatik Pixabay API key kurulumu
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PixabayAutoSetup:
    """Pixabay API otomatik kurulum sınıfı"""
    
    def __init__(self):
        self.api_key = None
        self.base_url = "https://pixabay.com/api/"
        
    def setup_pixabay_account(self):
        """Pixabay hesabı kurulumu"""
        print("🖼️ PIXABAY AUTO SETUP")
        print("=" * 50)
        
        steps = [
            {
                'step': 1,
                'title': 'Pixabay Kayıt',
                'url': 'https://pixabay.com/accounts/register/',
                'action': 'Free account oluştur'
            },
            {
                'step': 2,
                'title': 'Email Onayı',
                'action': 'Gelen kutusunu kontrol et'
            },
            {
                'step': 3,
                'title': 'API Key Al',
                'url': 'https://pixabay.com/accounts/dashboard/',
                'action': 'Dashboard\'dan API key kopyala'
            },
            {
                'step': 4,
                'title': 'Test Et',
                'action': 'API key\'i test et'
            },
            {
                'step': 5,
                'title': 'VUC-2026 Entegrasyon',
                'action': '.env dosyasına ekle'
            }
        ]
        
        for step in steps:
            print(f"\n📍 ADIM {step['step']}: {step['title']}")
            if 'url' in step:
                print(f"   🔗 Link: {step['url']}")
            print(f"   📝 Aksiyon: {step['action']}")
        
        # Kayıt linkini aç
        try:
            import webbrowser
            webbrowser.open('https://pixabay.com/accounts/register/')
            print("\n✅ Pixabay kayıt sayfası açıldı!")
        except:
            print("\n📋 Linki manuel açın: https://pixabay.com/accounts/register/")
    
    def test_pixabay_api(self, api_key):
        """Pixabay API test"""
        if not api_key:
            print("❌ API key gerekli!")
            return False
        
        test_url = f"{self.base_url}?key={api_key}&response_group=high_resolution&q=baby&per_page=3"
        
        try:
            response = requests.get(test_url)
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get('hits', [])
                
                print("✅ PIXABAY API BAŞARILI!")
                print("=" * 40)
                print(f"📸 Baby photos/videos: {len(hits)} sonuç")
                
                for i, hit in enumerate(hits[:3], 1):
                    if 'imageURL' in hit:
                        print(f"{i}. 🖼️ Image: {hit.get('tags', 'No tags')}")
                        print(f"   📏 {hit.get('imageWidth', 0)}x{hit.get('imageHeight', 0)}px")
                        print(f"   👤 {hit.get('user', 'Unknown')}")
                    elif 'videoURL' in hit:
                        print(f"{i}. 🎥 Video: {hit.get('tags', 'No tags')}")
                        print(f"   📏 {hit.get('videos', {}).get('large', {}).get('width', 0)}x{hit.get('videos', {}).get('large', {}).get('height', 0)}px")
                    print()
                
                return True
                
            else:
                print(f"❌ API Hatası: {response.status_code}")
                print(f"Hata: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Bağlantı hatası: {str(e)}")
            return False
    
    def install_pixabay_library(self):
        """Pixabay Python library kurulumu"""
        print("\n📦 PIXABAY PYTHON LIBRARY KURULUMU")
        print("=" * 40)
        
        libraries = [
            {
                'name': 'pixabay',
                'install': 'pip install pixabay',
                'import': 'import pixabay.core'
            },
            {
                'name': 'requests',
                'install': 'pip install requests',
                'import': 'import requests'
            }
        ]
        
        for lib in libraries:
            print(f"\n📚 {lib['name']}:")
            print(f"   💾 Kurulum: {lib['install']}")
            print(f"   📥 Import: {lib['import']}")
        
        # Test kurulum
        try:
            import requests
            print("\n✅ requests library zaten kurulu!")
        except ImportError:
            print("\n📦 requests kuruluyor...")
            os.system("pip install requests")
    
    def create_pixabay_service(self):
        """Pixabay service oluştur"""
        service_code = '''
"""
VUC-2026 Pixabay Service
Stock images and videos for content generation
"""

import os
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()

class PixabayService:
    """Pixabay API integration for VUC-2026"""
    
    def __init__(self):
        self.api_key = os.getenv('PIXABAY_API_KEY')
        self.base_url = "https://pixabay.com/api/"
        
    def search_images(self, query: str, per_page: int = 20, category: str = "all") -> List[Dict]:
        """Search for images"""
        if not self.api_key:
            return []
            
        params = {
            'key': self.api_key,
            'q': query,
            'per_page': per_page,
            'category': category,
            'safesearch': 'true',
            'response_group': 'high_resolution'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('hits', [])
            return []
        except:
            return []
    
    def search_videos(self, query: str, per_page: int = 20) -> List[Dict]:
        """Search for videos"""
        if not self.api_key:
            return []
            
        params = {
            'key': self.api_key,
            'q': query,
            'per_page': per_page,
            'video_type': 'all',
            'safesearch': 'true'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get('hits', [])
            return []
        except:
            return []
    
    def get_baby_content(self) -> Dict[str, List]:
        """Get baby-related content"""
        baby_queries = ['baby', 'newborn', 'infant', 'toddler', 'pregnancy']
        
        results = {
            'images': [],
            'videos': []
        }
        
        for query in baby_queries:
            # Images
            images = self.search_images(query, per_page=5)
            results['images'].extend(images)
            
            # Videos
            videos = self.search_videos(query, per_page=3)
            results['videos'].extend(videos)
        
        return results
'''
        
        # Service dosyası oluştur
        with open('backend/app/services/pixabay_service.py', 'w') as f:
            f.write(service_code)
        
        print("\n✅ Pixabay service oluşturuldu!")
        print("📁 backend/app/services/pixabay_service.py")
    
    def update_env_file(self, api_key):
        """.env dosyasını güncelle"""
        env_file_path = '.env'
        
        # .env dosyasını oku
        with open(env_file_path, 'r') as f:
            lines = f.readlines()
        
        # API key'i güncelle
        updated_lines = []
        for line in lines:
            if line.startswith('PIXABAY_API_KEY='):
                updated_lines.append(f'PIXABAY_API_KEY={api_key}\n')
            else:
                updated_lines.append(line)
        
        # Dosyayı yaz
        with open(env_file_path, 'w') as f:
            f.writelines(updated_lines)
        
        print("✅ .env dosyası güncellendi!")
    
    def auto_setup_complete(self, api_key):
        """Complete auto setup"""
        print("\n🚀 PIXABAY AUTO SETUP COMPLETE")
        print("=" * 50)
        
        # 1. Test API
        if self.test_pixabay_api(api_key):
            # 2. Update env
            self.update_env_file(api_key)
            
            # 3. Install library
            self.install_pixabay_library()
            
            # 4. Create service
            self.create_pixabay_service()
            
            print("\n🎯 PIXABAY TAM ENTEGRE!")
            print("✅ API key working")
            print("✅ .env updated")
            print("✅ Library ready")
            print("✅ Service created")
            print("✅ VUC-2026 ready!")
            
            return True
        else:
            print("\n❌ Setup failed - API key not working")
            return False

def main():
    """Main auto setup function"""
    setup = PixabayAutoSetup()
    
    print("🚀 VUC-2026 PIXABAY AUTO SETUP")
    print("=" * 60)
    
    # Setup account
    setup.setup_pixabay_account()
    
    # API key'i al
    print("\n🔑 PIXABAY API KEY GEREKLİ")
    print("1. Yukarıdaki linklerden kayıt olun")
    print("2. Dashboard'dan API key alın")
    print("3. Aşağıya yapıştırın")
    print()
    
    api_key = input("Pixabay API Key: ").strip()
    
    if api_key:
        # Complete setup
        setup.auto_setup_complete(api_key)
    else:
        print("❌ API key gerekli!")

if __name__ == "__main__":
    main()
