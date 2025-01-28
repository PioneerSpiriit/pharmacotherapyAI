from chembl_webresource_client.new_client import new_client
from tqdm import tqdm
import json

def fetch_bioactivity_no_batches(chembl_id, filename):
    bioactivity = new_client.activity
    results = []

    print(f"Starting for target: {chembl_id}...")

    # Test connection
    try:
        test_data = bioactivity.filter(target_chembl_id=chembl_id, limit=1)
        if not test_data:
            print(f"No data found for target: {chembl_id}")
            return
        print(f"Connected to ChEMBL API for {chembl_id}.")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # Fetch all records at once
    try:
        tqdm.write("Fetching all records...")
        data = bioactivity.filter(target_chembl_id=chembl_id)  # Fetch all records
        for record in tqdm(data, desc=f"Processing {chembl_id}", unit="record"):
            # Collect relevant fields
            if record.get("standard_type") and record.get("standard_value"):
                results.append({
                    "compound_id": record.get("molecule_chembl_id"),
                    "activity_type": record.get("standard_type"),
                    "activity_value": record.get("standard_value"),
                    "activity_units": record.get("standard_units"),
                    "assay_description": record.get("assay_description"),
                    "document_year": record.get("document_year"),
                    "document_journal": record.get("document_journal"),
                })

        # Save results to JSON file
        with open(filename, "w") as file:
            json.dump(results, file, indent=2)
        tqdm.write(f"Data saved to {filename}. Total records: {len(results)}")

    except Exception as e:
        print(f"Error during data fetching: {e}")

# Fetch bioactivity for GLP-1R
fetch_bioactivity_no_batches("CHEMBL1985", "gcgr_bioactivity.json")
