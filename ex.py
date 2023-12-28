import PyPDF2
import io
from PIL import Image
import os


def extract_images(pdf_path, output_folder):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    pdf_output_folder = os.path.join(output_folder, pdf_name)
    if not os.path.exists(pdf_output_folder):
        os.makedirs(pdf_output_folder)

    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            
            if '/Resources' in page and '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
             
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        image = xObject[obj]
                        
                        img_data = image._data

                        try:
                            
                            img = Image.open(io.BytesIO(img_data))

                            img = img.convert('RGB')
                            
                            img_name = f"{pdf_name}_page{page_num + 1}_{obj[1:]}.png"
                            img_path = os.path.join(pdf_output_folder, img_name)
                            img.save(img_path, 'PNG')

                            print(f"Extracted: {img_name} from {pdf_name}")
                        except Exception as e:
                            print(f"Error extracting image from {pdf_name}, page {page_num + 1}, object {obj}: {e}")
            else:
                print(f"Page {page_num + 1} in {pdf_name} does not contain '/Resources' or '/XObject', skipping.")


def batch_extract_images(pdf_folder, output_folder):
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            extract_images(pdf_path, output_folder)


if __name__ == "__main__":
    pdf_folder = r"E:\edge_download\bighw\bighw\codes\100_PDF"  # 替换成包含多个 PDF 文件的文件夹路径
    output_folder = "output"  # 图像输出文件夹

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    batch_extract_images(pdf_folder, output_folder)
