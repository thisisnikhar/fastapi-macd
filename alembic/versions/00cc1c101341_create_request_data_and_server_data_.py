"""create request_data and server_data tables

Revision ID: 00cc1c101341
Revises: 
Create Date: 2026-07-13 09:04:21.647254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00cc1c101341'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
       "request_data",
    sa.Column("ticket_number", sa.String(25), primary_key=True),
       sa.Column("ticket_id", sa.Integer(), unique=True),

    )

    op.create_table(
        "server_data",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("request_id", sa.String(25)),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["request_data.ticket_number"]
        ),
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("server_data")
    op.drop_table("request_data")
