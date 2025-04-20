import asyncio


from database_layer.db_service import DBService


async def main():
    db_service = DBService()
    all_pers = await db_service.read_all_persons()
    if all_pers is None:
        print("No klanten found.")
        return
    for klant in all_pers:
        print(klant)


if __name__ == "__main__":
    asyncio.run(main())
