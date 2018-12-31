import os


_orig_dir = os.path.dirname(os.path.realpath(__file__))


def resolve_path(*path):
    """Resolve any path based on the project root.
    resolve_path('foo', 'bar') will give an absolute path to your_project_directory/foo/bar
    If the path is already absolute, it will stay absolute
    """
    return os.path.abspath(os.path.join(_orig_dir, '..', *path))
