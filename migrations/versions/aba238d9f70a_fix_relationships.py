"""Fix relationships

Revision ID: aba238d9f70a
Revises: 35e314371481
Create Date: 2025-06-18 22:59:34.327675

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aba238d9f70a"
down_revision: str | None = "35e314371481"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("books", sa.Column("series_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
        None, "books", "series", ["series_id"], ["id"], ondelete="SET NULL"
    )
    op.create_foreign_key(
        None, "books", "authors", ["author_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "books", type_="foreignkey")
    op.drop_constraint(None, "books", type_="foreignkey")
    op.drop_column("books", "series_id")
    # ### end Alembic commands ###
