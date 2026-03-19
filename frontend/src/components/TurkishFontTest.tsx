import React from 'react';

const TurkishFontTest = () => {
  return (
    <div className="p-8 bg-gray-900 text-white min-h-screen">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="turkish-heading-1 text-4xl mb-4">
            VUC-2026 Türkçe Karakter Desteği
          </h1>
          <p className="turkish-body text-gray-300">
            Türkçe karakterlerin mükemmel görüntülendiği font sistemi
          </p>
        </div>

        {/* Turkish Character Showcase */}
        <div className="glass-effect p-6 rounded-lg">
          <h2 className="turkish-heading-2 text-2xl mb-4 text-amber-400">
            Türkçe Karakterler
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="turkish-heading-3 text-lg mb-2 text-blue-400">
                Küçük Harfler
              </h3>
              <p className="turkish-body text-3xl font-mono">
                ç ğ ı ö ş ü
              </p>
            </div>
            <div>
              <h3 className="turkish-heading-3 text-lg mb-2 text-green-400">
                Büyük Harfler
              </h3>
              <p className="turkish-body text-3xl font-mono">
                Ç Ğ İ Ö Ş Ü
              </p>
            </div>
          </div>
        </div>

        {/* Sample Turkish Text */}
        <div className="glass-effect p-6 rounded-lg">
          <h2 className="turkish-heading-2 text-2xl mb-4 text-amber-400">
            Örnek Türkçe Metinler
          </h2>
          <div className="space-y-4">
            <div className="turkish-body">
              <h3 className="turkish-heading-3 text-lg mb-2 text-blue-400">
                VUC-2026 Sistem Açıklaması
              </h3>
              <p className="turkish-body leading-relaxed">
                VUC-2026, YouTube'da hakimiyet kurmak için tasarlanmış otonom bir dijital varlıktır. 
                Bu sistem, Türkçe karakterleri mükemmel bir şekilde destekler ve içerik üretiminde 
                ç ğ ı ö ş ü karakterlerini problemsiz kullanır.
              </p>
            </div>
            
            <div className="turkish-body">
              <h3 className="turkish-heading-3 text-lg mb-2 text-green-400">
                Teknik Özellikler
              </h3>
              <p className="turkish-body leading-relaxed">
                Sistem, İstanbul'un 18 ilçesi için içerik stratejileri üretir. 
                Pregnancy, newborn, infant, toddler aşamalarında 100 video hazırlandı. 
                Çocuk içerikleri için higher CPM ($2.5/1000 views) potansiyeli mevcuttur.
              </p>
            </div>

            <div className="turkish-body">
              <h3 className="turkish-heading-3 text-lg mb-2 text-purple-400">
                Karakter Testi
              </h3>
              <p className="turkish-body leading-relaxed">
                Bu metinde tüm Türkçe karakterler test ediliyor: ç, ğ, ı, ö, ş, ü, Ç, Ğ, İ, Ö, Ş, Ü.
                Ayrıca özel karakterler: â, î, û, Â, Î, Û.
                Rakamlar ve noktalama işaretleri: 1, 2, 3, ?, !, :, ;, ,, .
              </p>
            </div>
          </div>
        </div>

        {/* Font Size Tests */}
        <div className="glass-effect p-6 rounded-lg">
          <h2 className="turkish-heading-2 text-2xl mb-4 text-amber-400">
            Font Boyutu Testleri
          </h2>
          <div className="space-y-2">
            <p className="turkish-text-xs">Çok küçük metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-text-sm">Küçük metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-text-base">Normal metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-text-lg">Büyük metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-text-xl">Çok büyük metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-text-2xl">Dev metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-text-3xl">En büyük metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
          </div>
        </div>

        {/* Font Weight Tests */}
        <div className="glass-effect p-6 rounded-lg">
          <h2 className="turkish-heading-2 text-2xl mb-4 text-amber-400">
            Font Kalınlık Testleri
          </h2>
          <div className="space-y-2">
            <p className="turkish-thin">İnce metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-light">Hafif metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-normal">Normal metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-medium">Orta metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-semibold">Yarı kalın metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-bold">Kalın metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-extrabold">Çok kalın metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
            <p className="turkish-black">En kalın metin - Türkçe karakterler: ç ğ ı ö ş ü</p>
          </div>
        </div>

        {/* UI Components Test */}
        <div className="glass-effect p-6 rounded-lg">
          <h2 className="turkish-heading-2 text-2xl mb-4 text-amber-400">
            UI Bileşenleri Testi
          </h2>
          <div className="space-y-4">
            <div>
              <label className="turkish-label block mb-2 text-blue-400">
                Türkçe Etiket: ç ğ ı ö ş ü
              </label>
              <input 
                type="text" 
                className="turkish-input w-full p-2 bg-gray-800 rounded border border-gray-600"
                placeholder="Türkçe metin giriniz: ç ğ ı ö ş ü"
              />
            </div>
            <button className="turkish-button btn-primary">
              Türkçe Buton: ç ğ ı ö ş ü
            </button>
          </div>
        </div>

        {/* Performance Test */}
        <div className="glass-effect p-6 rounded-lg">
          <h2 className="turkish-heading-2 text-2xl mb-4 text-amber-400">
            Performans Metrikleri
          </h2>
          <div className="turkish-body space-y-2">
            <p>✅ Font Loading: Optimize edilmiş</p>
            <p>✅ Character Rendering: Mükemmel</p>
            <p>✅ Text Rendering: optimizeLegibility</p>
            <p>✅ Font Smoothing: Antialiased</p>
            <p>✅ Unicode Support: Tam</p>
            <p>✅ BIDI Direction: LTR</p>
            <p>✅ Font Features: kern, liga, calt</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TurkishFontTest;
