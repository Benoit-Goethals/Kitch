import asyncio


from database_layer.db_service import DBService


async def main():
    db_service = DBService()
    all_pers = await db_service.read_all_persons()
    if all_pers is None:
        print("No klanten found.")
        return
    print("Persons:")
    for klant in all_pers:
        print(klant)


    all_companys = await db_service.read_all_companies()
    if all_companys is None:
        print("No companies found.")
        return
    print("Companies:")
    for company in all_companys:
        print(company)

    all_companys = await db_service.read_all_companies()
    if all_companys is None:
        print("No companies found.")
        return
    print("Companies:")
    for company in all_companys:
        print(company)

    print("Address")
    all_address = await db_service.read_all_address()
    if all_address is None:
        print("No address found.")
        return
    for address in all_address:
        print(address)





if __name__ == "__main__":
    asyncio.run(main())
