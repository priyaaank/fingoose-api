"""update asset maturity date

Revision ID: 002
Revises: 001
Create Date: 2024-03-14
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns
    op.add_column('asset', sa.Column('maturity_month', sa.Integer(), nullable=True))
    op.add_column('asset', sa.Column('maturity_year', sa.Integer(), nullable=True))
    
    # Update new columns from old data
    connection = op.get_bind()
    
    # Update the new columns directly from maturity_date
    connection.execute(
        'UPDATE asset SET maturity_month = MONTH(maturity_date), '
        'maturity_year = YEAR(maturity_date) '
        'WHERE maturity_date IS NOT NULL'
    )
    
    # Drop old column
    op.drop_column('asset', 'maturity_date')

def downgrade():
    # Add back the old column
    op.add_column('asset', sa.Column('maturity_date', sa.Date(), nullable=True))
    
    # Update old column from new data
    connection = op.get_bind()
    connection.execute(
        'UPDATE asset SET maturity_date = DATE(CONCAT(maturity_year, "-", maturity_month, "-01")) '
        'WHERE maturity_month IS NOT NULL AND maturity_year IS NOT NULL'
    )
    
    # Drop new columns
    op.drop_column('asset', 'maturity_year')
    op.drop_column('asset', 'maturity_month') 