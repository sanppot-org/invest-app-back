"""V10_Strategy market 컬럼추가

Revision ID: 91e4ee6c088c
Revises: db54643c0efa
Create Date: 2024-12-19 14:15:27.190115

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.common.domain.type import Market
from src.common.adapter.out.persistence.base_entity import EnumType


# revision identifiers, used by Alembic.
revision: str = "91e4ee6c088c"
down_revision: Union[str, None] = "db54643c0efa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("strategy") as batch_op:
        batch_op.add_column(sa.Column("market", sa.CHAR(length=2), nullable=False, server_default="KR"))


def downgrade() -> None:
    with op.batch_alter_table("strategy") as batch_op:
        batch_op.drop_column("market")
