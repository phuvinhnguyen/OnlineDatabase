class ExampleValidation:
    def __init__(self,
                 score,
                 validate_instances,
                 meta_data,
                 ) -> None:
        self.data = {
            "score": score,
            "validate": validate_instances,
            "meta_data": meta_data
        }

    def __repr__(self) -> str:
        # Return json like string
        return str(self.data)