import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


COMMENDATIONS_TEXTS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!",
]


def fix_marks(schoolkid):
    schoolkid_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    )

    for bad_mark in schoolkid_bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)

    for chastisement in schoolkid_chastisements:
        chastisement.delete()


def create_commendation(schoolkid):
    lessons = Lesson.objects.filter(
        group_letter=schoolkid.group_letter,
        year_of_study=schoolkid.year_of_study
    )
    lesson = lessons.order_by("date").first()
    text = random.choice(COMMENDATIONS_TEXTS)

    commendation = Commendation.objects.get_or_create(
        subject=lesson.subject,
        schoolkid=schoolkid,
        created=lesson.date,
        teacher=lesson.teacher,
        text=text
    )


def improve_performance(schoolkid):
    create_commendation(schoolkid)
    remove_chastisements(schoolkid)
    fix_marks(schoolkid)
    return f"Теперь ученик {schoolkid.full_name} идеален!"


if __name__ == "__main__":
    try:
        name = input("Введите полное имя ученика: ")
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print("Такого ученика нет в базе!")
    except MultipleObjectsReturned:
        print("Найдено несколько учеников, уточните запрос!")

    print(improve_performance(schoolkid))
