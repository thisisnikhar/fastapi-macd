"""Rename ci_onboading table

Revision ID: e73c04c02f15
Revises: d5bbf70672ec
Create Date: 2026-07-14 06:22:54.958541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e73c04c02f15'
down_revision: Union[str, Sequence[str], None] = 'd5bbf70672ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("ci_onboading_server_data","ci_onboarding_server_data")


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table("ci_onboarding_server_data","ci_onboading_server_data")
