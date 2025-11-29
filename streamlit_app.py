import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import altair as alt
from datetime import datetime
import time

# --- YAHAN NAYE FILES IMPORT KIYE HAIN ---
import flipkart_handler  # Token ke liye
import sku_mapping       # Design/Color/Size ke liye

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="SDK FASHION Manager", layout="wide")
DB_FILE = "order.db"

def process_sku_data(df):
    """
    IMP: Yeh function SKU se Design, Color, Size nikalta hai.
    """
    if df.empty or 'sku' not in df.columns:
        return df

    try:
        details = df['sku'].apply(lambda x: sku_mapping.get_sku_details(x)[0])
        
        # Dictionary ko Columns me badalna
        details_df = pd.DataFrame(details.tolist())
        
        # Main Dataframe me columns jodna
        df['design'] = details_df['design']
        df['color'] = details_df['color']
        df['size'] = details_df['size']
    except Exception as e:
        st.error(f"Mapping Error: {e}")
    
    return df

def load_data():
    """Database se data lana aur process karna"""
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql("SELECT * FROM orders", conn)
        
        # Dates fix karna
        df['orderDate'] = pd.to_datetime(df['orderDate'], errors='coerce')
        df['dispatchByDate'] = pd.to_datetime(df['dispatchByDate'], errors='coerce')
        
        # SKU Mapping Call karna
        df = process_sku_data(df)
        
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# --- 3. UI SECTIONS ---

