import json
from smolagents import Tool
from utils.lei_utils import LeiUtils


class LegalEntityIdentifierTool(Tool):
    name = "legal_entity_identifier_tool"
    description = (
        """
        Checks if an entity has a Legal Entity Identifier (LEI) and determines regulatory obligations. 
        It queries the GLEIF API for LEI existence, assesses if an LEI is required based on jurisdiction and 
        industry, 
        and assigns a risk score based on compliance. The tool outputs results in JSON format with entity details, 
        LEI status, risk score, and supporting evidence.
        Example:
        >>> tool = LegalEntityIdentifier()
        >>> result = tool.forward("JPMorgan Chase & Co.", "US", "banking")
        >>> print(result)
        {
            "entity": "JPMorgan Chase & Co.",
            "lei": "5493004FHQUJY2R9V759",
            "lei_required": true,
            "risk_score": 1,
            "reason": "JPMorgan Chase & Co. has an LEI: 5493004FHQUJY2R9V759"
        }
        """
    )
    inputs = {
        "entity": {
            "type": "string",
            "description": "The name of the entity (e.g., 'Goldman Sachs Group Inc.')."
        },
        "jurisdiction": {
            "type": "string",
            "description": "The jurisdiction of the entity (e.g., 'United States')."
        },
        "industry": {
            "type": "string",
            "description": "The industry of the entity (e.g., 'banking')."
        }
    }
    output_type = "string"

    def forward(self, entity: str, jurisdiction: str, industry: str) -> str:
        assert isinstance(entity, str) and isinstance(jurisdiction, str) and isinstance(industry, str), "Inputs must " \
                                                                                                            "be strings. "
        entity_info = {"name": entity, "jurisdiction": jurisdiction, "industry": industry}
        return json.dumps(LeiUtils.assign_risk_score(entity_info), indent=2)


if __name__ == "__main__":
    tool = LegalEntityIdentifierTool()
    response = tool.forward("JPMorgan Chase & Co.", "US", "banking")
    print(response)
