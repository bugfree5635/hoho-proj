from app.database.connection import engine

print(">>>>", engine.url)
with engine.connect() as conn:
    print("database connected")
