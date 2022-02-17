from src.models.user.entities.enums.user_type import UserType
from src.models.refresh_token.entities.refresh_token import RefreshToken
from src.models.seller.entities.seller import Seller
from src.shared.usecases.crud_usecase import CrudUsecase
from src.utils import utils
from jwt.exceptions import ExpiredSignatureError
from src.utils import globals


class ManageUsersUsecase(CrudUsecase):
    def __init__(self, repository, refresh_token_repository, seller_repository):
        super().__init__(repository)
        self.refresh_token_repository = refresh_token_repository
        self.seller_repository = seller_repository

    def register(self, entity, access_token=None):
        if entity.user_type == UserType.ADMINISTRATOR:
            if access_token is None:
                return ["Missing Access Token in creation of an Admin Account"]
            try:
                payload = utils.decode_access_token(
                    globals.SECRET,
                    access_token
                )
                user = self.repository.find_by_id(payload["user_id"])
                if user.user_type != UserType.ADMINISTRATOR:
                    return ["Access Token is not from an Admin account"]
            except ExpiredSignatureError as e:
                return [str(e)]

        current_time = utils.get_current_datetime()
        entity.created_at = current_time
        entity.updated_at = current_time

        entity.password = entity.password

        entity = self.repository.create(entity)

        if entity.user_type == UserType.SELLER:
            current_time = utils.get_current_datetime()
            seller = Seller(None, "", "", "", entity.id)
            seller.created_at = current_time
            seller.updated_at = current_time
            self.seller_repository.create(seller)

        access_token = utils.get_access_token(
            globals.SECRET,
            entity.id,
            entity.email,
            entity.user_type
        )

        refresh_token = RefreshToken(entity.email, utils.get_refresh_token())
        refresh_token = self.refresh_token_repository.create(
            refresh_token
        ).token

        return [access_token, refresh_token]

    def login(self, email, password):
        user = self.repository.find_by_email(email)

        if user is None:
            return ["Invalid user information"]

        if user.password != password:
            return ["Invalid user information"]

        access_token = utils.get_access_token(
            globals.SECRET,
            user.id,
            user.email,
            user.user_type
        )

        refresh_token = self.refresh_token_repository.find_by_id(user.email)

        if refresh_token is None:
            refresh_token = RefreshToken(user.email, utils.get_refresh_token())
            refresh_token = self.refresh_token_repository.create(
                refresh_token
            )

        return [access_token, refresh_token.token]

    def logout(self, access_token, refresh_token):
        data = utils.decode_access_token(globals.SECRET, access_token)
        refresh_token = self.refresh_token_repository.find_by_id(data["email"])
        if refresh_token is not None:
            self.refresh_token_repository.delete(data["email"])
        return

    def refresh(self, refresh_token):
        refresh_token = self.refresh_token_repository.find_by_token(
            refresh_token)
        if refresh_token is None:
            return ["Invalid Token"]

        user = self.repository.find_by_email(refresh_token.id)

        self.refresh_token_repository.delete(user.email)

        access_token = utils.get_access_token(
            globals.SECRET,
            user.id,
            user.email,
            user.user_type
        )

        refresh_token = RefreshToken(user.email, utils.get_refresh_token())
        refresh_token = self.refresh_token_repository.create(
            refresh_token
        )

        return [access_token, refresh_token.token]
