import os
import math
import logging
import zipfile
import shutil
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# -------------------------------------------------------------------
# SETUP LOGGING
# -------------------------------------------------------------------
LOG_FILE = 'errors.txt'
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

logging.basicConfig(filename=LOG_FILE,
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# -------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------
def safe_strip(val):
    if isinstance(val, str):
        return val.strip()
    return val

def setup_output_directories():
    """Cleans and recreates the main output directories."""
    dirs = ["output", "attendance_sheets"]
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
    return dirs

def get_session_paths(date_str, session):
    """
    Creates the sub-folder hierarchy inside output and attendance_sheets.
    Structure: output/YYYY_MM_DD/Session/
    """
    folder_name = date_str.replace("-", "_")
    
    # Path for Excel
    excel_dir = os.path.join("output", folder_name, session)
    os.makedirs(excel_dir, exist_ok=True)
    
    # Path for PDF
    pdf_dir = os.path.join("attendance_sheets", folder_name, session)
    os.makedirs(pdf_dir, exist_ok=True)
    
    return excel_dir, pdf_dir

def write_room_excel(course_code, room, slot, date, student_rows, folder_path):
    """Create the individual room Excel files in the 'output' folder."""
    filename = f"{date}_{course_code}_{room}_{slot.lower()}.xlsx"
    path = os.path.join(folder_path, filename)

    wb = Workbook()
    ws = wb.active
    ws.append([f"Course: {course_code} | Room: {room} | Date: {date} | Session: {slot}"])
    ws.append(["Roll", "Student Name", "Signature"])
    for roll, name in student_rows:
        ws.append([roll, name, ""])

    ws.append([])
    for i in range(1, 6):
        ws.append([f"TA{i}"])
    for i in range(1, 6):
        ws.append([f"Invigilator{i}"])
    wb.save(path)

# -------------------------------------------------------------------
# PDF GENERATION FUNCTION (Fixed Layouts)
# -------------------------------------------------------------------
def generate_attendance_pdf(course_code, room, slot, date, student_rows, folder_path, photos_dir="photos"):
    """
    Generates PDF with fixed margins and overlap protection.
    """
    date_clean = date.replace("-", "_")
    filename = f"{date_clean}_{slot.upper()}_{room}_{course_code}.pdf"
    file_path = os.path.join(folder_path, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4  # 595.27, 841.89 points

    # --- Margins & Layout Config ---
    left_m = 25
    right_m = 25
    top_m = height - 25
    bottom_m = 25
    
    printable_width = width - left_m - right_m
    
    # Grid config
    row_height = 80
    col_width = printable_width / 3
    
    # Footer Config
    footer_buffer = 30 # Min distance from last student
    footer_row_h = 22
    footer_header_h = 22
    footer_title_h = 25
    # Total height required for the footer block
    footer_block_height = footer_title_h + footer_header_h + (10 * footer_row_h)

    # --- Graphic Helpers ---
    def draw_page_border():
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.rect(left_m, bottom_m, printable_width, top_m - bottom_m)

    def draw_label_val(x, y, label, value):
        """Draws Bold Label and Normal Value, returns next X position."""
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y, label)
        
        label_w = c.stringWidth(label, "Helvetica-Bold", 10)
        c.setFont("Helvetica", 10)
        c.drawString(x + label_w + 3, y, value)
        
        return x + label_w + c.stringWidth(value, "Helvetica", 10) + 10

    def draw_header():
        """Draws the header with right-aligned attendance fields."""
        # 1. Main Title
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, top_m - 20, "IITP Attendance System")
        
        c.setLineWidth(0.5)
        c.line(left_m, top_m - 30, width - right_m, top_m - 30)
        
        # 2. Date/Shift/Room Row
        curr_y = top_m - 45
        curr_x = left_m + 5
        
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_fmt = f"{date} ({date_obj.strftime('%A')})"
        
        curr_x = draw_label_val(curr_x, curr_y, "Date:", date_fmt)
        c.drawString(curr_x - 5, curr_y, "|") 
        curr_x += 5
        
        curr_x = draw_label_val(curr_x, curr_y, "Shift:", slot)
        c.drawString(curr_x - 5, curr_y, "|")
        curr_x += 5
        
        curr_x = draw_label_val(curr_x, curr_y, "Room No:", str(room))
        c.drawString(curr_x - 5, curr_y, "|")
        curr_x += 5
        
        draw_label_val(curr_x, curr_y, "Student count:", str(len(student_rows)))
        
        # 3. Subject & Attendance Row (Fixed Layout)
        curr_y -= 20
        
        # Define Text
        absent_str = "Stud Absent: ________________"
        present_str = "Stud Present: ________________"
        
        # Calculate widths
        c.setFont("Helvetica-Bold", 10)
        w_absent = c.stringWidth(absent_str, "Helvetica-Bold", 10)
        w_present = c.stringWidth(present_str, "Helvetica-Bold", 10)
        
        # Right Align Calculations
        # Absent field touches Right Margin (minus padding)
        x_absent = width - right_m - w_absent - 5 
        # Present field sits to the left of Absent field
        x_present = x_absent - 20 - w_present 
        
        # Draw Attendance Fields
        c.drawString(x_present, curr_y, present_str)
        c.drawString(x_absent, curr_y, absent_str)
        
        # Draw Subject (Truncate if it hits Present field)
        # Max width available for subject = x_present - left_m - padding
        max_sub_w = x_present - left_m - 15
        
        sub_label = "Subject: "
        sub_label_w = c.stringWidth(sub_label, "Helvetica-Bold", 10)
        
        available_for_code = max_sub_w - sub_label_w
        
        # Simple truncation logic
        disp_course = course_code
        if c.stringWidth(course_code, "Helvetica", 10) > available_for_code:
            # Approximate char width ~ 6
            chars_fit = int(available_for_code / 6)
            disp_course = course_code[:chars_fit] + "..."
            
        draw_label_val(left_m + 5, curr_y, sub_label, disp_course)
        
        # Line Divider
        c.line(left_m, curr_y - 10, width - right_m, curr_y - 10)
        
        return curr_y - 10 # Returns Y bottom of header

    # --- Start Page 1 ---
    draw_page_border()
    header_bottom = draw_header()
    
    y = header_bottom - row_height # Top of first row is header_bottom
    # Wait: The loop below uses `y` as the BOTTOM of the cell in some contexts, let's standardize.
    # Logic: y represents the BOTTOM of the current cell being drawn.
    # c.drawImage uses (x, y) as bottom-left.
    # So if header ends at 700, and row is 80. The first row should be drawn at y = 620.
    
    current_y = header_bottom - row_height 
    x = left_m
    col_counter = 0
    
    # Track the lowest Y point used on the page to determine footer placement
    lowest_y_used = height 

    # --- Student Loop ---
    for roll, name in student_rows:
        
        # Check if we need a new page
        # If current_y is dangerously close to bottom margin
        if current_y < (bottom_m + 10):
            c.showPage()
            draw_page_border()
            # Reset top
            current_y = top_m - row_height - 10
            x = left_m
            col_counter = 0
            lowest_y_used = height

        # Update lowest Y tracking
        if current_y < lowest_y_used:
            lowest_y_used = current_y

        # Draw Photo
        photo_path = os.path.join(photos_dir, f"{roll}.jpg")
        img_x = x + 5
        img_y = current_y + 10
        img_w = 55
        img_h = 60
        
        has_image = False
        if os.path.exists(photo_path):
            try:
                c.drawImage(photo_path, img_x, img_y, width=img_w, height=img_h, preserveAspectRatio=True)
                has_image = True
            except Exception:
                pass

        if not has_image:
            c.setStrokeColor(colors.black)
            c.setLineWidth(1)
            c.rect(img_x, img_y, img_w, img_h)
            c.setFont("Helvetica", 7)
            c.drawCentredString(img_x + img_w/2, img_y + img_h/2 + 5, "No Image")
            c.drawCentredString(img_x + img_w/2, img_y + img_h/2 - 5, "Available")

        # Draw Text
        text_x = img_x + img_w + 5
        text_y_start = current_y + row_height - 20
        
        c.setFillColor(colors.black)
        disp_name = name if len(name) < 22 else name[:20] + "..."
        c.setFont("Helvetica-Bold", 10)
        c.drawString(text_x, text_y_start, disp_name)
        
        c.setFont("Helvetica-Bold", 10) # Keys Bold
        c.drawString(text_x, text_y_start - 15, "Roll:")
        c.setFont("Helvetica", 10)      # Values Normal
        c.drawString(text_x + 25, text_y_start - 15, str(roll))
        
        c.setFont("Helvetica", 10)
        c.drawString(text_x, text_y_start - 35, "Sign: ____________")

        # Increment
        col_counter += 1
        if col_counter < 3:
            x += col_width
        else:
            x = left_m
            col_counter = 0
            current_y -= row_height

    # --- Footer Logic (Collision Proof) ---
    
    # Calculate where the footer *wants* to start (buffer below last student)
    # lowest_y_used represents the bottom line of the last drawn student row.
    wanted_table_start = lowest_y_used - footer_buffer
    
    # Calculate where the table would end
    wanted_table_end = wanted_table_start - footer_block_height
    
    # Determine actual start position
    if wanted_table_end < bottom_m:
        # Overlap detected! New Page.
        c.showPage()
        draw_page_border()
        footer_start_y = top_m - footer_buffer
    else:
        # Fits on current page
        footer_start_y = wanted_table_start
    
    # Draw Footer
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_m + 5, footer_start_y, "Invigilator Name & Signature")
    
    table_top = footer_start_y - footer_title_h
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    
    # Header
    c.setFont("Helvetica-Bold", 10)
    c.rect(left_m, table_top - footer_header_h, 40, footer_header_h)
    c.drawCentredString(left_m + 20, table_top - 15, "Sl No.")
    
    c.rect(left_m + 40, table_top - footer_header_h, 250, footer_header_h)
    c.drawString(left_m + 45, table_top - 15, "Name")
    
    c.rect(left_m + 290, table_top - footer_header_h, 200, footer_header_h)
    c.drawString(left_m + 295, table_top - 15, "Signature")
    
    # Rows (1 to 10)
    c.setFont("Helvetica", 10)
    for i in range(1, 11):
        row_y = table_top - footer_header_h - ((i-1) * footer_row_h)
        
        c.rect(left_m, row_y - footer_row_h, 40, footer_row_h)
        c.drawCentredString(left_m + 20, row_y - 15, str(i))
        
        c.rect(left_m + 40, row_y - footer_row_h, 250, footer_row_h)
        c.rect(left_m + 290, row_y - footer_row_h, 200, footer_row_h)

    c.save()

