"""update goal fields

Revision ID: 002
Revises: 001
Create Date: 2024-03-14
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = 'db2328d0e3d5'
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
            op.execute('ALTER TABLE goal CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
            
            # Drop old columns
            op.drop_column('goal', 'type')
            op.drop_column('goal', 'target_amount')
            op.drop_column('goal', 'current_value')
            op.drop_column('goal', 'target_month')
            op.drop_column('goal', 'expected_inflation')
            
            # Add new columns
            op.add_column('goal', sa.Column('icon', sa.String(10, collation='utf8mb4_unicode_ci'), nullable=False))
            # Set default icon after column is created
            connection.execute("UPDATE goal SET icon = _utf8mb4 '🎯'")
            
            op.add_column('goal', sa.Column('goal_creation_year', sa.Integer(), nullable=False, server_default='2024'))
            op.add_column('goal', sa.Column('projected_inflation', sa.Float(), nullable=False, server_default='0.0'))
            op.add_column('goal', sa.Column('initial_goal_value', sa.Float(), nullable=False, server_default='0.0'))
            
            # Remove server defaults
            op.alter_column('goal', 'goal_creation_year', server_default=None)
            op.alter_column('goal', 'projected_inflation', server_default=None)
            op.alter_column('goal', 'initial_goal_value', server_default=None)
            
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
            op.add_column('goal', sa.Column('type', sa.String(50), nullable=False))
            op.add_column('goal', sa.Column('target_amount', sa.Float(), nullable=False))
            op.add_column('goal', sa.Column('current_value', sa.Float(), nullable=False))
            op.add_column('goal', sa.Column('target_month', sa.Integer(), nullable=False))
            op.add_column('goal', sa.Column('expected_inflation', sa.Float(), nullable=False))
            
            # Drop new columns
            op.drop_column('goal', 'icon')
            op.drop_column('goal', 'goal_creation_year')
            op.drop_column('goal', 'projected_inflation')
            op.drop_column('goal', 'initial_goal_value')
            
            # Commit transaction
            transaction.commit()
        except Exception as e:
            # Rollback on error
            transaction.rollback()
            raise e 