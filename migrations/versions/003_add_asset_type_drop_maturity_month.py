"""add asset type drop maturity month

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
    
    with connection.begin() as transaction:
        try:
            # Add asset_type column
            op.add_column('asset', 
                sa.Column('asset_type', sa.String(50), nullable=False, server_default='Other'))
            
            # Remove server default after column is populated
            op.alter_column('asset', 'asset_type',
                existing_type=sa.String(50),
                server_default=None)
            
            # Get column information
            columns = [row[0] for row in op.get_bind().execute('SHOW COLUMNS FROM asset').fetchall()]
            
            # Drop maturity_month if it exists
            if 'maturity_month' in columns:
                op.drop_column('asset', 'maturity_month')

            # Drop type if it exists
            if 'type' in columns:
                op.drop_column('asset', 'type')
            
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
            # Add back maturity_month
            op.add_column('asset', 
                sa.Column('maturity_month', sa.Integer(), nullable=True))
            
            # Add back type
            op.add_column('asset', 
                sa.Column('type', sa.String(50), nullable=False, server_default='Other'))

            # Drop asset_type
            op.drop_column('asset', 'asset_type')
            
            # Commit transaction
            transaction.commit()
        except Exception as e:
            # Rollback on error
            transaction.rollback()
            raise e 