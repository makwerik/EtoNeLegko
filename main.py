
import asyncio

from service.fetch import get_image, fetch


URL = "https://avatars.mds.yandex.net/i?id=ce15335bb16d67bd6f65c38a031ca85b_l-5569949-images-thumbs&n=13"


async def main():
    avg_time, mb_size, speed = await get_image(
        url=URL,
        count=10,
        sync=True
    )

    print(f"Среднее время запроса: {avg_time:.3f} сек.")
    print(f"Общий объем данных: {mb_size:.3f} МБ")
    print(f"Скорость скачивания: {speed:.3f} МБ/с")


if __name__ == "__main__":
    asyncio.run(main())