def show_dashboard(df):
    st.title("SDK FASHION Dashboard")
    
    if df.empty:
        st.warning("No Data found in database.")
        return

    # Metrics
    total_sales = df['customerPrice'].sum() if 'customerPrice' in df.columns else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"₹{total_sales:,.0f}")
    c2.metric("Total Orders", len(df))
    pending = len(df[~df['status'].isin(['DELIVERED', 'CANCELLED'])]) if 'status' in df.columns else 0
    c3.metric("Pending Orders", pending)
    
    st.divider()

    # --- TOP STATIC CHARTS ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎨 Sales by Color")
        if 'color' in df.columns:
            fig = px.pie(df, names='color', values='quantity', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("👕 Sales by Design")
        if 'design' in df.columns:
            design_counts = df.groupby('design')['quantity'].sum().reset_index().sort_values('quantity', ascending=False)
            fig = px.bar(design_counts, x='design', y='quantity', color='design')
            st.plotly_chart(fig, use_container_width=True)

    # --- INTERACTIVE DRILL-DOWN CHART ---
    st.divider()
    st.subheader("🔍 Interactive Trend (Click to Expand)")

    if 'orderDate' in df.columns and 'design' in df.columns:
        # 1. State Management
        if 'drill_level' not in st.session_state:
            st.session_state.drill_level = 'Design' # Levels: Design -> Color -> Size
            st.session_state.sel_design = None
            st.session_state.sel_color = None

        # 2. Back Button Logic
        if st.session_state.drill_level != 'Design':
            if st.button("⬅️ Back to All Designs"):
                st.session_state.drill_level = 'Design'
                st.session_state.sel_design = None
                st.session_state.sel_color = None
                st.rerun()

        # 3. Filter Data
        chart_data = df.copy()
        # FIX: Date formatting clean rakhi taaki chart sahi se samjhe
        chart_data['short_date'] = chart_data['orderDate'].dt.strftime('%Y-%m-%d')
        chart_data['quantity'] = pd.to_numeric(chart_data['quantity']).fillna(0)
        
        current_level = st.session_state.drill_level
        group_col = 'design' # Default
        
        # Logic to Filter Data based on drill level
        if current_level == 'Design':
            group_col = 'design'
            title_text = "Step 1: Click a Design bar to see Colors"
        elif current_level == 'Color':
            chart_data = chart_data[chart_data['design'] == st.session_state.sel_design]
            group_col = 'color'
            title_text = f"Step 2: Sales for '{st.session_state.sel_design}' (Click Color to see Sizes)"
        elif current_level == 'Size':
            chart_data = chart_data[chart_data['design'] == st.session_state.sel_design]
            chart_data = chart_data[chart_data['color'] == st.session_state.sel_color]
            group_col = 'size'
            title_text = f"Step 3: Sales for '{st.session_state.sel_design} - {st.session_state.sel_color}'"

        # 4. Aggregate Data
        final_chart_df = chart_data.groupby(['short_date', group_col])['quantity'].sum().reset_index()

        if not final_chart_df.empty:
            # 5. Create Chart (FIXED: Explicit Selection in Altair)
            
            # Hum ek "Selection Point" bana rahe hain jo "group_col" (Design/Color) par kaam karega
            click_selection = alt.selection_point(fields=[group_col], name='click_select')
            
            base_chart = alt.Chart(final_chart_df).encode(
                x=alt.X('short_date:O', title='Date'),
                y=alt.Y('quantity:Q', title='Quantity'),
                color=alt.Color(f'{group_col}:N', title=current_level, legend=alt.Legend(orient='bottom')),
                tooltip=['short_date', group_col, 'quantity'],
                # Highlight logic: Select kiya hua bright dikhega, baaki dull
                opacity=alt.condition(click_selection, alt.value(1), alt.value(0.3))
            ).add_params(click_selection) # <-- IMP: Parameter yahan add kiya
            
            chart = base_chart.mark_bar().properties(
                title=title_text,
                height=400
            )

            # 6. Capture Click Event
            # 'selection_mode' hata diya kyunki humne upar manually selection define kar diya hai
            event = st.altair_chart(chart, use_container_width=True, on_select="rerun")

            # 7. Handle Drill-down Logic
            # Ab hum event.selection dictionary se apna 'click_select' dhoondhenge
            if event.selection:
                # Selection dictionary kuch aisi dikhti hai: {'click_select': [{'design': '188M'}]}
                # Hum pehla key (param name) uthayenge
                param_name = list(event.selection.keys())[0]
                selection_data = event.selection[param_name]
                
                if selection_data and len(selection_data) > 0:
                    # Data list of dicts hoti hai, pehla item uthaya
                    clicked_value = selection_data[0].get(group_col)

                    if clicked_value:
                        # Logic to go deeper
                        if current_level == 'Design':
                            st.session_state.sel_design = clicked_value
                            st.session_state.drill_level = 'Color'
                            st.rerun()
                        elif current_level == 'Color':
                            st.session_state.sel_color = clicked_value
                            st.session_state.drill_level = 'Size'
                            st.rerun()
        else:
            st.warning("No data available for this selection.")

    # --- NEW TABLES SECTION ---
    st.divider()
    st.header("📋 Detailed Order Analysis")
    
    # 1. Date Filter Logic for Tables
    st.subheader("1. Date Selection")
    
    # Min/Max date nikalenge database se
    if 'orderDate' in df.columns:
        min_date = df['orderDate'].min().date()
        max_date = df['orderDate'].max().date()
        
        c_d1, c_d2 = st.columns(2)
        start_date = c_d1.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
        end_date = c_d2.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
        
        # Filter Data based on selection
        mask = (df['orderDate'].dt.date >= start_date) & (df['orderDate'].dt.date <= end_date)
        table_df = df.loc[mask]
    else:
        table_df = df
        st.warning("Date column missing, showing all data.")

    st.divider()
    
    # --- TABLE 1: HIERARCHICAL VIEW (Collapsible) ---
    st.subheader("📂 1. Hierarchical Breakdown (Design > Color > Size)")
    
    if not table_df.empty and 'design' in table_df.columns:
        # Group by Design first
        design_groups = table_df.groupby('design')
        
        for design_name, design_data in design_groups:
            total_qty = design_data['quantity'].sum()
            
            # Top Level Expander (Design)
            with st.expander(f"📦 {design_name} (Total Qty: {total_qty})"):
                
                # Internal View: Colors
                color_groups = design_data.groupby('color')
                
                # Hum columns bana ke dikhayenge taaki clean lage
                for color_name, color_data in color_groups:
                    c_qty = color_data['quantity'].sum()
                    st.markdown(f"**🎨 Color: {color_name} (Qty: {c_qty})**")
                    
                    # Lowest Level: Sizes (Table format me)
                    size_counts = color_data.groupby('size')['quantity'].sum().reset_index()
                    # Transpose karke horizontal dikhayenge taaki jagah kam le
                    st.dataframe(size_counts.set_index('size').T, use_container_width=True)
    else:
        st.info("No data for selected range.")

    st.divider()

    # --- TABLE 2: SIZE MATRIX (Row: Design_Color, Col: Size) ---
    st.subheader("🔢 2. Size Matrix (Total Breakdown)")
    
    if not table_df.empty and 'design' in table_df.columns:
        # Create unique row identifier
        matrix_df = table_df.copy()
        matrix_df['Design_Color'] = matrix_df['design'] + ' - ' + matrix_df['color']
        
        # Create Pivot Table with Margins (Totals)
        pivot_matrix = matrix_df.pivot_table(
            index='Design_Color', 
            columns='size', 
            values='quantity', 
            aggfunc='sum', 
            fill_value=0, 
            margins=True, 
            margins_name='Total'
        )
        
        # Display
        st.dataframe(pivot_matrix, use_container_width=True, height=500)
    else:
        st.info("No data for matrix.")

def show_pivot_analysis(df):
    st.title("📈 Custom Reports")
    
    if df.empty:
        st.info("No data.")
        return

    st.markdown("Select **Design, Color, or Size** to analyze:")
    
    c1, c2, c3 = st.columns(3)
    group_options = ['design', 'color', 'size', 'sku', 'status', 'state']
    
    with c1:
        row_group = st.selectbox("Group By", group_options, index=0)
    with c2:
        val_group = st.selectbox("Value", ['quantity', 'customerPrice'], index=0)
    with c3:
        chart_type = st.selectbox("Chart Type", ['Bar Chart', 'Line Chart', 'Pie Chart'])

    if row_group in df.columns:
        pivot_table = df.pivot_table(index=row_group, values=val_group, aggfunc='sum').reset_index()
        pivot_table = pivot_table.sort_values(by=val_group, ascending=False)
        
        st.dataframe(pivot_table, use_container_width=True)
        
        if chart_type == 'Bar Chart':
            st.plotly_chart(px.bar(pivot_table, x=row_group, y=val_group, color=row_group), use_container_width=True)
        elif chart_type == 'Pie Chart':
            st.plotly_chart(px.pie(pivot_table, names=row_group, values=val_group), use_container_width=True)
        elif chart_type == 'Line Chart':
            st.plotly_chart(px.line(pivot_table, x=row_group, y=val_group), use_container_width=True)

def show_data_management(df):
    st.title("🔄 Sync Data & Mapping Helper")
    
    # Placeholder for Real API Sync
    # Future me yahan Flipkart API button aayega
    st.info("Real API Sync will be implemented here.")

    st.divider()
    st.markdown("### Raw Database View")
    st.dataframe(df.head(50), use_container_width=True)
    st.subheader("⚠️ Missing Mappings")
    
    if 'design' in df.columns:
        unmapped_df = df[df['design'] == 'Unmapped']
        if not unmapped_df.empty:
            st.warning(f"Found {len(unmapped_df['sku'].unique())} SKUs jo mapping file mein nahi hain!")
            missing_skus = unmapped_df['sku'].unique()
            code_snippet = ""
            for sku in missing_skus:
                code_snippet += f"'{sku}': {{'design': 'TODO', 'color': 'TODO', 'size': 'TODO'}},\n"
            st.markdown("Is code ko copy karke `sku_mapping.py` mein paste karein:")
            st.code(code_snippet, language='python')
        else:
            st.success("Badhai ho! Saare SKUs mapped hain. ✅")
            
    st.divider()
    

# --- 4. MAIN EXECUTION ---
def main():
    
    with st.sidebar:
        st.header("Token:")
        
        is_connected = flipkart_handler.get_saved_token() is not None
        status_icon = "✅" if is_connected else "❌"
        st.caption(f"API Connection: {status_icon}")
        
        # --- FIX: Message Placeholder ---
        status_placeholder = st.empty()

        if st.button("🔄 Refresh Token"):
            status_placeholder.info("⏳ Connecting to Flipkart...")
            # Capture Token Response
            new_token = flipkart_handler.generate_and_save_token()
            
            if new_token:
                status_placeholder.success("Token Updated! ✅")
                time.sleep(1) # Visual Delay (1s) taaki user message padh sake
                st.rerun()
            else:
                status_placeholder.error("Failed to Refresh Token ❌")
            
        st.divider()
        menu = st.radio("Menu", ["Dashboard", "Reports", "Sync Data"])

    df = load_data()
    
    if menu == "Dashboard":
        show_dashboard(df)
    elif menu == "Reports":
        show_pivot_analysis(df)
    elif menu == "Sync Data":
        show_data_management(df)

if __name__ == "__main__":
    main()
