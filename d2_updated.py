from chembl_webresource_client.new_client import new_client
import pandas as pd
from tqdm import tqdm
import sys

def fetch_bioactivity(target_name, file_name):
    print(f"🔍 Fetching data for {target_name}...")

    bioactivity = new_client.activity
    data = bioactivity.filter(target_chembl_id=target_name)  # ✅ Get an iterator instead of loading all at once

    results = []
    
    with tqdm(desc=f"Processing {target_name}", unit="record", dynamic_ncols=True, leave=True, file=sys.stdout) as pbar:
        for record in data:  # ✅ Stream records one by one instead of waiting for all
            results.append(record)
            pbar.update(1)  # ✅ Updates tqdm progress bar in real-time
            sys.stdout.flush()  # ✅ Forces immediate output in Spyder

    print(f"✅ Retrieved {len(results)} records for {target_name}")

    df = pd.DataFrame(results)
    df.to_csv(file_name, index=False)
    print(f"✅ Data saved: {file_name}")

if __name__ == "__main__":
# Fetch data for multiple targets with parallel sessions
    targets = [
        ("CHEMBL1985", "GCGR_bioactivity.csv"),
        ("CHEMBL1784", "GLP1R_bioactivity.csv"),
        ("CHEMBL4383", "GIP1R_bioactivity.csv")
        ]

    for target in targets:
        fetch_bio_activity(target[0], target[1])
