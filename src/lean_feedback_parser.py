class LeanFeedbackParser:
    """
    Parses Lean theorem prover output and extracts actionable feedback.
    """
    def __init__(self, lean_output: str):
        self.lean_output = lean_output

    def parse(self):
        """
        Parses Lean output and returns a list of recommendations.
        """
        recommendations = []
        lines = self.lean_output.splitlines()
        for line in lines:
            if "unknown identifier" in line:
                recommendations.append("Define missing identifier mentioned: " + line.split("'",2)[1])
            elif "type mismatch" in line:
                recommendations.append("Check and correct type mismatch: " + line)
            elif "invalid argument" in line:
                recommendations.append("Review arguments for function/application: " + line)
            elif "missing assumption" in line or "no such assumption" in line:
                recommendations.append("Add missing assumption: " + line)
            elif "syntax error" in line:
                recommendations.append("Fix syntax error: " + line)
            # Add more patterns as needed
        if not recommendations:
            recommendations.append("No actionable feedback detected.")
        return recommendations

    def to_dict(self):
        return {"lean_output": self.lean_output, "recommendations": self.parse()}

# Example usage:
# parser = LeanFeedbackParser(lean_output)
# feedback = parser.parse()
# print(feedback)
