from django.core.files import File

import string
from celery import Task
from io import BytesIO
from random import randint, choice
from PIL import ImageDraw, Image

from conf.celery import app
from courses.models import Course, Homework, Mark


class GenerateCourseImageTask(Task):
    name = 'generate_course_image_based_on_title'

    def run(self, course_pk, *args, **kwargs):
        course = Course.objects.get(pk=course_pk)
        if not course.picture:
            image_width = 1200
            image_high = 630
            image_background = "#FFFFFF"

            image = Image.new("RGB", (image_width, image_high), image_background)
            draw = ImageDraw.Draw(image)

            r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
            dr = (randint(0, 255) - r) / 500.0
            dg = (randint(0, 255) - g) / 500.0
            db = (randint(0, 255) - b) / 500.0
            for i in range(image_width):
                r, g, b = r + dr, g + dg, b + db
                draw.line((i, 0, i, image_high), fill=(int(r), int(g), int(b)))

            w, h = draw.textsize(course.name)
            draw.text(
                xy=((image_width - w) / 2, (image_high - h) / 2),
                text=course.name,
                fill="black",
            )
            blob = BytesIO()
            image.save(blob, "PNG")
            course.picture.save(f"{course.name}_{self.random_string()}.png", File(blob))

    @staticmethod
    def random_string():
        letters = string.ascii_letters
        return "".join(choice(letters) for _ in range(10))


class CalculateAverageMarkTask(Task):
    def run(self, *args, **kwargs):
        for homework in Homework.objects.all():
            counter = 0
            for answer in homework.answers.all():
                if Mark.objects.filter(homework_answer=answer).exists():
                    counter += answer.mark.mark
            if counter:
                homework.average_mark = counter / homework.answers.count()
            else:
                homework.average_mark = 0
            homework.save()


app.register_task(CalculateAverageMarkTask)
app.register_task(GenerateCourseImageTask)
