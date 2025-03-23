import requests


class LeiUtils:
    @staticmethod
    def check_lei(entity_name: str) -> str:
        """
        Query the GLEIF API for an entity by its legal name.
        Returns the LEI if found, otherwise returns None.
        """
        url = "https://api.gleif.org/api/v1/lei-records"
        params = {"filter[entity.legalName]": entity_name}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error querying GLEIF API: {e}")
            return None

        data = response.json()
        return data["data"][0].get("id") if data.get("data") else None

    @staticmethod
    def standardize_jurisdiction(jurisdiction: str) -> str:
        """
        Standardizes common abbreviations and variations of jurisdiction names.
        """
        mapping = {
            "US": "United States",
            "USA": "United States",
            "UK": "United Kingdom",
            "EU": "European Union",
            "Canada": "Canada",
            "Australia": "Australia"
        }
        return mapping.get(jurisdiction.upper(), jurisdiction.title())

    @staticmethod
    def requires_lei(jurisdiction: str, industry: str) -> tuple:
        """
        Determines whether an entity is required to have an LEI based on its jurisdiction and industry.
        """
        regulated_industries = {
            "banking": {"European Union": "EMIR", "United States": "Dodd-Frank Act"},
            "investment": {"European Union": "MiFID II", "United States": "Dodd-Frank Act"},
            "insurance": {"European Union": "Solvency II", "United States": "NAIC Model Laws"},
            "securities": {"European Union": "CSDR", "United States": "Dodd-Frank Act"},
            "fund management": {"European Union": "AIFMD", "United States": "Investment Advisers Act"},
            "derivatives": {"European Union": "EMIR", "United States": "Dodd-Frank Act"},
            "financial services": {"European Union": "MiFID II", "United States": "Dodd-Frank Act"}
        }

        jurisdiction = LeiUtils.standardize_jurisdiction(jurisdiction)
        industry = industry.strip().lower()

        if industry in regulated_industries and jurisdiction in regulated_industries[industry]:
            mandate = regulated_industries[industry][jurisdiction]
            return True, f"Entities in {industry} within {jurisdiction} require an LEI under {mandate}."

        return False, f"No LEI mandate found for {industry} in {jurisdiction}."

    @staticmethod
    def assign_risk_score(entity: dict) -> dict:
        """
        Assigns a risk score based on LEI compliance.
        """
        lei = LeiUtils.check_lei(entity["name"])
        lei_required, reason = LeiUtils.requires_lei(entity["jurisdiction"], entity["industry"])

        if lei_required and not lei:
            risk_score = 10  # High risk if LEI is required but missing
            details = f"{entity['name']} is required to have an LEI but does not possess one."
        else:
            risk_score = 1 if lei else 0  # Low risk if LEI exists or not required
            details = f"{entity['name']} has an LEI: {lei}" if lei else "LEI not required."

        return {
            "entity": entity["name"],
            "lei": lei,
            "lei_required": lei_required,
            "risk_score": risk_score,
            "reason": f"{details} {reason}"
        }


if __name__ == "__main__":
    import json

    entity = {
        "name": "Goldman Sachs",
        "jurisdiction": "US",
        "industry": "banking"
    }
    result = LeiUtils.assign_risk_score(entity)
    print(json.dumps(result, indent=2))
