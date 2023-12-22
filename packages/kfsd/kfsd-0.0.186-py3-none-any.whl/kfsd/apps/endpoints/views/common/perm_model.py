from kfsd.apps.endpoints.views.common.model import ModelViewSet


class PermModelViewSet(ModelViewSet):
    lookup_field = "identifier"
    lookup_value_regex = "[^/]+"

    def get_queryset(self):
        if self.token_user.isAuthEnabled() and self.token_user.isAuthenticated():
            pass

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
