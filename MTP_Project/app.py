import streamlit as st
import os
import math
import logging
import zipfile
import shutil
import pandas as pd
import base64
import time
from openpyxl import Workbook
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ==========================================
# CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Exam Seating Master",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold;}
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 5px solid #4CAF50;
    }
    .success-box { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; margin-bottom: 10px; }
    .error-box { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 5px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'processed' not in st.session_state: st.session_state.processed = False
if 'seating_df' not in st.session_state: st.session_state.seating_df = None
if 'seats_left_df' not in st.session_state: st.session_state.seats_left_df = None
if 'pdf_map' not in st.session_state: st.session_state.pdf_map = {}
if 'zip_path' not in st.session_state: st.session_state.zip_path = None

# ==========================================
# LOGGING SETUP (FIXED)
# ==========================================
LOG_FILE = 'errors.txt'

# Close any existing handlers to release the file lock
# This prevents [WinError 32] when re-running the script
for handler in logging.root.handlers[:]:
    handler.close()
    logging.root.removeHandler(handler)

# Safely remove the old log file
if os.path.exists(LOG_FILE):
    try:
        os.remove(LOG_FILE)
    except PermissionError:
        pass # If still locked, we append to it rather than crashing

# Re-configure logging
logging.basicConfig(
    filename=LOG_FILE, 
    filemode='a', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_message(msg, level="info"):
    """Helper to log to file and print to console"""
    if level == "info": logging.info(msg)
    elif level == "error": logging.error(msg)
    print(msg)

# ==========================================
# BACKEND LOGIC
# ==========================================

def safe_strip(val):
    if isinstance(val, str): return val.strip()
    return val

def setup_output_directories():
    dirs = ["output", "attendance_sheets", "photos"]
    for d in dirs:
        if not os.path.exists(d): os.makedirs(d)
        # Note: We don't clean 'photos' to preserve user uploads if any
    
    # Clean output dirs only
    for d in ["output", "attendance_sheets"]:
        if os.path.exists(d): shutil.rmtree(d)
        os.makedirs(d)
    return dirs

def get_session_paths(date_str, session):
    folder_name = date_str.replace("-", "_")
    excel_dir = os.path.join("output", folder_name, session)
    pdf_dir = os.path.join("attendance_sheets", folder_name, session)
    os.makedirs(excel_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    return excel_dir, pdf_dir

# --- PDF Generation ---
def generate_attendance_pdf(course_code, room, slot, date, student_rows, folder_path, photos_dir="photos"):
    try:
        date_clean = date.replace("-", "_")
        filename = f"{date_clean}_{slot.upper()}_{room}_{course_code}.pdf"
        file_path = os.path.join(folder_path, filename)

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        left_m, right_m, top_m, bottom_m = 25, 25, height - 25, 25
        printable_width = width - left_m - right_m
        row_height = 80
        col_width = printable_width / 3
        footer_buffer, footer_row_h, footer_header_h, footer_title_h = 30, 22, 22, 25
        footer_block_height = footer_title_h + footer_header_h + (10 * footer_row_h)

        def draw_page_border():
            c.setStrokeColor(colors.black); c.setLineWidth(1)
            c.rect(left_m, bottom_m, printable_width, top_m - bottom_m)

        def draw_label_val(x, y, label, value):
            c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 10); c.drawString(x, y, label)
            label_w = c.stringWidth(label, "Helvetica-Bold", 10)
            c.setFont("Helvetica", 10); c.drawString(x + label_w + 3, y, value)
            return x + label_w + c.stringWidth(value, "Helvetica", 10) + 10

        def draw_header():
            c.setFont("Helvetica-Bold", 14); c.drawCentredString(width / 2, top_m - 20, "IITP Attendance System")
            c.setLineWidth(0.5); c.line(left_m, top_m - 30, width - right_m, top_m - 30)
            curr_y, curr_x = top_m - 45, left_m + 5
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            curr_x = draw_label_val(curr_x, curr_y, "Date:", f"{date} ({date_obj.strftime('%A')})")
            c.drawString(curr_x - 5, curr_y, "|"); curr_x += 5
            curr_x = draw_label_val(curr_x, curr_y, "Shift:", slot)
            c.drawString(curr_x - 5, curr_y, "|"); curr_x += 5
            curr_x = draw_label_val(curr_x, curr_y, "Room No:", str(room))
            c.drawString(curr_x - 5, curr_y, "|"); curr_x += 5
            draw_label_val(curr_x, curr_y, "Student count:", str(len(student_rows)))
            curr_y -= 20
            absent_str, present_str = "Stud Absent: ________________", "Stud Present: ________________"
            c.setFont("Helvetica-Bold", 10)
            w_absent, w_present = c.stringWidth(absent_str, "Helvetica-Bold", 10), c.stringWidth(present_str, "Helvetica-Bold", 10)
            x_absent = width - right_m - w_absent - 5; x_present = x_absent - 20 - w_present
            c.drawString(x_present, curr_y, present_str); c.drawString(x_absent, curr_y, absent_str)
            max_sub_w = x_present - left_m - 15; sub_label = "Subject: "; sub_label_w = c.stringWidth(sub_label, "Helvetica-Bold", 10)
            available_for_code = max_sub_w - sub_label_w
            disp_course = course_code if c.stringWidth(course_code, "Helvetica", 10) <= available_for_code else course_code[:int(available_for_code / 6)] + "..."
            draw_label_val(left_m + 5, curr_y, sub_label, disp_course)
            c.line(left_m, curr_y - 10, width - right_m, curr_y - 10)
            return curr_y - 10

        draw_page_border(); header_bottom = draw_header()
        current_y, x, col_counter, lowest_y_used = header_bottom - row_height, left_m, 0, height

        for roll, name in student_rows:
            if current_y < (bottom_m + 10):
                c.showPage(); draw_page_border(); current_y = top_m - row_height - 10; x = left_m; col_counter = 0; lowest_y_used = height
            if current_y < lowest_y_used: lowest_y_used = current_y
            
            photo_path = os.path.join(photos_dir, f"{roll}.jpg")
            img_x, img_y, img_w, img_h = x + 5, current_y + 10, 55, 60
            if os.path.exists(photo_path):
                try: c.drawImage(photo_path, img_x, img_y, width=img_w, height=img_h, preserveAspectRatio=True)
                except: pass
            else:
                c.setStrokeColor(colors.black); c.setLineWidth(1); c.rect(img_x, img_y, img_w, img_h)
                c.setFont("Helvetica", 7); c.drawCentredString(img_x + img_w/2, img_y + img_h/2 + 5, "No Image"); c.drawCentredString(img_x + img_w/2, img_y + img_h/2 - 5, "Available")
            
            text_x, text_y_start = img_x + img_w + 5, current_y + row_height - 20
            c.setFillColor(colors.black); disp_name = name if len(name) < 22 else name[:20] + "..."
            c.setFont("Helvetica-Bold", 10); c.drawString(text_x, text_y_start, disp_name)
            c.setFont("Helvetica-Bold", 10); c.drawString(text_x, text_y_start - 15, "Roll:")
            c.setFont("Helvetica", 10); c.drawString(text_x + 25, text_y_start - 15, str(roll))
            c.setFont("Helvetica", 10); c.drawString(text_x, text_y_start - 35, "Sign: ____________")

            col_counter += 1
            if col_counter < 3: x += col_width
            else: x = left_m; col_counter = 0; current_y -= row_height

        wanted_table_start = lowest_y_used - footer_buffer
        if (wanted_table_start - footer_block_height) < bottom_m: c.showPage(); draw_page_border(); footer_start_y = top_m - footer_buffer
        else: footer_start_y = wanted_table_start
        
        c.setFillColor(colors.black); c.setFont("Helvetica-Bold", 10); c.drawString(left_m + 5, footer_start_y, "Invigilator Name & Signature")
        table_top = footer_start_y - footer_title_h; c.setStrokeColor(colors.black); c.setLineWidth(1)
        c.setFont("Helvetica-Bold", 10)
        c.rect(left_m, table_top - footer_header_h, 40, footer_header_h); c.drawCentredString(left_m + 20, table_top - 15, "Sl No.")
        c.rect(left_m + 40, table_top - footer_header_h, 250, footer_header_h); c.drawString(left_m + 45, table_top - 15, "Name")
        c.rect(left_m + 290, table_top - footer_header_h, 200, footer_header_h); c.drawString(left_m + 295, table_top - 15, "Signature")
        c.setFont("Helvetica", 10)
        for i in range(1, 11):
            row_y = table_top - footer_header_h - ((i-1) * footer_row_h)
            c.rect(left_m, row_y - footer_row_h, 40, footer_row_h); c.drawCentredString(left_m + 20, row_y - 15, str(i))
            c.rect(left_m + 40, row_y - footer_row_h, 250, footer_row_h); c.rect(left_m + 290, row_y - footer_row_h, 200, footer_row_h)
        c.save()
        return file_path
    except Exception as e:
        log_message(f"Error generating PDF for {course_code} in {room}: {str(e)}", "error")
        return None

# --- Helpers ---
def write_room_excel(course_code, room, slot, date, student_rows, folder_path):
    try:
        filename = f"{date}_{course_code}_{room}_{slot.lower()}.xlsx"
        path = os.path.join(folder_path, filename)
        wb = Workbook(); ws = wb.active
        ws.append([f"Course: {course_code} | Room: {room} | Date: {date} | Session: {slot}"])
        ws.append(["Roll", "Student Name", "Signature"])
        for roll, name in student_rows: ws.append([roll, name, ""])
        for i in range(1, 6): ws.append([f"TA{i}"])
        for i in range(1, 6): ws.append([f"Invigilator{i}"])
        wb.save(path)
    except Exception as e:
        log_message(f"Error writing Excel {filename}: {str(e)}", "error")

# --- Main Processor ---
def process_allocation(uploaded_file, buffer, mode):
    setup_output_directories()
    
    try:
        xls = pd.ExcelFile(uploaded_file)
        timetable = pd.read_excel(xls, 'in_timetable').map(safe_strip)
        roll_map = pd.read_excel(xls, 'in_roll_name_mapping').map(safe_strip)
        room_capacity = pd.read_excel(xls, 'in_room_capacity').map(safe_strip)
        course_rolls = pd.read_excel(xls, 'in_course_roll_mapping').map(safe_strip)
    except Exception as e:
        log_message(f"Error reading Input Excel: {str(e)}", "error")
        st.error("Failed to read input file. Check sheets and format.")
        return None, None, None, None

    roll_to_name = dict(zip(roll_map['Roll'], roll_map['Name']))
    
    rooms_info = []
    for _, row in room_capacity.iterrows():
        cap = row['Exam Capacity']; eff_cap = max(0, cap - buffer)
        if mode == 'Sparse': eff_cap = math.floor(eff_cap / 2)
        rooms_info.append({"Room": row['Room No.'], "Capacity": cap, "Block": row['Block'], "Available": eff_cap, "InitialAvailable": eff_cap})

    seating_records, seats_left_records, pdf_mapping = [], [], {}
    progress_bar = st.progress(0); status_text = st.empty()
    total_steps = len(timetable) * 2; step = 0

    for _, day_row in timetable.iterrows():
        date_val = str(day_row['Date']).split()[0].replace(" 00:00:00", "")
        day = str(day_row['Day'])
        for slot in ['Morning', 'Evening']:
            step += 1; progress_bar.progress(int((step/total_steps)*100)); status_text.text(f"Processing {date_val} {slot}")
            slot_data = str(day_row[slot])
            if "NO EXAM" in slot_data.upper(): continue

            excel_folder, pdf_folder = get_session_paths(date_val, slot)
            subjects = [s.strip() for s in slot_data.split(';') if s.strip()]
            
            # Safe subject retrieval
            try:
                subject_rolls = {sub: course_rolls[course_rolls['course_code'] == sub]['rollno'].tolist() for sub in subjects}
            except KeyError as e:
                log_message(f"Course Code missing in Mapping: {e}", "error")
                continue

            # Clash Check
            all_sets = list(subject_rolls.values())
            for i in range(len(all_sets)):
                for j in range(i + 1, len(all_sets)):
                    inter = set(all_sets[i]).intersection(set(all_sets[j]))
                    if inter:
                        log_message(f"CLASH DETECTED {date_val} {slot}: {subjects[i]} & {subjects[j]} -> {inter}", "error")

            subjects_sorted = sorted(subject_rolls.items(), key=lambda x: len(x[1]), reverse=True)
            
            rooms = [r.copy() for r in rooms_info]
            block_groups = {}; 
            for r in rooms: block_groups.setdefault(r['Block'], []).append(r)
            for b in block_groups: block_groups[b] = sorted(block_groups[b], key=lambda x: x['Room'])
            unallocated = {}

            def save_alloc(course, room_obj, assigned):
                names = [roll_to_name.get(r, "Unknown") for r in assigned]
                data = list(zip(assigned, names))
                write_room_excel(course, room_obj["Room"], slot, date_val, data, excel_folder)
                pdf_path = generate_attendance_pdf(course, room_obj["Room"], slot, date_val, data, pdf_folder)
                if pdf_path:
                    key = f"{date_val}|{slot}|{room_obj['Room']}|{course}"
                    pdf_mapping[key] = pdf_path
                seating_records.append([date_val, day, slot, course, room_obj["Room"], len(assigned), ';'.join(assigned)])

            for course, rolls in subjects_sorted:
                remaining = rolls.copy()
                for block, block_rooms in block_groups.items():
                    for room in block_rooms:
                        if not remaining or room["Available"] <= 0: continue
                        take = min(room["Available"], len(remaining))
                        save_alloc(course, room, remaining[:take])
                        room["Available"] -= take; remaining = remaining[take:]
                    if not remaining: break
                if remaining: unallocated[course] = remaining
            
            for course, remaining in unallocated.items():
                if not remaining: continue
                for room in rooms:
                    if not remaining or room["Available"] <= 0: continue
                    take = min(room["Available"], len(remaining))
                    save_alloc(course, room, remaining[:take])
                    room["Available"] -= take; remaining = remaining[take:]
                if remaining:
                    log_message(f"Unallocated Students: {course} ({len(remaining)} students left) on {date_val}", "error")
            
            for room in rooms:
                seats_left_records.append([date_val, day, slot, room["Room"], room["Capacity"], room["Block"], room["InitialAvailable"] - room["Available"], max(0, room["Available"])])

    df_seating = pd.DataFrame(seating_records, columns=['Date', 'Day', 'Slot', 'Course_Code', 'Room', 'Allocated', 'Roll_List'])
    df_seats = pd.DataFrame(seats_left_records, columns=['Date', 'Day', 'Slot', 'Room', 'Capacity', 'Block', 'Allotted', 'Vacant'])
    
    zip_name = "output.zip"
    df_seating.to_excel("op_overall_seating_arrangement.xlsx", index=False)
    df_seats.to_excel("op_seats_left.xlsx", index=False)
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in ["op_overall_seating_arrangement.xlsx", "op_seats_left.xlsx"]: 
            if os.path.exists(f): z.write(f)
        if os.path.exists(LOG_FILE): z.write(LOG_FILE) # Include LOGS
        for root, _, files in os.walk("output"):
            for f in files: z.write(os.path.join(root, f))
        for root, _, files in os.walk("attendance_sheets"):
            for f in files: z.write(os.path.join(root, f))

    return df_seating, df_seats, pdf_mapping, zip_name

# ==========================================
# UI
# ==========================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3534/3534033.png", width=80)
    st.title("Exam Master")
    
    st.markdown("### ⚙️ Settings")
    buffer_val = st.number_input("Buffer Seats", 0, 10, 0)
    mode_val = st.selectbox("Seating Mode", ["Dense", "Sparse"])
    
    st.markdown("---")
    st.markdown("### 📁 Data Source")
    uploaded_file = st.file_uploader("Upload Excel Input", type=['xlsx'])
    
    # --- PERMANENT DOWNLOAD BUTTON IN SIDEBAR ---
    if st.session_state.processed and st.session_state.zip_path:
        st.markdown("---")
        st.markdown("### 📥 Downloads")
        
        try:
            with open(st.session_state.zip_path, "rb") as f:
                st.download_button(
                    label="Download Result ZIP",
                    data=f,
                    file_name="Exam_Seating_Output.zip",
                    mime="application/zip",
                    key="sidebar_download"
                )
        except FileNotFoundError:
            st.error("Zip file missing. Reprocess.")

st.title("🎓 Exam Seating & Attendance System")

# PROCESSING BUTTON
if uploaded_file:
    if st.button("🚀 Process & Allocate"):
        with st.spinner("Processing Seating Plan..."):
            with open("temp.xlsx", "wb") as f: f.write(uploaded_file.getbuffer())
            
            df_seat, df_left, pdf_map, zip_f = process_allocation("temp.xlsx", buffer_val, mode_val)
            
            if df_seat is not None:
                st.session_state.seating_df = df_seat
                st.session_state.seats_left_df = df_left
                st.session_state.pdf_map = pdf_map
                st.session_state.zip_path = zip_f
                st.session_state.processed = True
                st.balloons()
            else:
                st.error("Processing Failed.")

# RESULTS AREA
if st.session_state.processed:
    
    # Check for Logs/Errors
    log_content = ""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as lf: log_content = lf.read()
    
    if log_content:
        with st.expander("⚠️ System Logs / Errors (Click to View)"):
            st.text_area("Log Output", log_content, height=200)

    # --- GLOBAL FILTERS ---
    st.markdown("### 🔍 Select Day & Session to Inspect")
    df_main = st.session_state.seats_left_df
    
    unique_dates = sorted(df_main['Date'].unique())
    col_f1, col_f2 = st.columns(2)
    with col_f1: sel_date = st.selectbox("Select Date", unique_dates)
    available_slots = df_main[df_main['Date'] == sel_date]['Slot'].unique()
    with col_f2: sel_slot = st.selectbox("Select Slot", available_slots)

    # Filter Data
    filtered_capacity_df = df_main[(df_main['Date'] == sel_date) & (df_main['Slot'] == sel_slot)]
    df_alloc = st.session_state.seating_df
    filtered_alloc_df = df_alloc[(df_alloc['Date'] == sel_date) & (df_alloc['Slot'] == sel_slot)]

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Stats", "📋 Data Explorer", "📄 Attendance Viewer"])

    # --- TAB 1: DASHBOARD ---
    with tab1:
        total_students_session = filtered_alloc_df['Allocated'].sum()
        total_capacity_session = filtered_capacity_df['Capacity'].sum() if not filtered_capacity_df.empty else 0
        rooms_used_session = filtered_capacity_df[filtered_capacity_df['Allotted'] > 0]['Room'].nunique()
        rooms_vacant_session = filtered_capacity_df[filtered_capacity_df['Allotted'] == 0]['Room'].nunique()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"Students ({sel_slot})", total_students_session)
        c2.metric("Rooms Used", rooms_used_session)
        c3.metric("Unallocated Rooms", rooms_vacant_session)
        c4.metric("Effective Capacity", total_capacity_session)

        st.markdown("### 📉 Room Utilization Breakdown")
        if not filtered_capacity_df.empty:
            chart_data = filtered_capacity_df[['Room', 'Allotted', 'Vacant']].set_index('Room')
            st.bar_chart(chart_data, color=["#4CAF50", "#E0E0E0"])

    # --- TAB 2: DATA EXPLORER ---
    with tab2:
        st.subheader(f"Room Status for {sel_date} ({sel_slot})")
        st.dataframe(filtered_capacity_df, use_container_width=True)

        st.subheader(f"Student Allocation Details for {sel_date} ({sel_slot})")
        st.dataframe(filtered_alloc_df, use_container_width=True)

    # --- TAB 3: PDF VIEWER ---
    with tab3:
        prefix = f"{sel_date}|{sel_slot}"
        relevant_pdfs = [k for k in st.session_state.pdf_map.keys() if k.startswith(prefix)]
        
        if relevant_pdfs:
            pdf_options = {f"{k.split('|')[2]} - {k.split('|')[3]}": k for k in relevant_pdfs}
            sel_pdf_label = st.selectbox("Select Room & Subject", sorted(pdf_options.keys()))
            
            if sel_pdf_label:
                key = pdf_options[sel_pdf_label]
                pdf_path = st.session_state.pdf_map.get(key)
                
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    st.error("PDF file not found on server.")
        else:
            st.warning(f"No PDFs generated for {sel_date} {sel_slot}.")
else:
    st.info("Upload an Excel file and click Process to see results.")