from unittest.mock import Mock

from acedatacloud.resources.providers.tripo import Tripo


def test_model_import_does_not_send_texture_or_conversion_options():
    transport = Mock()
    transport.request.return_value = {"task_id": "original"}
    Tripo(transport).models(action="import", model_url="https://example.org/a.glb", idempotency_key="stable")
    call = transport.request.call_args
    assert call.kwargs["json"] == {"action": "import", "model_url": "https://example.org/a.glb", "async": True}
    assert call.kwargs["extra_headers"] == {"Idempotency-Key": "stable"}


def test_rig_check_and_batch_keep_their_own_request_shape():
    transport = Mock()
    transport.request.return_value = {"task_id": "original"}
    client = Tripo(transport)
    client.animations(action="rig_check", model_id="source")
    assert transport.request.call_args.kwargs["json"] == {"action": "rig_check", "model_id": "source", "async": True}
    client.tasks(action="retrieve_batch", ids=["one", "two"])
    assert transport.request.call_args.kwargs["json"] == {"action": "retrieve_batch", "ids": ["one", "two"]}
