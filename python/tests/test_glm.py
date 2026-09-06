from typing import get_args

from acedatacloud.resources.glm import GlmModel


def test_glm_model_literal_includes_latest_docs_models() -> None:
    models = set(get_args(GlmModel))
    assert {"glm-5.3", "glm-5.2", "glm-5", "glm-5-turbo"}.issubset(models)
