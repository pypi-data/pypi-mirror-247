from functools import wraps

from werkzeug.exceptions import Forbidden


def permission_required(perm, fn=None):
    """
    View decorator that checks for the given permissions before allowing the
    view to execute. Use it like this::

        from rules.contrib.views import permission_required
        from posts.models import Post

        def get_post_by_pk(request, post_id):
            return get_object_or_404(Post, pk=post_id)

        @permission_required('posts.change_post', fn=get_post_by_pk)
        def post_update(request, post_id):
            # ...

    ``perm`` is either a permission name as a string, or a list of permission
    names.

    ``fn`` is an optional callback that receives the same arguments as those
    passed to the decorated view and must return the object to check
    permissions against. If omitted, the decorator behaves just like Django's
    ``permission_required`` decorator, i.e. checks for model-level permissions.

    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Normalize to a list of permissions
            match perm:
                case str():
                    perms = (perm,)
                case list() | tuple():
                    perms = perm
                case _:
                    raise TypeError(
                        "The first argument to permission_required must be a "
                        "permission name or a list of permission names."
                    )

            # Get the object to check permissions against
            if callable(fn):
                obj = fn(request, *args, **kwargs)
            else:  # pragma: no cover
                obj = fn

            # Get the user
            user = request.user

            # Check for permissions and return a response
            if not user.has_perms(perms, obj):
                # User does not have a required permission
                raise Forbidden()

            # User has all required permissions -- allow the view to execute
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
