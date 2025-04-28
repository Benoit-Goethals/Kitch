import asyncio

from database_layer.db_service import DBService


async def main():
    db_service = DBService()

    succes=await db_service.replace_lat_lon()

    if succes is True:
        print("Success")
    else:
        print("Error")





if __name__ == "__main__":
    asyncio.run(main())
