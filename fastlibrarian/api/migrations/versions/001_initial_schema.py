"""Initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2024-01-20

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial tables."""
    # Create authors table
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False, index=True),
    )

    # Create series table
    op.create_table(
        "series",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False, index=True),
    )

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("username", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("email", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
    )

    # Create books table
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(), nullable=False, index=True),
        sa.Column(
            "author_id", sa.Integer(), sa.ForeignKey("authors.id"), nullable=False
        ),
        sa.Column("published_date", sa.Date(), nullable=False),
        sa.Column("isbn", sa.String(), nullable=False, unique=True),
        sa.Column("pages", sa.Integer(), nullable=False),
        sa.Column("cover_image", sa.String()),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("series_id", sa.Integer(), sa.ForeignKey("series.id")),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
    )


def downgrade() -> None:
    """Remove schema."""
    op.drop_table("books")
    op.drop_table("users")
    op.drop_table("series")
    op.drop_table("authors")
