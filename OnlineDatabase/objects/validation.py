class ExampleValidation:
    def __init__(self,
                 score,
                 validate_scores,
                 validate_samples,
                 meta_data,
                 ) -> None:
        self.data = {
            "score": score,
            "validate_scores": validate_scores,
            "validate_samples": validate_samples,
            "meta_data": meta_data
        }

    def __repr__(self) -> str:
        # Return json like string
        return str(self.data)