import os, re, sys
from fpdf import FPDF

class ChinesePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.font_path = r"C:\Users\Administrator\Desktop\code\05_ai-foreign-trade-automation\data\simhei.ttf"
        self.add_font("SimHei", "", self.font_path)
        self.add_font("SimHei", "B", self.font_path)
        self.set_auto_page_break(True, 20)
    
    def header(self):
        pass
    
    def footer(self):
        self.set_y(-15)
        self.set_font("SimHei", "", 8)
        self.cell(0, 10, f"{self.page_no()}", align="C")

def clean_bold(text):
    return re.sub(r'\*\*(.+?)\*\*', r'\1', text)

def fix_glyphs(text):
    """Replace characters not available in SimHei font"""
    replacements = {
        '\u00e3': 'a',  # ã -> a (Portuguese)
        '\u00e1': 'a',  # á -> a
        '\u00e9': 'e',  # é -> e
        '\u00ed': 'i',  # í -> i
        '\u00f3': 'o',  # ó -> o
        '\u00fa': 'u',  # ú -> u
        '\u00f1': 'n',  # ñ -> n
        '\u00e7': 'c',  # ç -> c
        '\u00c3': 'A',  # Ã -> A
        '\u00c1': 'A',
        '\u00c9': 'E',
        '\u00cd': 'I',
        '\u00d3': 'O',
        '\u00da': 'U',
        '\u00d1': 'N',
        '\u00c7': 'C',
        '\u015b': 's',  # ś -> s (Polish)
        '\u0142': 'l',  # ł -> l (Polish)
        '\u0105': 'a',  # ą -> a (Polish)
        '\u0119': 'e',  # ę -> e (Polish)
        '\u017c': 'z',  # ż -> z (Polish)
        '\u017a': 'z',  # ź -> z (Polish)
        '\u0107': 'c',  # ć -> c (Polish)
        '\u0144': 'n',  # ń -> n (Polish)
        '\u015a': 'S',  # Ś -> S
        '\u0141': 'L',  # Ł -> L
        '\u0104': 'A',  # Ą -> A
        '\u0118': 'E',  # Ę -> E
        '\u017b': 'Z',  # Ż -> Z
        '\u0179': 'Z',  # Ź -> Z
        '\u0106': 'C',  # Ć -> C
        '\u0143': 'N',  # Ń -> N
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def render_table(pdf, rows):
    if not rows:
        return
    num_cols = max(len(r) for r in rows)
    col_w = 190 / num_cols
    estimated_height = len(rows) * 7 + 10
    if pdf.get_y() + estimated_height > 270:
        pdf.add_page()
    for row_idx, row in enumerate(rows):
        pdf.set_font("SimHei", "B" if row_idx == 0 else "", 8)
        max_lines = 1
        for cell_text in row:
            w = pdf.get_string_width(cell_text)
            max_lines = max(max_lines, max(1, int(w / (col_w - 2) + 0.5)))
        row_h = max_lines * 5 + 2
        if pdf.get_y() + row_h > 270:
            pdf.add_page()
            pdf.set_font("SimHei", "B" if row_idx == 0 else "", 8)
        y_start = pdf.get_y()
        x_vals = [10 + j * col_w for j in range(num_cols)]
        heights = []
        for col_idx, cell_text in enumerate(row):
            pdf.set_xy(x_vals[col_idx] + 1, y_start + 0.5)
            pdf.multi_cell(col_w - 2, 5, cell_text)
            heights.append(pdf.get_y() - y_start)
        actual_h = max(heights)
        for col_idx in range(num_cols):
            pdf.rect(x_vals[col_idx], y_start, col_w, actual_h)
        pdf.set_xy(10, y_start + actual_h)

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pdf = ChinesePDF()
    pdf.add_page()
    
    lines = content.split('\n')
    i = 0
    table_rows = []
    
    while i < len(lines):
        line = lines[i]
        stripped = fix_glyphs(line.strip())
        
        if not stripped:
            if table_rows:
                render_table(pdf, table_rows)
                table_rows = []
                pdf.ln(4)
            else:
                pdf.ln(2)
            i += 1
            continue
        
        # Table
        if stripped.startswith('|') and '|' in stripped[1:]:
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                i += 1
                continue
            cells = [c.strip() for c in stripped.split('|')]
            cells = [c for c in cells if c]
            table_rows.append(cells)
            i += 1
            continue
        
        if table_rows:
            render_table(pdf, table_rows)
            table_rows = []
            pdf.ln(4)
        
        # Headings
        if stripped.startswith('### '):
            pdf.set_font("SimHei", "B", 12)
            pdf.set_x(10)
            pdf.multi_cell(190, 6.5, stripped[4:])
            pdf.ln(2)
        elif stripped.startswith('## '):
            pdf.set_font("SimHei", "B", 14)
            pdf.set_x(10)
            pdf.multi_cell(190, 8, stripped[3:])
            pdf.ln(2)
        elif stripped.startswith('# '):
            pdf.set_font("SimHei", "B", 16)
            pdf.set_x(10)
            pdf.multi_cell(190, 10, stripped[2:])
            pdf.ln(3)
        elif stripped.startswith('- ') or stripped.startswith('    - '):
            pdf.set_font("SimHei", "", 10)
            text = clean_bold(re.sub(r'^[\s]*-\s*', '', stripped))
            pdf.set_x(14)
            pdf.cell(6, 5.5, "-")
            pdf.set_x(20)
            pdf.multi_cell(180, 5.5, text)
        elif re.match(r'^\d+\.\s+', stripped):
            pdf.set_font("SimHei", "", 10)
            m = re.match(r'^(\d+\.)\s*', stripped)
            num = m.group(1)
            text = clean_bold(stripped[m.end():])
            pdf.set_x(14)
            pdf.cell(6, 5.5, num)
            pdf.set_x(20)
            pdf.multi_cell(180, 5.5, text)
        elif stripped.startswith('*注：') or stripped.startswith('*Note'):
            pdf.set_font("SimHei", "", 9)
            pdf.set_x(15)
            pdf.multi_cell(180, 5, stripped)
        else:
            pdf.set_font("SimHei", "", 10)
            pdf.set_x(10)
            text = clean_bold(stripped)
            if text:
                pdf.multi_cell(190, 5.5, text)
        
        i += 1
    
    if table_rows:
        render_table(pdf, table_rows)
    
    pdf.output(pdf_path)
    return pdf.page_no()

if __name__ == '__main__':
    reports_dir = r"C:\Users\Administrator\Desktop\code\05_ai-foreign-trade-automation\reports_deai"
    for filename in sorted(os.listdir(reports_dir)):
        if filename.endswith('.md'):
            md_path = os.path.join(reports_dir, filename)
            pdf_name = filename.replace('.md', '.pdf')
            pdf_path = os.path.join(reports_dir, pdf_name)
            pages = md_to_pdf(md_path, pdf_path)
            print(f"OK: {pdf_name} ({pages} pages)")
    print("\nDone!")
