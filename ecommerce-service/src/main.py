from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app

from src.models.seller.http.sellers_blueprint import create_sellers_blueprint
from src.models.seller.repositories.sqlalchemy_sellers_repository import SQLAlchemySellersRepository
from src.models.seller.usecases.manage_sellers_usecase import ManageSellersUsecase

from src.models.user.http.users_blueprint import create_users_blueprint
from src.models.user.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.models.user.usecases.manage_users_usecase import ManageUsersUsecase

from src.models.product.http.products_blueprint import create_products_blueprint
from src.models.product.repositories.sqlalchemy_products_repository import SQLAlchemyProductsRepository
from src.models.product.usecases.manage_products_usecase import ManageProductsUsecase

from src.models.order.http.orders_blueprint import create_orders_blueprint
from src.models.order.repositories.sqlalchemy_orders_repository import SQLAlchemyOrdersRepository
from src.models.order.usecases.manage_orders_usecase import ManageOrdersUsecase

from src.models.refresh_token.repositories.sqlalchemy_refresh_token_repository import SQLAlchemyRefreshTokenRepository

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

sqlalchemy_client = SQLAlchemyClient()
sqlalchemy_sellers_repository = SQLAlchemySellersRepository(sqlalchemy_client)
sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_products_repository = SQLAlchemyProductsRepository(
    sqlalchemy_client
)
sqlalchemy_orders_repository = SQLAlchemyOrdersRepository(sqlalchemy_client)
sqlalchemy_refresh_token_repository = SQLAlchemyRefreshTokenRepository(
    sqlalchemy_client
)
sqlalchemy_client.create_tables()

manage_sellers_usecase = ManageSellersUsecase(sqlalchemy_sellers_repository)
manage_users_usecase = ManageUsersUsecase(
    sqlalchemy_users_repository,
    sqlalchemy_refresh_token_repository,
    sqlalchemy_sellers_repository
)
manage_products_usecase = ManageProductsUsecase(
    sqlalchemy_products_repository, sqlalchemy_sellers_repository)
manage_orders_usecase = ManageOrdersUsecase(sqlalchemy_orders_repository)

blueprints = [
    create_sellers_blueprint(manage_sellers_usecase),
    create_users_blueprint(manage_users_usecase),
    create_products_blueprint(manage_products_usecase),
    create_orders_blueprint(manage_orders_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)
