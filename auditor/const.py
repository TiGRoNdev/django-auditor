"""
This module contains all necessary django-auditor constants

.. moduleauthor:: Igor Nazarov <tigron.dev@gmail.com>

"""
SAVE = 'SAVE'
DELETE = 'DELETE'
M2M_CHANGE = 'M2M_CHANGE'

ACTION_CHOICES = (
    (SAVE, SAVE),
    (DELETE, DELETE),
    (M2M_CHANGE, M2M_CHANGE)
)
