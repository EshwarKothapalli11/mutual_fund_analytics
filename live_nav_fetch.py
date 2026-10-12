


from pathlib import Path
import requests
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

FUNDS = {
    "HDFC_Large_Cap": {
        "code": "119018",
        "expected": "HDFC Large Cap Fund",
    },
    "SBI_Large_Cap": {
        "code": "119598",
        "expected": "SBI Large Cap Fund",
    },
    "ICICI_Prudential_Large_Cap": {
        "code": "120586",
        "expected": "ICICI Prudential Large Cap Fund",
    },
    "Nippon_India_Large_Cap": {
        "code": "118632",
        "expected": "Nippon India Large Cap Fund",
    },
    "Axis_Large_Cap": {
        "code": "120465",
        "expected": "Axis Large Cap Fund",
    },
    "Kotak_Large_Cap": {
        "code": "120152",
        "expected": "Kotak Large Cap Fund",
    },
}


def fetch_nav(label, details):
    code = details["code"]
    expected = details["expected"]
    url = f"https://api.mfapi.in/mf/{code}"

    print(f"\nChecking {label} (scheme code {code})...")

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        result = response.json()

        actual_name = result.get("meta", {}).get("scheme_name", "")

        print("API scheme name:", actual_name)

        # Prevent incorrect scheme names from being saved.
        if expected.lower() not in actual_name.lower():
            print("SKIPPED: Scheme name did not match the expected name.")
            return

        records = result.get("data", [])
        if not records:
            print("SKIPPED: API returned no NAV records.")
            return

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(
            df["date"], format="%d-%m-%Y", errors="coerce"
        )
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
        df = df.dropna(subset=["date", "nav"])

        df["scheme_code"] = code
        df["scheme_name"] = actual_name
        df = df[["scheme_code", "scheme_name", "date", "nav"]]
        df = df.sort_values("date")

        output = RAW_DIR / f"live_nav_{label.lower()}.csv"
        df.to_csv(output, index=False)

        print("Records saved:", len(df))
        print("File:", output)

    except (requests.RequestException, ValueError) as error:
        print("ERROR:", error)


if __name__ == "__main__":
    for label, details in FUNDS.items():
        fetch_nav(label, details)
