"""fill_tables

Revision ID: a19e2ebba6fb
Revises: f95f6e5ddb04
Create Date: 2025-04-12 14:50:43.891962

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy.orm import Session

from src.db.models import Table, Reservation

# revision identifiers, used by Alembic.
revision: str = 'a19e2ebba6fb'
down_revision: Union[str, None] = 'f95f6e5ddb04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    table1 = Table(name='Table_1', seats=6, location='общий зал')
    table2 = Table(name='Table_2', seats=2, location='терраса')
    table3 = Table(name='Table_3', seats=4, location='зал для некурящих')
    session.add_all([table1, table2, table3])
    session.flush()

    reserve1 = Reservation(customer_name='Anna', table_id=table1.id, reservation_time='2025-07-15T15:00:00',
                           duration_minutes=120)
    reserve2 = Reservation(customer_name='Inga', table_id=table2.id, reservation_time='2025-05-16T19:30:00',
                           duration_minutes=180)
    reserve3 = Reservation(customer_name='Ivan', table_id=table3.id, reservation_time='2025-06-01T11:45:00',
                           duration_minutes=90)
    reserve4 = Reservation(customer_name='Oleg', table_id=table1.id, reservation_time='2025-07-15T18:00:00',
                           duration_minutes=180)
    session.add_all([reserve1, reserve2, reserve3, reserve4])

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    session.query(Reservation).filter(
        Reservation.customer_name.in_(['Anna', 'Inga', 'Ivan', 'Oleg'])
    ).delete(synchronize_session=False)

    session.query(Table).filter(
        Table.name.in_(['Table_1', 'Table_2', 'Table_3', 'Oleg'])
    ).delete(synchronize_session=False)

    session.commit()
