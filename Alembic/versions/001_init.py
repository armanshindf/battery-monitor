from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('devices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('firmware_version', sa.String(length=50), nullable=False),
        sa.Column('status', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('batteries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('nominal_voltage', sa.Float(), nullable=False),
        sa.Column('remaining_capacity', sa.Float(), nullable=False),
        sa.Column('lifespan', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('device_battery_link',
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('battery_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
        sa.ForeignKeyConstraint(['battery_id'], ['batteries.id'], ),
        sa.PrimaryKeyConstraint('device_id', 'battery_id')
    )

def downgrade():
    op.drop_table('device_battery_link')
    op.drop_table('batteries')
    op.drop_table('devices')