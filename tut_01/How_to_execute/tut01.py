import streamlit as st
import pandas as pd
import os
import shutil
import zipfile
from collections import deque
from io import BytesIO
import contextlib

def unique_branch(df, base_dir):
    output_dir = os.path.join(base_dir, "full_branchwise")
    os.makedirs(output_dir, exist_ok=True)
    for branch in df['Branch'].unique():
        branch_df = df[df['Branch'] == branch]
        branch_df.drop(columns=['Branch']).to_csv(os.path.join(output_dir, f"{branch}.csv"), index=False)
    return output_dir

def branch_mix(df, N, base_dir):
    output_dir = os.path.join(base_dir, "group_branch_wise_mix")
    os.makedirs(output_dir, exist_ok=True)

    total_students = len(df)
    q, r = divmod(total_students, N)
    group_sizes = [q + 1] * r + [q] * (N - r)

    branches = {branch: deque(df[df['Branch'] == branch].to_dict('records'))
                for branch in df['Branch'].unique()}

    groups = []
    branch_order = list(branches.keys())

    for g in range(N):
        group = []
        while len(group) < group_sizes[g] and any(branches.values()):
            for branch in branch_order:
                if branches[branch] and len(group) < group_sizes[g]:
                    student = branches[branch].popleft()
                    group.append(student)
        groups.append(group)

    for idx, group in enumerate(groups, start=1):
        gdf = pd.DataFrame(group).drop(columns=['Branch'])
        gdf.to_csv(os.path.join(output_dir, f"g{idx}.csv"), index=False)

    return output_dir


def uniform_mix(df, N, base_dir):
    output_dir = os.path.join(base_dir, "group_uniform_mix")
    os.makedirs(output_dir, exist_ok=True)

    total_students = len(df)
    q, r = divmod(total_students, N)
    group_sizes = [q + 1] * r + [q] * (N - r)

    branch_students = {b: deque(g.to_dict('records')) for b, g in df.groupby('Branch')}

    groups = []
    for size in group_sizes:
        group = []
        remaining = size
        while remaining > 0 and branch_students:
            branch = max(branch_students.keys(), key=lambda b: (len(branch_students[b]), b))
            take = min(len(branch_students[branch]), remaining)
            for _ in range(take):
                group.append(branch_students[branch].popleft())
            remaining -= take
            if not branch_students[branch]:
                del branch_students[branch]
        groups.append(group)

    for idx, group in enumerate(groups, start=1):
        gdf = pd.DataFrame(group).drop(columns=['Branch']) if group else pd.DataFrame(columns=df.columns)
        gdf.to_csv(os.path.join(output_dir, f"g{idx}.csv"), index=False)

    return output_dir


def export_summary(mix_path, uniform_path, out_file):
    def summarize(input_dir):
        rows = []
        for file in sorted(os.listdir(input_dir)):
            if file.endswith(".csv"):
                group_name = os.path.splitext(file)[0]
                df = pd.read_csv(os.path.join(input_dir, file))
                if df.empty:
                    continue
                df['Branch'] = df['Roll'].astype(str).str[4:6]
                counts = df['Branch'].value_counts().to_dict()
                row = {"Group": group_name}
                row.update(counts)
                rows.append(row)

        if not rows:
            return pd.DataFrame([{"Group": "No data"}]) 

        df_sum = pd.DataFrame(rows).fillna(0)
        for col in df_sum.columns:
            if col != "Group":
                df_sum[col] = df_sum[col].astype(int)

        branch_cols = [c for c in df_sum.columns if c != "Group"]
        df_sum["Total"] = df_sum[branch_cols].sum(axis=1)

        return df_sum

    with contextlib.suppress(IndexError):
        with pd.ExcelWriter(out_file, engine="openpyxl", mode="w") as writer:
            df1 = summarize(mix_path)
            df2 = summarize(uniform_path)
            df1.to_excel(writer, sheet_name="Branchwise_Mix", index=False)
            df2.to_excel(writer, sheet_name="Uniform_Mix", index=False)

    return out_file



def make_zip(base_dir):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for root, _, files in os.walk(base_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, base_dir)
                zf.write(filepath, arcname)
    zip_buffer.seek(0)
    return zip_buffer
st.title("Tut01")

uploaded_file = st.file_uploader("Upload Input File", type=["xlsx"])
N = st.number_input("Enter number of groups", min_value=1, step=1, value=2)

if uploaded_file:
    if st.button("Process"):
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        if 'Unique' in df.columns:
            df = df.drop(columns=['Unique'])
        df['Branch'] = df['Roll'].astype(str).str[4:6]

        base_dir = "outputs"
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir, exist_ok=True)
        unique_branch(df, base_dir)
        mix_dir = branch_mix(df, N, base_dir)
        uniform_dir = uniform_mix(df, N, base_dir)
        summary_file = export_summary(mix_dir, uniform_dir, os.path.join(base_dir, "output.xlsx"))
        zip_file = make_zip(base_dir)

        st.success("Download ready!")
        st.download_button("Download ZIP", data=zip_file, file_name="tut01.zip", mime="application/zip")
