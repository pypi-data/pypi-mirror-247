from rest_framework import status

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.services.gateway import APIGateway
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class PermissionApi(APIGateway):
    def __init__(self, request=None):
        APIGateway.__init__(self, request)

    def genResourceId(self, resource):
        return "{},{}".format(resource.type, resource.identifier)

    def genUserId(self, user):
        return "{},{}".format(user.getUserModel(), user.getUserId())

    def getGatewayUrl(self):
        return self.constructUrl(
            [
                "services.context.gateway_api.host",
                "services.context.perm_api.base_uri",
            ]
        )

    def getAuthResourceUrl(self, userId, resourceId):
        authorizeUri = DictUtils.get_by_path(
            self.getDjangoRequest().getConfig(),
            "services.context.perm_api.auth_resource_uri",
        )
        authorizeUri = authorizeUri.format(userId, resourceId)

        return self.getGatewayUrl().format(self.genUrlEncode(authorizeUri))

    def getAllResources(self, userId, resourceType):
        resourcesUri = DictUtils.get_by_path(
            self.getDjangoRequest().getConfig(),
            "services.context.perm_api.auth_resources_all_uri",
        )
        resourcesUri = resourcesUri.format(userId, resourceType)
        return self.getGatewayUrl().format(self.genUrlEncode(resourcesUri))

    def authorize(self, userId, perm, resourceId):
        url = self.getAuthResourceUrl(userId, resourceId)
        payload = {"action": perm}
        return self.httpPost(url, payload, status.HTTP_200_OK)

    def authorized_resources(self, userId, perm, resourceType):
        url = self.getAllResources(userId, resourceType)
        payload = {"action": perm}
        return self.httpPost(url, payload, status.HTTP_200_OK)
