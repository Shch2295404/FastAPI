"""Добавлено поле role в таблицу users

Revision ID: 5981c07e15f6
Revises: 6ae9b70856b1
Create Date: 2025-03-04 18:21:34.429594

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5981c07e15f6'
down_revision: Union[str, None] = '6ae9b70856b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Изменения в других таблицах (автогенерированные команды)
    op.alter_column('bookings', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('hotels', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=False)
    op.alter_column('hotels', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    
    # Создаем тип enum "userrole" (если его ещё нет)
    user_role_enum = sa.Enum('USER', 'DEVELOPER', 'ADMIN', name='userrole')
    user_role_enum.create(op.get_bind(), checkfirst=True)
    
    # Добавляем колонку role с типом enum, устанавливая временное значение по умолчанию
    op.add_column('users', sa.Column('role', user_role_enum, nullable=False, server_default='USER'))
    
    # После установки значений можно убрать значение по умолчанию, если оно не нужно в дальнейшем
    op.alter_column('users', 'role', server_default=None)


def downgrade() -> None:
    # Удаляем колонку role
    op.drop_column('users', 'role')
    
    # Удаляем тип enum "userrole"
    user_role_enum = sa.Enum('USER', 'DEVELOPER', 'ADMIN', name='userrole')
    user_role_enum.drop(op.get_bind(), checkfirst=True)
    
    # Остальные автогенерированные команды для отката
    op.alter_column('rooms', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('rooms', 'hotel_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('hotels', 'image_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('hotels', 'services',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               nullable=True)
    op.alter_column('bookings', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bookings', 'room_id',
               existing_type=sa.INTEGER(),
               nullable=True)
