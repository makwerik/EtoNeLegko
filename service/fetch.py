import asyncio
import time
import aiohttp


async def get_image(url: str = None, count: int = 10,
                    headers: dict = None, cookies: dict = None, sync: bool = True) -> tuple:
    """
    Метод загрузки изображения
    :param url: Адрес изображения
    :param count: Количество запросов
    :param headers: Заголовки
    :param cookies: Печеньки
    :param sync: Синхронный режим (по умолчанию True)
    :return: Возвращает кортеж (среднее время загрузки, кол-во скачанных мб, скорость загрузки)
    """

    if not url:
        assert "Адрес изображения не передан"

    if count < 0:
        assert "Кол-во запросов не может быть отрицательным"

    # Общее время, которое мы суммируем
    all_times: list = []

    # Кол-во загруженных байтов
    count_bytes: int = 0

    if sync:
        async with aiohttp.ClientSession(headers=headers, cookies=cookies, timeout=aiohttp.ClientTimeout(60)) as session:
            for i in range(count):
                time_start = time.perf_counter()

                async with session.get(url=url) as response:
                    # Выдаст исключение, если не будет ответа 2хх
                    response.raise_for_status()

                    data = await response.read()

                time_finish = time.perf_counter() - time_start

                all_times.append(time_finish)
                count_bytes += len(data)

        total_time = sum(all_times)
        avg_time = total_time / 10
        mb_size = count_bytes / (1024 ** 2)
        speed = mb_size / total_time
    else:
        async with aiohttp.ClientSession(headers=headers, cookies=cookies, timeout=aiohttp.ClientTimeout(60)) as session:

            tasks = [fetch(session, url) for _ in range(count)]

            results = await asyncio.gather(*tasks)

            total_time = sum(t for t, size in results)
            avg_time = total_time / count

            count_bytes = sum(size for t, size in results)
            mb_size = count_bytes / (1024 ** 2)

            speed = mb_size / total_time

    return avg_time, mb_size, speed


async def fetch(session: aiohttp.ClientSession, url: str):
    """
    Метод для асинхронных запросов
    :param session: объект сессии
    :param url: адрес изображения
    :return:
    """
    start = time.perf_counter()

    async with session.get(url) as response:
        response.raise_for_status()
        data = await response.read()

    return time.perf_counter() - start, len(data)
