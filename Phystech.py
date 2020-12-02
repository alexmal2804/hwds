"""
ДОП Задание к ДЗ (Необязательно к выполнению, но приносит доп. балл)

Дополните класс Phystech так, чтобы у пользователей появился список друзей. Пользователи должны быть в состоянии
добавлять других в друзья по uid, удалять других из друзей; смотреть на список общих друзей; проверять, приняли ли
заявку в друзья; видеть актуальный список входящих и исходящих заявок; запрещать конкретным пользователям добавлять себя
 в друзья.
При этом любое действие пользователя должно обновлять переменную self.last_online, а история её значений для каждого из
пользователей должна накапливаться в статическом поле класса (т.е. должен быть Dict[int, List[datetime]] -- отображение
из uid в историю сеансов. Задание с двумя звёздочками -- сгенерировать 20 случайных пользователей, случайным образом
просимулировать их взаимодействия, затем собрать pandas.DataFrame с данными о том, когда пользователи были онлайн и
сколько у разных пользователей общих друзей, а потом визуализировать эти данные в seaborn с помощью line plots и heatmap
соответственно.
"""
from datetime import datetime
from typing import Optional
from collections import defaultdict


class Phystech:
    uid = 0
    list_online = defaultdict(list)
    stop_list = defaultdict(list)
    friend_list = defaultdict(list)

    def __init__(
            self,
            name: str,
            login: str,
            password: str,
            friends: list = [],
            graduation_year: Optional[int] = None,
            birthday: Optional[datetime] = None,
            status: Optional[str] = None,
    ):
        self.name = name
        self.status = status
        self.__uid = Phystech.uid
        self.last_online = datetime.now()
        Phystech.list_online[self.__uid].append(self.last_online)
        Phystech.uid += 1

        self._birthday = birthday
        self._graduation_year = graduation_year
        self.__login = login
        self.__password = password
        self.friends = friends

    @property
    def is_graduate(self) -> Optional[bool]:
        if self._graduation_year is not None:
            return datetime.now().year - self._graduation_year > 0
        return None

    def set_last_online(self):
        self.last_online = datetime.now()
        Phystech.list_online[self.get_uid()].append(self.last_online)

    def __str__(self) -> str:
        str_repr_lines = [
            f'НаФизтехе. Пользователь \"{self.name}\".',
            'День рождения: {}'.format(
                self._birthday if self._birthday is not None else '(скрыт)'
            ),
            f'Статус: \"{self.status}\".',
            f'Последний раз был онлайн {self.last_online}'
        ]
        if self.is_graduate is not None:
            if self.is_graduate:
                str_repr_lines.append(
                    f'Выпускник {self._graduation_year} года'
                )
        return '\n'.join(str_repr_lines)

    def __repr__(self) -> str:
        return '\n'.join([
            f'uid:\t{self.__uid}',
            f'last_online:\t{self.last_online}',
        ])

    def get_uid(self) -> Optional[int]:
        if self.__uid is not None:
            return self.__uid
        else:
            return None

    def add_friend(self, uid: int):
        if self.get_uid() not in Phystech.stop_list[uid]:
            self.friends.append(uid)
        else:
            print(f'Вы не можете добавить пользователя с идентификатором {uid} в друзья')
        self.set_last_online()

    def set_stop_list(self, uid: int):
        Phystech.stop_list[self.get_uid()].append(uid)
        self.set_last_online()

    def print_friends(self):
        print('\nМеня зовут', self.name)
        print('Мой список актвинотсей ', self.get_uid(), Phystech.list_online[self.get_uid()])
        print('Мой список друзей ', self.friends)
        print('Мой стоп-лист', self.get_uid(), Phystech.stop_list[self.get_uid()])
        self.set_last_online()


ovchinkin = Phystech(
    name='Овчинкин Владимир Александрович',
    birthday=datetime(year=1946, month=6, day=9),
    status='Знаете, как много надо знать, чтобы понять, как мало мы знаем.',
    login='ovchinkin',
    graduation_year=2021,
    password='general_physics_rules'
)
paul_simon = Phystech(
    name='Пол Саймон',
    login='paul_simon',
    graduation_year=1986,
    password='I<3English',
    status='Sapere Aude!'
)

landau = Phystech(
    name='Лев Давидович Ландау',
    birthday=datetime(year=1908, month=1, day=22),
    status='Главное – делайте все с увлечением: это страшно украшает жизнь.',
    login='dau',
    password='I<3Physics'
)

# landau.print_friends()
ovchinkin.add_friend(landau.get_uid())
ovchinkin.add_friend(paul_simon.get_uid())
ovchinkin.print_friends()
landau.set_stop_list(paul_simon.get_uid())
landau.print_friends()
paul_simon.add_friend(landau.get_uid())
