"""
This module provide mixins(rest_framework) for access to auditor features

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class AuditModelViewSetMixin(object):
    """
    function that decorates ModelViewSet class
    """

    queryset = None

    @action(['get'], detail=True, url_name="audited_log", url_path="audited_log")
    def _audited_log(self, request, pk=None, format=None, id=None):
        """
        Return a list of all audited data.
        """
        if not self.queryset:
            raise LookupError("You must override the queryset param!")

        model = self.queryset.model

        primary_key = pk
        if not primary_key:
            primary_key = id
            if not id:
                return Response(
                    data={"detail": "You must provide 'pk' param"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            data=model.get_audited_log(primary_key, limit=0),  # TODO: do the limit lookup(remove mocking by zero)
            status=status.HTTP_200_OK
        )
