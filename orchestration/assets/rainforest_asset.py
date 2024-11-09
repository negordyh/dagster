import os
import requests
import json
import pandas as pd
from dagster import asset, MetadataValue, MaterializeResult, DailyPartitionsDefinition, get_dagster_logger, AssetIn
from datetime import datetime

logger = get_dagster_logger()

@asset(
    compute_kind="python",
    partitions_def=DailyPartitionsDefinition(start_date="2024-08-01"),
    group_name="rainforest_ingestion"
)
def get_product_asin() -> list:
    # Construct the full path to asins.csv
    current_dir = os.path.dirname(os.path.abspath(__file__))
    asins_path = os.path.join(current_dir, 'asins.csv')
    
    # Read ASINs from the CSV file using the full path
    asins_df = pd.read_csv(asins_path)
    asins = asins_df['asin'].tolist()
    
    logger.info(f"Found {len(asins)} ASINs to process: {asins}")
    return asins


@asset(
    compute_kind="python",
    partitions_def=DailyPartitionsDefinition(start_date="2024-08-01"),
    group_name="rainforest_ingestion",
    ins={
        "asins": AssetIn(key="get_product_asin")
    }
)
def fetch_amazon_product_data(context, asins: list) -> MaterializeResult:
    api_key = os.getenv('RAINFOREST_API_KEY')
    base_url = 'https://api.rainforestapi.com/request'
    results = []
    
    # Define output directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, 'data')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get current timestamp for filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    for asin in asins:
        logger.info(f"Processing ASIN: {asin}")
        params = {
            'api_key': api_key,
            'type': 'product',
            'amazon_domain': 'amazon.com',
            'asin': asin
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            results.append(data)
            
            # Save individual ASIN result using output_dir instead of data_dir
            asin_file = os.path.join(output_dir, f'{asin}_{timestamp}.json')
            with open(asin_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved data for ASIN {asin} to {asin_file}")
        else:
            logger.error(f"Failed to retrieve data for ASIN {asin}: {response.status_code}")

    return MaterializeResult(
        metadata={
            "num_records": len(results),
            "preview": MetadataValue.md(json.dumps(results[:5], indent=2)),
            "data_location": MetadataValue.path(output_dir)
        }
    )