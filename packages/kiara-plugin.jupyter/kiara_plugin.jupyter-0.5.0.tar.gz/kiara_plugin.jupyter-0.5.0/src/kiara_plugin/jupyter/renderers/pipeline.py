# -*- coding: utf-8 -*-
from typing import Any, Dict, Iterable, Mapping, Union

from jinja2 import Template
from pydantic import Field

from kiara.models.module.pipeline.pipeline import Pipeline
from kiara.renderers import RenderInputsSchema, SourceTransformer
from kiara.renderers.included_renderers.pipeline import PipelineTransformer
from kiara.renderers.jinja import BaseJinjaRenderer, JinjaEnv
from kiara.utils import log_message


class JupyterNotebookRenderInputSchema(RenderInputsSchema):
    inputs: Dict[str, Any] = Field(
        description="The pipeline inputs.", default_factory=dict
    )


class PipelineRenderer(BaseJinjaRenderer[Pipeline, JupyterNotebookRenderInputSchema]):
    """Renders a basic Jupyter notebook from a pipeline.

    If the pipeline inputs have required inputs, you can either specify those in in the render config, or you have to edit the rendered notebook in the places indicted with `<TODO_SET_INPUT>` before execution.

    ## Examples

    ### Terminal

    Example invoication from the command line (using [this](https://github.com/DHARPA-Project/kiara_plugin.tabular/blob/develop/examples/pipelines/tables_from_csv_files.yaml) pipeline):

    ```
    kiara render --source-type pipeline --target-type jupyter_notebook item tables_from_csv_files.yaml inputs='{"path": "/home/markus/projects/kiara/kiara_plugin.tabular/examples/data/journals"}' > tables_from_csv_files.ipynb

    jupyter-lab tables_from_csv_files.ipynb
    ```

    ### Python API

    Example usage from the Python API:

    ``` python
    from kiara.api import KiaraAPI

    kiara = KiaraAPI.instance()

    pipeline = "logic.xor"  # any valid pipeline operation (or reference to one)
    pipeline_inputs = {
        "a": True,
        "b": False,
    }
    rendered = kiara.render(pipeline, source_type="pipeline", target_type="jupyter_notebook", render_config={"inputs": pipeline_inputs})
    print("# Rendered notebook for pipeline 'logic.xor':")
    print(rendered)
    ```

    """

    _renderer_name = "pipeline_notebook"
    _inputs_schema = JupyterNotebookRenderInputSchema

    def retrieve_supported_render_sources(self) -> str:
        return "pipeline"

    def retrieve_supported_render_targets(cls) -> Union[Iterable[str], str]:
        return "jupyter_notebook"

    def retrieve_source_transformers(self) -> Iterable[SourceTransformer]:
        return [PipelineTransformer(kiara=self._kiara)]

    def retrieve_jinja_env(self) -> JinjaEnv:

        jinja_env = JinjaEnv(template_base="kiara_plugin.jupyter")
        return jinja_env

    def get_template(self, render_config: JupyterNotebookRenderInputSchema) -> Template:

        return self.get_jinja_env().get_template("pipeline/jupyter_notebook.ipynb.j2")

    def assemble_render_inputs(
        self, instance: Any, render_config: JupyterNotebookRenderInputSchema
    ) -> Mapping[str, Any]:

        from kiara.utils.rendering import create_pipeline_render_inputs

        pipeline: Pipeline = instance
        pipeline_user_inputs: Mapping[str, Any] = render_config.inputs
        result: Mapping[str, Any] = create_pipeline_render_inputs(
            pipeline, pipeline_user_inputs
        )
        return result

    def _post_process(self, rendered: str) -> str:

        is_notebook = True
        if is_notebook:
            import jupytext

            notebook = jupytext.reads(rendered, fmt="py:percent")
            converted: str = jupytext.writes(notebook, fmt="notebook")
            return converted
        else:
            try:
                import black
                from black import Mode  # type: ignore

                cleaned: str = black.format_str(rendered, mode=Mode())
                return cleaned

            except Exception as e:
                log_message(
                    f"Could not format python code, 'black' not in virtual environment: {e}."
                )
                return rendered
