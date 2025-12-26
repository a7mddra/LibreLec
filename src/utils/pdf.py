import os
from PIL import Image
from .system import SystemUtils

class PDFMerger:
    @staticmethod
    def merge_to_pdf(image_folder, output_filename):
        """Merges PNGs to PDF."""
        try:
            files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')], 
                           key=lambda x: int(x.split('_')[1].split('.')[0]))
            
            if not files:
                return None

            images = [Image.open(os.path.join(image_folder, f)).convert('RGB') for f in files]
            
            docs_path = SystemUtils.get_documents_path()
            output_path = docs_path / f"{output_filename}.pdf"
            
            images[0].save(output_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
            return output_path
        except Exception as e:
            print(f"Merge error: {e}")
            return None
