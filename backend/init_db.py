from backend.database import Base, SessionLocal, engine
from backend.models import Customer


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        if not db.get(Customer, "101"):
            db.add_all([
                Customer(
                    id="101",
                    name="Rahul Kumar",
                    phone="9876543210",
                    outstanding=3500
                ),
                Customer(
                    id="102",
                    name="Priya Sharma",
                    phone="9123456780",
                    outstanding=1200
                ),
                Customer(
                    id="103",
                    name="Amit Singh",
                    phone="9988776655",
                    outstanding=7500
                )
            ])

            db.commit()
    finally:
        db.close()