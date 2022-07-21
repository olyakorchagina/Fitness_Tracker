from dataclasses import dataclass, asdict
from typing import List, Dict, Union, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    TXT_MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return self.TXT_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # расстояние в метрах, преодолённое за один шаг
    M_IN_KM: float = 1000   # метров в километре
    MIN_IN_H: float = 60    # минут в часе

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    # Коэффициенты для расчёта расхода калорий при беге
    COEFF_CAL_1: float = 18
    COEFF_CAL_2: float = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CAL_1 * self.get_mean_speed() - self.COEFF_CAL_2)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # Коэффициенты для расчёта расхода калорий при ходьбе
    COEFF_CAL_1: float = 0.035
    COEFF_CAL_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CAL_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CAL_2 * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # расстояние в метрах, преодолённое за один гребок

    # Коэффициенты для расчёта расхода калорий при плавании
    COEFF_CAL_1: float = 1.1
    COEFF_CAL_2: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CAL_1)
                * self.COEFF_CAL_2 * self.weight)


def read_package(
    workout_type: str,
    data: List[Union[float, int]]
) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_comparison: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in type_comparison:
        raise ValueError(
            'Неизвестный тип тренировки. '
            'Допустимые значения: "SWM", "RUN", "WLK".'
        )

    return type_comparison[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)