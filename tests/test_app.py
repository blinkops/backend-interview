from app import create_app


def test_run_app():
    assert create_app()
