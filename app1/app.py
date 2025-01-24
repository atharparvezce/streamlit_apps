import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# App Title
st.title("Data Analysis App")

# Subheader
st.subheader("This is a simple data analysis app created by Athar")

# Horizontal divider
st.write("---")

# Predefined datasets
datasets = {
    'tips': sns.load_dataset('tips'),
    'titanic': sns.load_dataset('titanic'),
    'iris': sns.load_dataset('iris')
}

# Dropdown to select predefined dataset
selected_dataset = st.selectbox(
    "Select a predefined dataset:",
    options=list(datasets.keys()),
    help="Choose a dataset to analyze"
)

# Section for uploading custom dataset
st.write("---")
st.header("Upload Your Own Dataset")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], help="Upload your own dataset in CSV format")

# Use session state to clear custom dataset when dropdown dataset is selected
if selected_dataset != "Select a predefined dataset" and uploaded_file is not None:
    st.session_state.uploaded_file = None  # Reset the custom dataset if dropdown dataset is selected

# Function to display dataset details
def display_dataset_details(dataframe):
    st.write("### Dataset Overview")
    st.dataframe(dataframe)  # Display the dataset

    # Display dataset metadata
    st.write(f"**Number of Rows:** {dataframe.shape[0]}")
    st.write(f"**Number of Columns:** {dataframe.shape[1]}")

    # Prepare column names, data types, and null value counts
    st.write("### Column Names, Data Types, and Null Values")
    
    column_info = pd.DataFrame({
        "Column Name": dataframe.columns,
        "Data Type": dataframe.dtypes.astype(str),
        "Null Values": dataframe.isnull().sum()
    })
    
    # If any column does not have null values, set the count to zero
    column_info["Null Values"] = column_info["Null Values"].apply(lambda x: x if x > 0 else 0)
    
    # Sort by 'Null Values' in descending order
    column_info = column_info.sort_values(by="Null Values", ascending=False)

    # Display the information in a table
    st.dataframe(column_info)

    # Display summary statistics
    st.write("### Summary Statistics")
    summary_stats = dataframe.describe()  # Get summary statistics
    st.dataframe(summary_stats)

# Function for plotting based on user selection
def plot_data(dataframe, x_col, y_col, plot_type):
    # Create the figure and axes
    fig, ax = plt.subplots(figsize=(8, 6))
    
    if plot_type == 'Line':
        st.write(f"### Line Plot between {x_col} and {y_col}")
        sns.lineplot(data=dataframe, x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)
    
    elif plot_type == 'Scatter':
        st.write(f"### Scatter Plot between {x_col} and {y_col}")
        sns.scatterplot(data=dataframe, x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)

    elif plot_type == 'Bar':
        st.write(f"### Bar Plot between {x_col} and {y_col}")
        sns.barplot(data=dataframe, x=x_col, y=y_col, ax=ax)
        st.pyplot(fig)

    elif plot_type == 'Histogram':
        st.write(f"### Histogram for {x_col}")
        sns.histplot(data=dataframe, x=x_col, kde=True, ax=ax)
        st.pyplot(fig)

    elif plot_type == 'Box':
        st.write(f"### Box Plot for {x_col}")
        sns.boxplot(data=dataframe, x=x_col, ax=ax)
        st.pyplot(fig)

    elif plot_type == 'KDE':
        st.write(f"### KDE Plot for {x_col}")
        sns.kdeplot(data=dataframe, x=x_col, ax=ax)
        st.pyplot(fig)

# Function to plot pairplot with selected hue column
def pairplot_with_hue(dataframe, hue_col):
    st.write(f"### Pairplot with Hue: {hue_col}")
    # Create the pairplot with hue
    pairplot = sns.pairplot(dataframe, hue=hue_col)
    st.pyplot(pairplot.fig)

# Function to plot the heatmap for numeric columns
def plot_heatmap(dataframe):
    # Select only numeric columns
    numeric_cols = dataframe.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 1:
        st.write(f"### Heatmap for Numeric Columns")
        # Compute the correlation matrix
        corr = dataframe[numeric_cols].corr()
        
        # Create the heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, linewidths=0.5, cbar_kws={'shrink': 0.8})
        st.pyplot(fig)
    else:
        st.write("### Heatmap cannot be generated with less than two numeric columns")

# Logic to display only one dataset at a time
if uploaded_file is not None:
    # If custom dataset is uploaded
    custom_df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Custom Dataset")
    display_dataset_details(custom_df)

    # Ask user to select X and Y columns
    x_column = st.selectbox("Select the X column", custom_df.columns)
    y_column = st.selectbox("Select the Y column", custom_df.columns)
    
    # Ask user to choose plot type
    plot_type = st.selectbox("Select the type of plot", ['Line', 'Scatter', 'Bar', 'Histogram', 'Box', 'KDE'])
    
    # Display plot
    plot_data(custom_df, x_column, y_column, plot_type)

    # Option to select a column to be used as hue for pairplot
    hue_column = st.selectbox("Select a column for hue (color differentiation)", custom_df.columns)
    if st.button("Generate Pairplot"):
        pairplot_with_hue(custom_df, hue_column)

    # Generate heatmap for numeric columns
    if st.button("Generate Heatmap for Numeric Columns"):
        plot_heatmap(custom_df)

else:
    # If predefined dataset is selected
    st.write(f"### Selected Dataset: {selected_dataset}")
    df = datasets[selected_dataset]
    display_dataset_details(df)

    # Ask user to select X and Y columns
    x_column = st.selectbox("Select the X column", df.columns)
    y_column = st.selectbox("Select the Y column", df.columns)
    
    # Ask user to choose plot type
    plot_type = st.selectbox("Select the type of plot", ['Line', 'Scatter', 'Bar', 'Histogram', 'Box', 'KDE'])
    
    # Display plot
    plot_data(df, x_column, y_column, plot_type)

    # Option to select a column to be used as hue for pairplot
    hue_column = st.selectbox("Select a column for hue (color differentiation)", df.columns)
    if st.button("Generate Pairplot"):
        pairplot_with_hue(df, hue_column)

    # Create a separate frame for the heatmap
    st.write("---")
    st.header("Generate Heatmap for Numeric Columns")
    if st.button("Generate Heatmap for Numeric Columns"):
        plot_heatmap(df)
