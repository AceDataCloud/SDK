from typing import get_args

from acedatacloud import AiChatModel


def test_aichat_model_literals_include_deepseek_v4_pro() -> None:
    assert "deepseek-v4-pro" in get_args(AiChatModel)
