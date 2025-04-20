from sqlalchemy.connectors import asyncio

from database_layer.db_service import DBService


async def main():
    db_service = DBService()
    all_klanten = await db_service.read_all_klant()
    if all_klanten is None:
        print("No klanten found.")
        return
    for klant in all_klanten:
        print(klant)


if __name__ == "__main__":
    asyncio.run(main())
