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
            line_lower = line.lower()
            if "unknown identifier" in line_lower:
                if "'" in line:
                    ident = line.split("'")[1] if len(line.split("'")) > 1 else "unknown"
                    recommendations.append(f"Import or define missing identifier: {ident}")
            elif "type mismatch" in line_lower:
                recommendations.append("Fix type mismatch - check argument types match expected types")
            elif "invalid argument" in line_lower:
                recommendations.append("Review function arguments - ensure correct number and types")
            elif "missing assumption" in line_lower or "no such assumption" in line_lower:
                recommendations.append("Add missing hypothesis or assumption to theorem statement")
            elif "syntax error" in line_lower or "unexpected token" in line_lower:
                recommendations.append("Fix syntax error - check Lean 4 syntax rules")
            elif "function expected" in line_lower:
                recommendations.append("Type error - expected function but got different type, check imports or definitions")
            elif "declaration uses 'sorry'" in line_lower:
                recommendations.append("Replace 'sorry' with complete proof tactics")
            elif "failed to synthesize" in line_lower:
                recommendations.append("Missing instance or import - add required instances or imports")
            elif "does not exist" in line_lower and "module" in line_lower:
                recommendations.append("Missing import - check module name and availability in mathlib")
            elif "error:" in line_lower and "lean" in line_lower:
                # Generic error fallback
                recommendations.append("Lean compilation error - review theorem syntax and tactics")
                
        # Special case: if no specific errors found but we have output, give general advice
        if not recommendations and self.lean_output.strip():
            if "warning" in self.lean_output.lower():
                recommendations.append("Warning detected - proof may be incomplete or use deprecated features")
            else:
                recommendations.append("Unknown Lean error - try simpler proof approach or check syntax")
        elif not recommendations:
            recommendations.append("No actionable feedback detected from Lean output")
            
        return recommendations

    def to_dict(self):
        return {"lean_output": self.lean_output, "recommendations": self.parse()}

# Example usage:
# parser = LeanFeedbackParser(lean_output)
# feedback = parser.parse()
# print(feedback)
