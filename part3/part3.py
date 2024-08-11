import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.nonparametric.smoothers_lowess import lowess

def categorize_subjects(subjects):
    """
    Categorize the subjects of a work into predefined categories based on keywords
    
    Args:
    subjects (str): A string containing subject keywords
    
    Returns:
    list: A list of categories the subjects fall into
    """
    try:
        # Handle cases where subjects might be missing or NaN
        if pd.isna(subjects):
            return []
        
        # Convert the subjects string to lowercase for case-insensitive matching
        subjects_lower = subjects.lower()
        categories = []
        
        # Mapping of categories to relevant keywords
        category_mapping = {
            "Business and Economics": [
                "business", "economic", "management", "decision support system"
            ],
            "Computer Vision and Image Processing": [
                "computer vision", "image processing", "optical pattern recognition", "computer imaging",
                "pattern perception", "pattern recognition", "image analysis", "imaging system"
            ],
            "Data Collection and Mining": [
                "data mining", "knowledge discovery", "big data"
            ],
            "Data Processing and Analysis": [
                "data processing", "data structure", "data encryption", "data protection"
            ],
            "Databases and Management": [
                "database"
            ],
            "Education and Learning": [
                "education", "computer-assisted instruction",
                "tutoring system", "learning", "teaching"
            ],
            "Healthcare and Medicine": [
                "medical", "diagnostic imaging", "health", "medical records"
            ],
            "Human-Computer Interaction and User Experience": [
                "human-computer", "user interface", "human-machine",
                "human information processing", "interactive computer system", "user-centered system design",
                "psychology", "psychological"
            ],
            "Information Systems and Technology": [
                "information", "multimedia system", "web services"
            ],
            "Natural Language Processing and Linguistics": [
                "NLP", "psycholinguistics", "language", "linguistics", "discourse analysis", "semantics", "syntax",
                "text processing", "conceptual structures"
            ],
            "Neural Networks and Evolutionary Computation": [
                "neural", "genetic algorithm", "evolution"
            ],
            "Philosophy and Ethics": [
                "philosophy", "cognitive science", "consciousness", "ethic", "moral"
            ],
            "Robotics and Automation": [
                "robotic", "robot", "intelligent control systems", "automation", "control system", "control theory"
            ],
            "Science Fiction and Literature": [
                "fiction", "thrillers", "suspense"
            ],
            "Security and Privacy": [
                "security", "encryption", "biometric identification", "privacy"
            ]
        }
        
        # Check each category to see if any keyword matches the subjects string
        for category, keywords in category_mapping.items():
            if any(keyword in subjects_lower for keyword in keywords):
                categories.append(category)
        
        return categories
    
    except Exception as e:
        print(f"Error in categorize_subjects: {str(e)}")
        return []

# Defining chart colours and hatches for each category
category_styles = {
    "Business and Economics": {"color": "#A9A9A9", "hatch": ""},  # Dark Gray
    "Computer Vision and Image Processing": {"color": "#A9A9A9", "hatch": "///"},
    "Data Collection and Mining": {"color": "#B0C4DE", "hatch": ""},  # Light Steel Blue
    "Data Processing and Analysis": {"color": "#B0C4DE", "hatch": "..."},
    "Databases and Management": {"color": "#4682B4", "hatch": ""},  # Steel Blue
    "Education and Learning": {"color": "#4682B4", "hatch": "--"},
    "Healthcare and Medicine": {"color": "#5F9EA0", "hatch": ""},  # Cadet Blue
    "Human-Computer Interaction and User Experience": {"color": "#5F9EA0", "hatch": "\\\\\\"},
    "Information Systems and Technology": {"color": "#1E90FF", "hatch": ""},  # Dodger Blue
    "Natural Language Processing and Linguistics": {"color": "#1E90FF", "hatch": "///"},  
    "Neural Networks and Evolutionary Computation": {"color": "#3CB371", "hatch": ""},  # Medium Sea Green
    "Philosophy and Ethics": {"color": "#3CB371", "hatch": "..."}, 
    "Robotics and Automation": {"color": "#556B2F", "hatch": ""},  # Dark Olive Green
    "Science Fiction and Literature": {"color": "#556B2F", "hatch": "--"},
    "Security and Privacy": {"color": "#B0E0E6", "hatch": ""}  # Powder Blue
}