# -------------------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------------------
def allocate_seating(excel_file):
    try:
        setup_output_directories()

        # Load input sheets
        timetable = pd.read_excel(excel_file, sheet_name='in_timetable')
        roll_map = pd.read_excel(excel_file, sheet_name='in_roll_name_mapping')
        room_capacity = pd.read_excel(excel_file, sheet_name='in_room_capacity')
        course_rolls = pd.read_excel(excel_file, sheet_name='in_course_roll_mapping')

        # Clean whitespace
        timetable = timetable.map(safe_strip)
        roll_map = roll_map.map(safe_strip)
        room_capacity = room_capacity.map(safe_strip)
        course_rolls = course_rolls.map(safe_strip)

        roll_to_name = dict(zip(roll_map['Roll'], roll_map['Name']))

        buffer = int(input("Enter buffer value: ").strip())
        mode = input("Enter mode (Sparse/Dense): ").strip().lower()
        if mode not in ['sparse', 'dense']:
            raise ValueError("Mode must be either 'Sparse' or 'Dense'.")

        # Process rooms
        rooms_info = []
        for _, row in room_capacity.iterrows():
            cap = row['Exam Capacity']
            block = row['Block']
            effective_capacity = max(0, cap - buffer)
            if mode == 'sparse':
                effective_capacity = math.floor(effective_capacity / 2)
            rooms_info.append({
                "Room": row['Room No.'],
                "Capacity": cap,
                "Block": block,
                "Available": effective_capacity,
                "InitialAvailable": effective_capacity 
            })

        seating_records = []
        seats_left_records = []
        
        photos_dir = "photos"
        if not os.path.exists(photos_dir):
            logging.warning(f"'{photos_dir}' folder not found. Images will be blank.")

        for _, day_row in timetable.iterrows():
            date_val = str(day_row['Date']).split()[0]
            date = date_val.replace(" 00:00:00", "")
            day = str(day_row['Day'])

            for slot in ['Morning', 'Evening']:
                slot_data = str(day_row[slot])
                if "NO EXAM" in slot_data.upper():
                    continue

                excel_folder, pdf_folder = get_session_paths(date, slot)
                logging.info(f"Processing {date} {day} {slot}")
                
                subjects = [s.strip() for s in slot_data.split(';') if s.strip()]
                subject_rolls = {
                    sub: course_rolls[course_rolls['course_code'] == sub]['rollno'].tolist()
                    for sub in subjects
                }

                # Check Clashes
                all_sets = list(subject_rolls.values())
                for i in range(len(all_sets)):
                    for j in range(i + 1, len(all_sets)):
                        inter = set(all_sets[i]).intersection(set(all_sets[j]))
                        if inter:
                            logging.error(f"Clash {date} {slot}: {subjects[i]} & {subjects[j]} -> {inter}")

                subjects_sorted = sorted(subject_rolls.items(), key=lambda x: len(x[1]), reverse=True)
                rooms = [r.copy() for r in rooms_info]

                block_groups = {}
                for r in rooms:
                    block_groups.setdefault(r['Block'], []).append(r)
                for b in block_groups:
                    block_groups[b] = sorted(block_groups[b], key=lambda x: x['Room'])

                unallocated = {}

                def save_allocation(course_code, room_obj, assigned_list):
                    names = [roll_to_name.get(r, "name not found") for r in assigned_list]
                    student_data = list(zip(assigned_list, names))
                    
                    write_room_excel(course_code, room_obj["Room"], slot, date, student_data, excel_folder)
                    generate_attendance_pdf(course_code, room_obj["Room"], slot, date, student_data, pdf_folder, photos_dir)
                    seating_records.append([date, day, slot, course_code, room_obj["Room"], len(assigned_list), ';'.join(assigned_list)])

                # Allocation Pass 1 & 2
                for course, rolls in subjects_sorted:
                    remaining = rolls.copy()
                    for block, block_rooms in block_groups.items():
                        for room in block_rooms:
                            if not remaining: break
                            if room["Available"] <= 0: continue
                            take = min(room["Available"], len(remaining))
                            assigned = remaining[:take]
                            remaining = remaining[take:]
                            room["Available"] -= take
                            save_allocation(course, room, assigned)
                        if not remaining: break
                    if remaining: unallocated[course] = remaining

                for course, remaining in unallocated.items():
                    if not remaining: continue
                    for room in rooms:
                        if not remaining: break
                        if room["Available"] <= 0: continue
                        take = min(room["Available"], len(remaining))
                        assigned = remaining[:take]
                        remaining = remaining[take:]
                        room["Available"] -= take
                        save_allocation(course, room, assigned)
                    if remaining:
                        msg = f"Unallocated {course}: {len(remaining)} left on {date} {slot}"
                        print(msg)
                        with open(LOG_FILE, 'a') as ef: ef.write(msg + '\n')

                # Seats Left
                for room in rooms:
                    initial = room.get("InitialAvailable", 0)
                    seats_left_records.append([date, day, slot, room["Room"], room["Capacity"], room["Block"], initial - room["Available"], max(0, room["Available"])])

        # Save Global Excels
        df_seating = pd.DataFrame(seating_records, columns=['Date', 'Day', 'Slot', 'Course_Code', 'Room', 'Allocated', 'Roll_List'])
        df_seatsleft = pd.DataFrame(seats_left_records, columns=['Date', 'Day', 'Slot', 'Room', 'Capacity', 'Block', 'Allotted', 'Vacant'])

        df_seating.to_excel("op_overall_seating_arrangement.xlsx", index=False)
        df_seatsleft.to_excel("op_seats_left.xlsx", index=False)

        # ZIP
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = "output.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for f in ["op_overall_seating_arrangement.xlsx", "op_seats_left.xlsx", LOG_FILE]:
                if os.path.exists(f): zipf.write(f)
            for root, _, files in os.walk("output"):
                for file in files: zipf.write(os.path.join(root, file))
            for root, _, files in os.walk("attendance_sheets"):
                for file in files: zipf.write(os.path.join(root, file))

        logging.info(f"✅ Completed. Files zipped to {zip_name}")

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    file = input("Enter Excel file name: ").strip()
    allocate_seating(file)