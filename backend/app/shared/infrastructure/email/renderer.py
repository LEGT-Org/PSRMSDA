from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class JinjaEmailRendered:

    def __init__(
        self, 
        template_directory: str
    ):

        self.environment = Environment(
            loader=FileSystemLoader(
                template_directory
            )
        )


    def render(
        self,
        template_name: str,
        **context
    ) -> str:

        template = self.environment.get_template(template_name)

        return template.render(**context)