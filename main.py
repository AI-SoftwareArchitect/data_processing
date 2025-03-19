import os
import json
import shutil
import difflib

def is_similar(keyword, annotation, threshold=0.7):

    words = annotation.split()
    for word in words:
        ratio = difflib.SequenceMatcher(None, keyword.lower(), word.lower()).ratio()
        if ratio >= threshold:
            return True
    return False

def load_keywords(keywords_source):
 
    if isinstance(keywords_source, str):
    
        with open(keywords_source, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return keywords
    elif isinstance(keywords_source, list):
        return keywords_source
    else:
        raise ValueError("Keywords source must be a filename or a list of keywords.")

def extract_images_by_keywords(dataset_folder, annotations_file, keywords_source, extracted_folder):

    if not os.path.exists(extracted_folder):
        os.makedirs(extracted_folder)
    
    with open(annotations_file, 'r', encoding='utf-8') as f:
        annotations = json.load(f)

    keywords = load_keywords(keywords_source)
    
    
    total_extracted = 0
    
 
    for keyword in keywords:
        found = False
        for image_file, annotation in annotations.items():
            if is_similar(keyword, annotation):
                src = os.path.join(dataset_folder, image_file)
                # Dosya uzantısını al (örneğin .png, .jpg)
                _, ext = os.path.splitext(image_file)
                new_filename = keyword + ext
                dst = os.path.join(extracted_folder, new_filename)
                
                if os.path.exists(src):
                    shutil.copy(src, dst)
                    print(f"✔️ '{image_file}' dosyası, '{keyword}' olarak kopyalandı.")
                    total_extracted += 1
                    found = True
                    break  
                else:
                    print(f"⚠️ {image_file} dosyası bulunamadı!")
        if not found:
            print(f"❌ '{keyword}' için eşleşme bulunamadı.")
    
    print(f"\nToplamda {total_extracted} adet resim, keyword listesindeki eşleşmelerle extract edildi.")

# Örnek Kullanım:
if __name__ == "__main__":
    # Dataset klasörü ve annotation dosya yolunu belirle
    dataset_folder = "dataset_images"       # Resimlerin bulunduğu klasör
    annotations_file = "annotations.json"     # JSON formatındaki annotation dosyası
    extracted_folder = "extracted"            # Eşleşen resimlerin kopyalanacağı klasör
    

    keywords_source = ["bisiklet", "araba", "uçak", "elma", "köpek"]  # örnek; burada 4000 kelime olabilir.
    
    # Resimleri işle
    extract_images_by_keywords(dataset_folder, annotations_file, keywords_source, extracted_folder)
