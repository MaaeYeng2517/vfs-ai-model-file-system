"""Initial schema for Phase 1 — Infrastructure Foundation.

Creates namespaces, directories, files, storage_objects, assets, audit_logs tables.
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    # namespaces
    op.create_table(
        "namespaces",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("settings", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )

    # directories
    op.create_table(
        "directories",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("namespace_id", sa.Uuid(), nullable=False),
        sa.Column("parent_id", sa.Uuid(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("path", sa.String(length=4096), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["directories.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("namespace_id", "path", name="uq_dir_ns_path"),
        sa.PrimaryKeyConstraint("id"),
    )

    # files
    op.create_table(
        "files",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("namespace_id", sa.Uuid(), nullable=False),
        sa.Column("directory_id", sa.Uuid(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("path", sa.String(length=4096), nullable=False),
        sa.Column("mime_type", sa.String(length=255), nullable=True),
        sa.Column("size", sa.BigInteger(), nullable=True),
        sa.Column("storage_key", sa.String(length=512), nullable=False),
        sa.Column("hash", sa.String(length=64), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("metadata", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["directory_id"], ["directories.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("namespace_id", "path", name="uq_file_ns_path"),
        sa.PrimaryKeyConstraint("id"),
    )

    # storage_objects
    op.create_table(
        "storage_objects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("bucket", sa.String(length=255), nullable=False),
        sa.Column("object_key", sa.String(length=512), nullable=False),
        sa.Column("size", sa.BigInteger(), nullable=True),
        sa.Column("content_type", sa.String(length=255), nullable=True),
        sa.Column("sha256", sa.String(length=64), nullable=True),
        sa.Column("storage_backend", sa.String(length=64), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("object_key"),
    )

    # assets
    op.create_table(
        "assets",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("namespace_id", sa.Uuid(), nullable=False),
        sa.Column("parent_id", sa.Uuid(), nullable=True),
        sa.Column("asset_type", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("path", sa.String(length=4096), nullable=False),
        sa.Column("mime_type", sa.String(length=255), nullable=True),
        sa.Column("size", sa.BigInteger(), nullable=True),
        sa.Column("storage_key", sa.String(length=512), nullable=True),
        sa.Column("hash", sa.String(length=64), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("metadata", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_id"], ["assets.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # audit_logs
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("namespace_id", sa.Uuid(), nullable=True),
        sa.Column("actor_id", sa.String(length=255), nullable=True),
        sa.Column("actor_type", sa.String(length=64), nullable=True),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=True),
        sa.Column("resource_id", sa.String(length=512), nullable=True),
        sa.Column("resource_path", sa.String(length=4096), nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("metadata", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Seed default namespace
    op.execute(
        """
        INSERT INTO namespaces (id, name, slug, description, is_active, created_at, updated_at)
        VALUES (
            '00000000-0000-0000-0000-000000000001',
            'default',
            'default',
            'Default namespace',
            1,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP
        )
        """
    )


def downgrade():
    op.drop_table("audit_logs")
    op.drop_table("assets")
    op.drop_table("storage_objects")
    op.drop_table("files")
    op.drop_table("directories")
    op.execute("DELETE FROM namespaces WHERE slug = 'default'")
    op.drop_table("namespaces")