"""update asset icon field

Revision ID: 003
Revises: 002
Create Date: 2024-03-14
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    # Start transaction
    connection = op.get_bind()
    
    # Set connection charset to utf8mb4
    connection.execute("SET NAMES utf8mb4")
    connection.execute("SET CHARACTER SET utf8mb4")
    connection.execute("SET character_set_connection=utf8mb4")
    
    with connection.begin() as transaction:
        try:
            # Ensure table uses utf8mb4 charset
            op.execute('ALTER TABLE asset CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
            
            # Drop old icon column
            op.drop_column('asset', 'icon')
            
            # Add new icon column with emoji support
            op.add_column('asset', sa.Column('icon', sa.String(10, collation='utf8mb4_unicode_ci'), nullable=False))
            
            # Set default icon
            connection.execute("UPDATE asset SET icon = _utf8mb4 '💰'")
            
            # Drop type column as it's no longer needed
            op.drop_column('asset', 'type')
            
            # Drop maturity_month as we only need year
            op.drop_column('asset', 'maturity_month')
            
            # Make maturity_year required
            op.alter_column('asset', 'maturity_year',
                existing_type=sa.Integer(),
                nullable=False)
            
            # Commit transaction
            transaction.commit()
        except Exception as e:
            # Rollback on error
            transaction.rollback()
            raise e

def downgrade():
    # Start transaction
    connection = op.get_bind()
    with connection.begin() as transaction:
        try:
            # Add back old columns
            op.add_column('asset', sa.Column('type', sa.String(50), nullable=False, server_default='Other'))
            op.add_column('asset', sa.Column('maturity_month', sa.Integer(), nullable=True))
            
            # Drop new icon column
            op.drop_column('asset', 'icon')
            
            # Add back old icon column
            op.add_column('asset', sa.Column('icon', sa.String(200), nullable=True))
            
            # Make maturity_year nullable again
            op.alter_column('asset', 'maturity_year',
                existing_type=sa.Integer(),
                nullable=True)
            
            # Commit transaction
            transaction.commit()
        except Exception as e:
            # Rollback on error
            transaction.rollback()
            raise e 