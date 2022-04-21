# from Resources.UserResources.UserListResource import UserListResource
# from Resources.UserResources.UserResource import UserResource
# from Resources.ImageResources.ImageListResource import ImageListResource
# from Resources.ImageResources.ImageResource import ImageResource
# from Resources.InterestResources.InterestListResource import InterestListResource

from flask_restful import Api


class MainAPI:
    def __init__(self, application):
        self.api = Api(application)
        self.api.prefix = r"/api/v1"
        self._resources()

    def _resources(self) -> None:
        pass
        # self.api.add_resource(UserResource, r"/user/<int:user_id>", methods=["GET", "PUT", "DELETE"])
        # self.api.add_resource(UserListResource, r"/users", methods=["GET", "POST"])
        # self.api.add_resource(ImageResource, r"/image/<int:image_id>", methods=["GET", "PUT", "DELETE"])
        # self.api.add_resource(ImageListResource, r"/images/<int:user_id>", methods=["GET", "POST"])
        # self.api.add_resource(InterestListResource, r"/interests", methods=["GET"])

    def get_api_prefix(self):
        return self.api.prefix
