import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from .models import Category, Subcategory

def read_excel_file(file):
    """Read the Excel file, excluding footer and totals/subtotals."""
    df = pd.read_excel(file, skipfooter=3)
    df = df[~df['Offre'].str.contains('Total', case=False, na=False)]
    return df

def process_excel_data(df):
    """Process Excel data to aggregate sums by categories."""
    try:
        subcategories = Subcategory.objects.all()
        categories = Category.objects.all()
        subcat_dict = {subcat.name: subcat for subcat in subcategories}
        cat_dict = {cat.id: cat for cat in categories}

        # Map 'Offre' to 'subcategory' objects
        df['subcategory'] = df['Offre'].apply(lambda x: subcat_dict.get(x))
        df = df.dropna(subset=['subcategory'])

        # Extract category from subcategory and map to category name
        df['category'] = df['subcategory'].apply(lambda x: cat_dict[x.category_id].name if x.category_id in cat_dict else None)
        df = df.dropna(subset=['category'])

        # Sum numeric data assuming it starts from the 3rd column
        date_columns = df.columns[2:]  # This assumes that date columns start from the 3rd column
        df['Total'] = df[date_columns].apply(pd.to_numeric, errors='coerce').sum(axis=1)

        # Aggregate total values by category
        result = df.groupby('category')['Total'].sum().reset_index()
        result.columns = ['Category', 'Total']

        # Debug prints
        print("Subcategories from database:", subcat_dict.keys())
        print("Categories from database:", cat_dict.keys())
        print("Data after mapping 'Offre' to subcategories and categories:", df[['Offre', 'subcategory', 'category', 'Total']])

        return result
    except Exception as e:
        logger.error(f"Error processing Excel data: {e}")
        raise