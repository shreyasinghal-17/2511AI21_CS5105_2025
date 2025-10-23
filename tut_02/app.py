
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from fac_allocator import allocate_students
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="BTP/MTP Allocation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Main styling */
    * {
        font-family: 'Poppins', sans-serif;
    }

    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
    }

    .sub-header {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin: 0.5rem 0;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }

    /* Success box */
    .success-box {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Info box */
    .info-box {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%);
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Warning box */
    .warning-box {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Algorithm box */
    .algo-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .algo-box h3 {
        color: #2d3748;
        margin-bottom: 1rem;
    }

    .algo-step {
        background: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        border: none;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }

    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(17, 153, 142, 0.4);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* DataFrame styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)


def display_animated_metric(label, value, icon):
    """Display an animated metric card"""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{icon} {label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


def create_distribution_chart(allocation_df):
    """Create interactive faculty distribution chart"""
    fac_counts = allocation_df['Allocated'].value_counts().sort_index()

    fig = go.Figure(data=[
        go.Bar(
            x=fac_counts.index,
            y=fac_counts.values,
            marker=dict(
                color=fac_counts.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Students")
            ),
            text=fac_counts.values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Students: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Faculty-wise Student Distribution",
        xaxis_title="Faculty",
        yaxis_title="Number of Students",
        template="plotly_white",
        height=500,
        hovermode='x unified'
    )

    return fig


def create_cgpa_distribution_chart(allocation_df):
    """Create CGPA distribution chart"""
    fig = px.histogram(
        allocation_df,
        x='CGPA',
        nbins=30,
        title='CGPA Distribution of Allocated Students',
        labels={'CGPA': 'CGPA', 'count': 'Number of Students'},
        color_discrete_sequence=['#667eea']
    )

    fig.update_layout(
        template="plotly_white",
        height=400
    )

    return fig


def create_preference_heatmap(pref_stats_df):
    """Create preference heatmap"""
    # Prepare data for heatmap
    faculties = pref_stats_df['Fac'].tolist()
    pref_columns = [col for col in pref_stats_df.columns if col.startswith('Count Pref')]

    data = pref_stats_df[pref_columns].values

    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=[f"P{i+1}" for i in range(len(pref_columns))],
        y=faculties,
        colorscale='RdYlGn_r',
        text=data,
        texttemplate='%{text}',
        textfont={"size": 10},
        hovertemplate='Faculty: %{y}<br>Preference: %{x}<br>Count: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title='Faculty Preference Heatmap (Darker = More students got this preference)',
        xaxis_title='Preference Level',
        yaxis_title='Faculty',
        height=600,
        template="plotly_white"
    )

    return fig


def create_faculty_allocation_chart(allocation_df):
    """Create sunburst chart for faculty allocation"""
    fac_counts = allocation_df['Allocated'].value_counts()

    fig = go.Figure(go.Pie(
        labels=fac_counts.index,
        values=fac_counts.values,
        hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set3),
        textinfo='label+value',
        hovertemplate='<b>%{label}</b><br>Students: %{value}<br>Percentage: %{percent}<extra></extra>'
    ))

    fig.update_layout(
        title='Faculty Allocation Distribution',
        height=500,
        template="plotly_white"
    )

    return fig


def main():
    """Main Streamlit application with enhanced UI"""

    # Header
    st.markdown('<h1 class="main-header">🎓 BTP/MTP Allocation System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Guide Allocation System</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 System Information")

        st.markdown("""
        <div class="algo-box">
            <h3>🔄 Algorithm Overview</h3>
            <div class="algo-step">
                <strong>Step 1:</strong> Sort students by CGPA (highest first)
            </div>
            <div class="algo-step">
                <strong>Step 2:</strong> Divide into cycles (n students per cycle)
            </div>
            <div class="algo-step">
                <strong>Step 3:</strong> Each cycle allocates 1 student per faculty
            </div>
            <div class="algo-step">
                <strong>Step 4:</strong> Respect student preferences within constraints
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        ### 📋 Input Format
        - **Fixed Columns:** Roll, Name, Email, CGPA
        - **Faculty Columns:** Contain preference rankings (1 to n)
        - Each value represents student's preference order
        """)

        st.markdown("---")

        st.markdown("""
        ### ✨ Features
        - 🎯 Fair allocation algorithm
        - 📊 Interactive visualizations
        - 📈 Detailed statistics
        - 💾 CSV export functionality
        - 🔍 Real-time preview
        """)

        st.markdown("---")

        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            1. Upload your input CSV file
            2. Preview the data and verify
            3. Click "Run Allocation" button
            4. View results and statistics
            5. Download output files
            """)

    # Main content area
    st.markdown("### 📁 Upload Input File")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        uploaded_file = st.file_uploader(
            "",
            type=['csv'],
            help="Upload the student preference CSV file",
            label_visibility="collapsed"
        )

    if uploaded_file is not None:
        try:
            # Read uploaded file
            logger.info(f"File uploaded: {uploaded_file.name}")

            # Save uploaded file temporarily
            with open("temp_input.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Display success message
            st.markdown(f"""
                <div class="success-box">
                    ✅ <strong>File uploaded successfully:</strong> {uploaded_file.name}
                </div>
            """, unsafe_allow_html=True)

            # Display input preview
            st.markdown("---")
            st.markdown("### 📋 Input Data Preview")

            input_df = pd.read_csv("temp_input.csv")
            n_faculties = len(input_df.columns) - 4

            # Display metrics in columns
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                display_animated_metric("Total Students", len(input_df), "👥")
            with col2:
                display_animated_metric("Faculties", n_faculties, "👨‍🏫")
            with col3:
                avg_cgpa = input_df['CGPA'].mean()
                display_animated_metric("Avg CGPA", f"{avg_cgpa:.2f}", "📊")
            with col4:
                max_cgpa = input_df['CGPA'].max()
                display_animated_metric("Max CGPA", f"{max_cgpa:.2f}", "🏆")

            st.markdown("")

            # Display data table with custom styling
            with st.expander("📊 View Full Input Data", expanded=False):
                st.dataframe(
                    input_df,
                    use_container_width=True,
                    height=400
                )

            # Display sample data
            st.markdown("#### 👀 Sample Preview (Top 10 Students)")
            st.dataframe(
                input_df.head(10).style.background_gradient(subset=['CGPA'], cmap='RdYlGn'),
                use_container_width=True
            )

            st.markdown("---")

            # Process button with centered layout
            col1, col2, col3 = st.columns([1, 1, 1])

            with col2:
                if st.button("🚀 Run Allocation", type="primary", use_container_width=True):
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    status_text.markdown("🔄 Initializing allocation process...")
                    progress_bar.progress(20)
                    time.sleep(0.3)

                    try:
                        # Run allocation
                        status_text.markdown("📊 Sorting students by CGPA...")
                        progress_bar.progress(40)
                        time.sleep(0.3)

                        status_text.markdown("🔄 Running round-robin allocation...")
                        progress_bar.progress(60)

                        logger.info("Starting allocation process")
                        allocation_df, pref_stats_df = allocate_students("temp_input.csv")

                        progress_bar.progress(80)
                        status_text.markdown("💾 Saving results...")
                        time.sleep(0.2)

                        # Store in session state
                        st.session_state['allocation_df'] = allocation_df
                        st.session_state['pref_stats_df'] = pref_stats_df

                        progress_bar.progress(100)
                        status_text.markdown("")

                        # Success message with animation
                        # st.balloons()
                        st.markdown("""
                            <div class="success-box">
                                ✅ <strong>Allocation completed successfully!</strong><br>
                                All students have been allocated to faculties.
                            </div>
                        """, unsafe_allow_html=True)

                        logger.info("Allocation completed successfully")

                    except Exception as e:
                        progress_bar.empty()
                        status_text.markdown("")
                        st.markdown(f"""
                            <div class="warning-box">
                                ❌ <strong>Error during allocation:</strong> {str(e)}
                            </div>
                        """, unsafe_allow_html=True)
                        logger.error(f"Allocation failed: {str(e)}")

        except Exception as e:
            st.markdown(f"""
                <div class="warning-box">
                    ❌ <strong>Error reading file:</strong> {str(e)}
                </div>
            """, unsafe_allow_html=True)
            logger.error(f"File reading failed: {str(e)}")

    else:
        # Show welcome message when no file is uploaded
        st.markdown("""
            <div class="info-box">
                📤 <strong>Please upload a CSV file to begin</strong><br>
                Use the file uploader above to select your student preference file.
            </div>
        """, unsafe_allow_html=True)

    # Display results if available
    if 'allocation_df' in st.session_state and 'pref_stats_df' in st.session_state:
        st.markdown("---")
        st.markdown("## 📊 Allocation Results & Analytics")

        allocation_df = st.session_state['allocation_df']
        pref_stats_df = st.session_state['pref_stats_df']

        # Summary metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            display_animated_metric("Total Allocated", len(allocation_df), "✅")
        with col2:
            highest_cgpa = allocation_df['CGPA'].max()
            display_animated_metric("Highest CGPA", f"{highest_cgpa:.2f}", "🏆")
        with col3:
            lowest_cgpa = allocation_df['CGPA'].min()
            display_animated_metric("Lowest CGPA", f"{lowest_cgpa:.2f}", "📉")
        with col4:
            unallocated = len(allocation_df[allocation_df['Allocated'] == 'UNALLOCATED'])
            display_animated_metric("Unallocated", unallocated, "⚠️")
        with col5:
            faculties = allocation_df['Allocated'].nunique()
            display_animated_metric("Active Faculties", faculties, "👨‍🏫")

        st.markdown("")

        # Tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👥 Student Allocation",
            "📊 Distribution Charts",
            "📈 Preference Statistics",
            "🔍 Detailed Analysis",
            "📥 Download Files"
        ])

        with tab1:
            st.markdown("### 🎯 Student-Faculty Allocation Table")

            # Search functionality
            search_col1, search_col2 = st.columns([2, 1])
            with search_col1:
                search_term = st.text_input("🔍 Search by Name, Roll, or Faculty", "")

            # Filter dataframe
            if search_term:
                filtered_df = allocation_df[
                    allocation_df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
                ]
                st.info(f"Found {len(filtered_df)} matching records")
            else:
                filtered_df = allocation_df

            # Display allocation table with gradient
            st.dataframe(
                filtered_df.style.background_gradient(subset=['CGPA'], cmap='RdYlGn'),
                use_container_width=True,
                height=500
            )

            # Faculty-wise student count
            st.markdown("### 📊 Faculty-wise Student Count")
            fac_counts = allocation_df['Allocated'].value_counts().sort_index()

            count_df = pd.DataFrame({
                'Faculty': fac_counts.index,
                'Student Count': fac_counts.values
            })

            st.dataframe(
                count_df.style.background_gradient(subset=['Student Count'], cmap='Blues'),
                use_container_width=True
            )

        with tab2:
            st.markdown("### 📊 Interactive Distribution Charts")

            # Faculty distribution bar chart
            st.plotly_chart(create_distribution_chart(allocation_df), use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                # Pie chart
                st.plotly_chart(create_faculty_allocation_chart(allocation_df), use_container_width=True)

            with col2:
                # CGPA distribution
                st.plotly_chart(create_cgpa_distribution_chart(allocation_df), use_container_width=True)

        with tab3:
            st.markdown("### 📈 Faculty Preference Statistics")

            st.markdown("""
                <div class="info-box">
                    ℹ️ <strong>Understanding the Heatmap:</strong><br>
                    - Each row represents a faculty<br>
                    - Each column represents a preference level (P1 = 1st preference, P2 = 2nd, etc.)<br>
                    - Values show how many students got that faculty at that preference level<br>
                    - Darker colors indicate more students
                </div>
            """, unsafe_allow_html=True)

            # Preference heatmap
            st.plotly_chart(create_preference_heatmap(pref_stats_df), use_container_width=True)

            # Statistics table
            st.markdown("### 📋 Detailed Preference Statistics Table")
            st.dataframe(pref_stats_df, use_container_width=True, height=400)

        with tab4:
            st.markdown("### 🔍 Detailed Allocation Analysis")

            # CGPA-based analysis
            st.markdown("#### 📊 CGPA-based Student Categories")

            high_cgpa = len(allocation_df[allocation_df['CGPA'] >= 8.5])
            mid_cgpa = len(allocation_df[(allocation_df['CGPA'] >= 7.0) & (allocation_df['CGPA'] < 8.5)])
            low_cgpa = len(allocation_df[allocation_df['CGPA'] < 7.0])

            col1, col2, col3 = st.columns(3)

            with col1:
                display_animated_metric("High CGPA (≥8.5)", high_cgpa, "🌟")
            with col2:
                display_animated_metric("Mid CGPA (7.0-8.5)", mid_cgpa, "⭐")
            with col3:
                display_animated_metric("Below 7.0", low_cgpa, "📝")

            st.markdown("")

            # Top and bottom students
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🏆 Top 10 Students (by CGPA)")
                top_students = allocation_df.nlargest(10, 'CGPA')[['Name', 'CGPA', 'Allocated']]
                st.dataframe(
                    top_students.style.background_gradient(subset=['CGPA'], cmap='Greens'),
                    use_container_width=True
                )

            with col2:
                st.markdown("#### 📋 Bottom 10 Students (by CGPA)")
                bottom_students = allocation_df.nsmallest(10, 'CGPA')[['Name', 'CGPA', 'Allocated']]
                st.dataframe(
                    bottom_students.style.background_gradient(subset=['CGPA'], cmap='Reds'),
                    use_container_width=True
                )

            # Faculty load analysis
            st.markdown("#### ⚖️ Faculty Load Balance Analysis")

            fac_counts = allocation_df['Allocated'].value_counts()
            max_load = fac_counts.max()
            min_load = fac_counts.min()
            avg_load = fac_counts.mean()

            col1, col2, col3 = st.columns(3)

            with col1:
                display_animated_metric("Max Load", int(max_load), "📈")
            with col2:
                display_animated_metric("Min Load", int(min_load), "📉")
            with col3:
                display_animated_metric("Avg Load", f"{avg_load:.1f}", "⚖️")

            if max_load - min_load <= 1:
                st.markdown("""
                    <div class="success-box">
                        ✅ <strong>Excellent Balance!</strong><br>
                        The load difference between faculties is minimal (≤1 student).<br>
                        This indicates optimal fair distribution.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="info-box">
                        ℹ️ <strong>Load Variation Detected</strong><br>
                        Some faculties have more students than others.<br>
                        This is normal when student count doesn't divide evenly by faculty count.
                    </div>
                """, unsafe_allow_html=True)

        with tab5:
            st.markdown("### 📥 Download Output Files")

            st.markdown("""
                <div class="info-box">
                    💾 <strong>Ready to Download</strong><br>
                    Your allocation results are ready. Download the CSV files below.
                </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                # Download allocation CSV
                allocation_csv = allocation_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Student Allocation CSV",
                    data=allocation_csv,
                    file_name="output_btp_mtp_allocation.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.markdown("")

                # Download preference stats CSV
                pref_stats_csv = pref_stats_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Preference Statistics CSV",
                    data=pref_stats_csv,
                    file_name="fac_preference_count.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.markdown("")

            # Preview of downloadable files
            with st.expander("👁️ Preview: Student Allocation File"):
                st.dataframe(allocation_df.head(20), use_container_width=True)

            with st.expander("👁️ Preview: Preference Statistics File"):
                st.dataframe(pref_stats_df, use_container_width=True)

    # Footer


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application crashed: {str(e)}")