def create_count_area_chart(df, start_year, end_year, filename):
    """
    Create and save a count-based area chart showing the number of works published over time
    
    Args:
    df (DataFrame): The input dataframe containing publication data
    start_year (int): The start year for the chart
    end_year (int): The end year for the chart
    filename (str): The filename to save the chart
    """
    try:
        # Filter the dataframe for the specified year range
        df_filtered = df[(df['Publish Year'] >= start_year) & (df['Publish Year'] <= end_year)]
        # Group the data by year and category, then count occurrences
        yearly_counts = df_filtered.groupby(['Publish Year', 'Categories']).size().unstack(fill_value=0)
        # Ensure the dataframe is sorted by year and filled for missing years
        yearly_counts = yearly_counts.sort_index().reindex(range(start_year, end_year + 1), fill_value=0)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True) 

        # Initialize the plot
        plt.figure(figsize=(20, 10))
        sns.set_style("whitegrid")

        ax = plt.gca()

        # Extracts colours and hatches for categories
        colours = [category_styles[cat]["color"] for cat in yearly_counts.columns]
        hatches = [category_styles[cat]["hatch"] for cat in yearly_counts.columns]

        # Plot the area chart
        yearly_counts.plot(kind='area', stacked=True, ax=ax, color=colours, alpha=0.7)

        # Apply hatches and outline to each area
        for i, collection in enumerate(ax.collections):
            collection.set_hatch(hatches[i])
            collection.set_edgecolor('black')
            collection.set_linewidth(0.5)

        # Reverse legend to match the stacking order
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(reversed(handles), reversed(labels), title='Categories', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

        # Add chart title and labels
        plt.title(f'Distribution of Categories in Works related to Artificial Intelligence({start_year}-{end_year})', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Number of Works Published', fontsize=12)
        plt.xticks(range(start_year, end_year + 1, 5), rotation=45, fontsize=10)
        plt.yticks(fontsize=10)

        plt.tight_layout()

        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Count-based area chart has been saved at '{filename}'")

    except Exception as e:
        print(f"Error in create_count_area_chart: {str(e)}")

def create_percentage_area_chart(df, start_year, end_year, filename):
    """
    Create and save a percentage-based area chart showing the distribution of categories over time
    
    Args:
    df (DataFrame): The input dataframe containing publication data
    start_year (int): The start year for the chart
    end_year (int): The end year for the chart
    filename (str): The filename to save the chart
    """
    try:
        # Filter the dataframe for the specified year range
        df_filtered = df[(df['Publish Year'] >= start_year) & (df['Publish Year'] <= end_year)]
        # Group the data by year and category, then count occurrences
        yearly_counts = df_filtered.groupby(['Publish Year', 'Categories']).size().unstack(fill_value=0)
        # Ensure the dataframe is sorted by year and filled for missing years
        yearly_counts = yearly_counts.sort_index().reindex(range(start_year, end_year + 1), fill_value=0)
        
        # Calculate yearly percentages for each category
        yearly_percentages = yearly_counts.div(yearly_counts.sum(axis=1), axis=0) * 100

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Initialize the plot
        plt.figure(figsize=(20, 10))
        sns.set_style("whitegrid")

        ax = plt.gca()

        # Extract colours and hatches for categories
        colours = [category_styles[cat]["color"] for cat in yearly_percentages.columns]
        hatches = [category_styles[cat]["hatch"] for cat in yearly_percentages.columns]

        # Plot the percentage area chart
        yearly_percentages.plot(kind='area', stacked=True, ax=ax, color=colours, alpha=0.7)

        # Apply hatches and outline to each area
        for i, collection in enumerate(ax.collections):
            collection.set_hatch(hatches[i])
            collection.set_edgecolor('black')
            collection.set_linewidth(0.5)

        # Reverse legend to match the stacking order
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(reversed(handles), reversed(labels), title='Categories', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

        # Add chart title and labels
        plt.title(f'Percentage Distribution of Categories in Works related to Artificial Intelligence({start_year}-{end_year})', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Percentage of Works Published', fontsize=12)
        plt.xticks(range(start_year, end_year + 1, 5), rotation=45, fontsize=10)
        plt.yticks(fontsize=10)

        plt.tight_layout()

        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Percentage-based area chart has been saved at '{filename}'")
    
    except Exception as e:
        print(f"Error in create_percentage_area_chart: {str(e)}")

def create_line_chart(df, start_year, end_year, filename_prefix):
    """
    Create and save line charts for each category and an overall line chart showing trends over time
    
    Args:
    df (DataFrame): The input dataframe containing publication data
    start_year (int): The start year for the chart
    end_year (int): The end year for the chart
    filename_prefix (str): The prefix for the filenames to save the charts
    """
    try:
        # Filter the dataframe for the specified year range
        df_filtered = df[(df['Publish Year'] >= start_year) & (df['Publish Year'] <= end_year)]
        # Group the data by year and category, then count occurrences
        yearly_counts = df_filtered.groupby(['Publish Year', 'Categories']).size().unstack(fill_value=0)
        # Ensure the dataframe is sorted by year and filled for missing years
        yearly_counts = yearly_counts.sort_index().reindex(range(start_year, end_year + 1), fill_value=0)
        
        # Calculate yearly percentages for each category
        yearly_percentages = yearly_counts.div(yearly_counts.sum(axis=1), axis=0) * 100

        # Define base directory for saving charts
        base_dir = filename_prefix
        os.makedirs(base_dir, exist_ok=True) # Create directory if it doesn't exist

        # Create individual line charts for each category
        for category in yearly_percentages.columns:
            # Define directory for the category
            category_dir = os.path.join(base_dir, category.lower().replace(" ", "_").replace("-", "_"))
            os.makedirs(category_dir, exist_ok=True) # Create directory if it doesn't exist
            
            # Initialize the plot
            plt.figure(figsize=(20, 10))
            sns.set_style("whitegrid")
            
            # Plot percentage line for the category
            plt.plot(yearly_percentages.index, yearly_percentages[category], color=category_styles[category]["color"], linewidth=2)
            
            # Add chart title and labels
            plt.title(f'Percentage of Works Published in {category} ({start_year}-{end_year})', fontsize=16)
            plt.xlabel('Year', fontsize=12)
            plt.ylabel('Percentage of Works Published', fontsize=12)
            plt.xticks(range(start_year, end_year + 1, 5), rotation=45, fontsize=10)
            plt.yticks(fontsize=10)
            
            plt.tight_layout()
            
            filename = os.path.join(category_dir, f'percentage_line_chart_{category.lower().replace(" ", "_").replace("-", "_")}_{start_year}_{end_year}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Line chart for {category} has been saved at '{filename}'")

        # Create an overall line chart with all categories
        plt.figure(figsize=(20, 10))
        sns.set_style("whitegrid")
        
        # Plot percentage lines for all categories
        for category in yearly_percentages.columns:
            plt.plot(yearly_percentages.index, yearly_percentages[category], color=category_styles[category]["color"], linewidth=2, label=category)
        
        # Add chart title and labels
        plt.title(f'Percentage of Works Published in All Categories ({start_year}-{end_year})', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Percentage of Works Published', fontsize=12)
        plt.xticks(range(start_year, end_year + 1, 5), rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend(title='Categories', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
        
        plt.tight_layout()
        
        filename = os.path.join(base_dir, f'percentage_line_chart_all_categories_{start_year}_{end_year}.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Overall line chart has been saved at '{filename}'")

    except Exception as e:
        print(f"Error in create_line_chart: {str(e)}")

def create_trend_charts(df, start_year, end_year, filename_prefix):
    """
    Create and save trend charts for each category showing the trend lines over time
    
    Args:
    df (DataFrame): The input dataframe containing publication data
    start_year (int): The start year for the chart
    end_year (int): The end year for the chart
    filename_prefix (str): The prefix for the filenames to save the charts
    """
    try:
        # Filter the dataframe for the specified year range
        df_filtered = df[(df['Publish Year'] >= start_year) & (df['Publish Year'] <= end_year)]
        # Group the data by year and category, then count occurrences
        yearly_counts = df_filtered.groupby(['Publish Year', 'Categories']).size().unstack(fill_value=0)
        # Ensure the dataframe is sorted by year and filled for missing years
        yearly_counts = yearly_counts.sort_index().reindex(range(start_year, end_year + 1), fill_value=0)
        
        # Calculate yearly percentages for each category
        yearly_percentages = yearly_counts.div(yearly_counts.sum(axis=1), axis=0) * 100

        # Define base directory for saving trend charts
        base_dir = os.path.join(filename_prefix, 'trends')
        os.makedirs(base_dir, exist_ok=True) # Create directory if it doesn't exist

        # Create trend charts for each category
        for category in yearly_percentages.columns:
            # Define directory for the category
            category_dir = os.path.join(base_dir, category.lower().replace(" ", "_").replace("-", "_"))
            os.makedirs(category_dir, exist_ok=True) # Create directory if it doesn't exist
            
            # Initialize the plot
            plt.figure(figsize=(20, 10))
            sns.set_style("whitegrid")
            
            # Plot percentage line for the category
            x = yearly_percentages.index
            y = yearly_percentages[category]
            
            plt.plot(x, y, color=category_styles[category]["color"], linewidth=2)
            
            # Calculate and plot trend line using LOWESS smoothing
            first_non_zero = next((i for i, v in enumerate(y) if v > 0), len(y))
            
            if first_non_zero < len(y):
                x_trend = x[first_non_zero:]
                y_trend = y[first_non_zero:]
                
                # Apply LOWESS smoothing to the data
                z = lowess(y_trend, x_trend, frac=0.6667, it=5)
                
                # Plot the trend line
                plt.plot(z[:, 0], z[:, 1], "r--", linewidth=1)
            
            # Add chart title and labels
            plt.title(f'Percentage of Works Published in {category} with Trend ({start_year}-{end_year})', fontsize=16)
            plt.xlabel('Year', fontsize=12)
            plt.ylabel('Percentage of Works Published', fontsize=12)
            plt.xticks(range(start_year, end_year + 1, 5), rotation=45, fontsize=10)
            plt.yticks(fontsize=10)
            
            plt.tight_layout()
            
            filename = os.path.join(category_dir, f'trend_line_chart_{category.lower().replace(" ", "_").replace("-", "_")}_{start_year}_{end_year}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Trend line chart for {category} has been saved at '{filename}'")

    except Exception as e:
        print(f"Error in create_trend_charts: {str(e)}")

def main():
    """
    Main function to run the data processing and chart creation pipeline
    """
    try:
        # Read and preprocess the data from CSV
        df = pd.read_csv('part2/part2_dataset.csv')
        # Convert 'Publish Year' to numeric and filter for valid range
        df['Publish Year'] = pd.to_numeric(df['Publish Year'], errors='coerce')
        df = df[(df['Publish Year'] >= 1950) & (df['Publish Year'] <= 2024)]
        # Apply categorization to the 'Subjects' column
        df['Categories'] = df['Subjects'].apply(categorize_subjects)
        # Explode the dataframe to have one category per row
        df = df.explode('Categories')

        # Define time periods for analysis
        time_periods = [(1950, 1982), (1950, 2012), (1950, 2024), (1970, 2005), (1970,2012), (1970, 2024), (1982,2005), (1982,2012), (2012,2024)]
        
        # Create charts for each time period
        for start_year, end_year in time_periods:
            create_count_area_chart(df, start_year, end_year, f'part3/charts/count_area_chart/count_area_chart_{start_year}_{end_year}.png')
            create_percentage_area_chart(df, start_year, end_year, f'part3/charts/percentage_area_chart/percentage_area_chart_{start_year}_{end_year}.png')
            
            # Create all_categories folder within percentage_line_chart
            all_categories_dir = 'part3/charts/percentage_line_chart/all_categories'
            os.makedirs(all_categories_dir, exist_ok=True) # Ensure the directory exists
            
            create_line_chart(df, start_year, end_year, 'part3/charts/percentage_line_chart')
            
            # Move overall line chart to all_categories folder
            old_path = f'part3/charts/percentage_line_chart/percentage_line_chart_all_categories_{start_year}_{end_year}.png'
            new_path = os.path.join(all_categories_dir, f'percentage_line_chart_all_categories_{start_year}_{end_year}.png')
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
            else:
                print(f"File '{new_path}' already exists, skipping rename.")
            
            # Create trend charts
            create_trend_charts(df, start_year, end_year, 'part3/charts')

        print("All charts have been created successfully.")

    except Exception as e:
        print(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()