from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def multi_cell_justify(self, w, h, txt):
        paragraphs = txt.strip().split('\n')
        for para in paragraphs:
            if not para.strip():
                self.ln(h)  # Paragraf kosong
                continue
            self.multi_cell(w, h, para, align='J')
            self.ln(h)


def paragraf(pdf : PDF, text: str, width: float, height: float, font_name: str = "DejaVuSans", indent_width: float = 5):
    """
    Fungsi untuk menambahkan paragraf ke PDF dengan perataan justify.
    """
    pdf.set_font(font_name, '', 14)
    words = text.split()
    if not words:
        return
    # print(words)
    # word = ' '.join(words)
    # print(f"Adding paragraph: {word}")
    first_line = ''
    remaining_words = words.copy()
    for word in words:
        first_line_test = ' '.join([first_line, word]) if first_line else word
        if pdf.get_string_width(first_line_test) < width-indent_width:
            first_line = first_line_test
            remaining_words.remove(word)
        else:
            break
    
    pdf.cell(indent_width)  # Tambahkan indentasi untuk baris pertama
    pdf.set_x(pdf.get_x() + indent_width)
    pdf.multi_cell(w=width-indent_width, h=height, text=first_line, align='J')

    if remaining_words:
        remaining_text = ' '.join(remaining_words)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=width, h=height, text=remaining_text, align='J')
        pass

    print("baris pertama", first_line)
    print("sisanya",remaining_words)
    # pdf.cell(10)
    # pdf.multi_cell(w=width, h=height, text=text, align='J')
    pdf.ln(height)

def paragraf(pdf : PDF, text: str, width: float, height: float, font_name: str = "DejaVuSans", indent_width: float = 5):
    """
    Fungsi untuk menambahkan paragraf ke PDF dengan perataan justify.
    """
    pdf.set_font(font_name, '', 14)
    
    pdf.multi_cell(w=width, h=height, text=text, align='J')
    # pdf.multi_cell(w=width, h=height, text=text, align='J')
    pdf.ln(height)



def title(pdf: PDF, text: str, font_name: str = "DejaVuSans", font_size: int = 20):
    """
    Fungsi untuk menambahkan judul ke PDF.
    """
    text = text.replace("/h1", "", 1).strip()
    pdf.set_font(font_name, 'B', font_size)
    pdf.cell(0, 10, text, ln=1, align='C')
    pdf.ln(10)

def img(pdf: PDF, image_path: str, width: float = 210, height: float = 0):
    """
    Fungsi untuk menambahkan gambar ke PDF.
    """
    if not os.path.exists(image_path):
        print(f"Gambar {image_path} tidak ditemukan.")
        return
    pdf.add_page()
    pdf.image(image_path, w=width, h=0, x=0, y=0)
    pdf.ln(10)  # Tambahkan jarak setelah gambar

def file_to_pdf(file_path: str, pdf: PDF, font_name: str = "DejaVuSans", width: float = 190, height: float = 8):
    """
    Fungsi untuk membaca file teks dan menambahkannya ke PDF.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} tidak ditemukan.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    if not lines[0].startswith("/img"):
        pdf.add_page()

    prev_img = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("/h1"):
            title(pdf=pdf, text=line, font_name=font_name)
            prev_img = False
        elif line.startswith("/img"):
            image_path = line.replace("/img", "", 1).strip()
            # img(pdf=pdf, image_path=image_path)
            if os.path.exists(image_path):
                img(pdf=pdf, image_path=image_path)
                prev_img = True
            else:
                print(f"Gambar {image_path} tidak ditemukan.")
                prev_img = False
            pass
        else:
            if prev_img:
                pdf.add_page()
            paragraf(pdf=pdf, text=line, width=width, height=8, font_name=font_name)



def main_v2(src: str = "src"):
    LEFT_MARGIN = 20
    RIGHT_MARGIN = 20
    TOP_MARGIN = 20
    BOTTOM_MARGIN = 20
    PAGE_WIDTH = 210  # A4 mm
    CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

    FONT_NAME = "DejaVuSans"
    FONT_FILE = "public/font/DejaVu/DejaVuSans.ttf"
    FONT_BOLD = "public/font/DejaVu/DejaVuSans-Bold.ttf"
    
    # with open('src/01.pytex', "r", encoding="utf-8") as file:
    #     data = file.readlines()

    pdf = PDF('P', 'mm', 'A4')
    pdf.set_auto_page_break(auto=True, margin=BOTTOM_MARGIN)
    pdf.set_margins(LEFT_MARGIN, TOP_MARGIN, RIGHT_MARGIN)

    pdf.add_font(FONT_NAME, "", FONT_FILE)
    pdf.add_font(FONT_NAME, "B", FONT_BOLD)

    list_file = get_list_file(folder_name=src)
    if not list_file:
        print("Tidak ada file yang ditemukan di folder 'src'.")
        return
    
    for file_name in list_file:
        file_path = os.path.join('src', file_name)
        if not os.path.isfile(file_path):
            print(f"File {file_path} tidak ditemukan.")
            continue
        print(f"Processing file: {file_path}")

        file_to_pdf(file_path=file_path, pdf=pdf, font_name=FONT_NAME, width=CONTENT_WIDTH, height=8)
    output_file = 'output1234.pdf'
    pdf.output(output_file)

def get_list_file(folder_name: str = "src"):
    import os

    arr = []
    try:
        files = os.listdir(folder_name)
        for file in files:
            if os.path.isfile(os.path.join(folder_name, file)):
                arr.append(file)
    except FileNotFoundError:
        print(f"Folder '{folder_name}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    if not arr:
        return
    return arr






if __name__ == "__main__":
    main_v2(src="src")
    pass
