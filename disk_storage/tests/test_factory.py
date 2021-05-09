from web_server import create_app


def test_config():
    # assert not create_app({"SELF_REGISTER": False}).testing
    assert create_app({"TESTING": True}).testing
