"""Initial versioned simulator, analysis and isolated evaluation schema."""

from alembic import op
from app.models import Base

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS evaluation")
    Base.metadata.create_all(op.get_bind())
    op.execute("GRANT USAGE ON SCHEMA public TO aml_app, aml_evaluator")
    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO aml_app")
    op.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO aml_evaluator")
    op.execute("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO aml_app")
    op.execute("GRANT USAGE ON SCHEMA evaluation TO aml_evaluator")
    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA evaluation TO aml_evaluator")
    op.execute("REVOKE ALL ON SCHEMA evaluation FROM aml_app, PUBLIC")


def downgrade():
    Base.metadata.drop_all(op.get_bind())
    op.execute("DROP SCHEMA evaluation")
