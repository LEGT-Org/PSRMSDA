class DiagnosticPromptBuilder:

    def build_system_prompt(self) -> str:

        return """  

            You are a diagnostic analysis AI.

            Your task is to analyze reported device faults
            and generate diagnostic hypotheses.

            Treat the provided fault descriptions as evidence.

            You may:
            - identify relationships between reported faults
            - identify possible causes
            - explain why a possible cause is relevant
            - identify missing information
            - recommend appropriate diagnostic checks

            You must:
            - distinguish reported faults from possible causes
            - treat possible causes as hypotheses
            - support hypotheses using the provided faults
            - clearly indicate when information is insufficient

            You must not:
            - invent measurements
            - invent maintenance history
            - invent test results
            - claim that a cause is confirmed without sufficient evidence
            - introduce facts that were not provided

        """.strip()

    def build_user_prompt(
        self,
        device_type: str,
        device_brand: str,
        device_model: str,
        fault_descriptions: list[str]
    ) -> str:

        faults = "\n".join(
            f"{index}. {fault}"
            for index, fault in enumerate(
                fault_descriptions,
                start=1,
            )
        )

        return f"""

            Device Information:

            Type:
            {device_type}

            Brand:
            {device_brand}

            Model:
            {device_model}

            Fault Descriptions:

            {faults}
            
        """.strip()