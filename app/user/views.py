"""
Views for the User API.
"""

from rest_framework import generics
from user.serializer import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new User in the system."""
    serializer_class = UserSerializer
