from rest_framework import status
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.logger import Logger, LogLevel

# from kfsd.apps.core.common.cache import cache
from kfsd.apps.core.services.gateway import APIGateway

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TokenApi(APIGateway):
    def __init__(self, request=None):
        APIGateway.__init__(self, request)

    def getFeApiUrl(self):
        return self.constructUrl(
            [
                "services.context.gateway_api.host",
                "services.context.fe_api.base_uri",
            ]
        )

    def getMgmtApiUrl(self):
        return self.constructUrl(
            [
                "services.context.gateway_api.host",
                "services.context.mgmt_api.base_uri",
            ]
        )

    def getLogoutUrl(self):
        logoutUri = DictUtils.get_by_path(
            self.getDjangoRequest().getConfig(),
            "services.context.fe_api.logout_uri",
        )

        return self.getFeApiUrl().format(self.genUrlEncode(logoutUri))

    def getTokenPublicKeyUrl(self):
        publicKeyUri = DictUtils.get_by_path(
            self.getDjangoRequest().getConfig(),
            "services.context.mgmt_api.public_key_uri",
        )
        return self.getMgmtApiUrl().format(self.genUrlEncode(publicKeyUri))

    def getRefreshAccessTokenUrl(self):
        refreshAccessTokenUri = DictUtils.get_by_path(
            self.getDjangoRequest().getConfig(),
            "services.context.mgmt_api.refresh_access_token_uri",
        )
        return self.getMgmtApiUrl().format(self.genUrlEncode(refreshAccessTokenUri))

    # @cache("kfsd.token.publickey")
    def tokenPublicKey(self):
        return self.httpGet(self.getTokenPublicKeyUrl(), status.HTTP_200_OK)

    def logout(self):
        return self.httpGet(self.getLogoutUrl(), status.HTTP_200_OK)

    def refreshAccessToken(self, payload):
        return self.httpPost(
            self.getRefreshAccessTokenUrl(), payload, status.HTTP_200_OK
        )
