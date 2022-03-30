from django_filters import rest_framework as filters

from courses.models import Course


class CourseFilter(filters.FilterSet):
    id = filters.BaseInFilter(field_name='id')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    teachers = filters.CharFilter(method='filter_for_teachers')
    starts_at = filters.DateFromToRangeFilter(field_name='starts_at')

    @classmethod
    def filter_for_teachers(cls, qs, field_name, lookup_expr=None):
        teacher_ids = lookup_expr.split(',')
        return qs.filter(teachers__in=teacher_ids)

    ordering = filters.OrderingFilter(
        fields=('name', )
    )

    class Meta:
        model = Course
        fields = ('id', 'name', 'teachers', 'starts_at')
        search_fields = ['name']
