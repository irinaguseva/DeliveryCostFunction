from typing import Union


def calculate_delivery_cost(
        distance: float,
        small_sized: bool = True,
        fragile: bool = False,
        workload: str = "normal",
        ) -> Union[str, float]:
    """
    Функция рассчитывает стоимость доставки на основе входных параметров.

    Args:
        distance: Расстояние до пункта назначения в км.
        small_sized: Флаг маленьких габаритов (True - маленькие, False - большие).
        fragile: Флаг хрупкости груза.
        workload: Уровень загруженности службы доставки.

    Returns:
        Стоимость доставки в рублях (тип float) или сообщение об ошибке (тип str).
    """

    if distance < 0:
        raise ValueError("Distance cannot be negative")

    if distance > 30 and fragile:
        return "Unable to deliver fragile items at such a long distance"

    workload_coefficients = {
        "very_high": 1.6,
        "high": 1.4,
        "increased": 1.2,
        "normal": 1.0
    }
    if workload not in workload_coefficients:
        return "Invalid workload provided"

    if distance <= 2:
        delivery_cost = 50
    elif distance <= 10:
        delivery_cost = 100
    elif distance <= 30:
        delivery_cost = 200
    else:
        delivery_cost = 300

    delivery_cost += 100 if small_sized else 200

    if fragile:
        delivery_cost += 300

    current_coefficient = workload_coefficients[workload]
    delivery_cost *= current_coefficient

    delivery_cost = round(delivery_cost, 2)
    return max(delivery_cost, 400)
