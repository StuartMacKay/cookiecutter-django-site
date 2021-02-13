
CONTEXT = {
    'create_virtualenv': 'n',
}


def test_bake_project(cookies):
    """Verify the template can actually generate a project"""
    result = cookies.bake(extra_context=CONTEXT)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == "site"
    assert result.project.isdir()
