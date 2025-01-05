"""V11_Strategy is_active 컬럼 추가

Revision ID: 224df5f44ae0
Revises: 91e4ee6c088c
Create Date: 2024-12-24 17:30:26.189502

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "224df5f44ae0"
down_revision: Union[str, None] = "91e4ee6c088c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("strategy") as batch_op:
        batch_op.add_column(sa.Column("is_active", sa.Boolean(), nullable=False, server_default="0"))


def downgrade() -> None:
    with op.batch_alter_table("strategy") as batch_op:
        batch_op.drop_column("is_active")
