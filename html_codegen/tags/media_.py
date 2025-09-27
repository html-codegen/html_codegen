"""
Медиа теги.
"""
from .base_ import SingleTag, Tag


class img(SingleTag):
    """
    This class represents an image tag in HTML. It inherits from the _SingleTag class.
    """


class audio(Tag):
    """
    This class represents an audio tag in HTML. It inherits from the _Tag class.
    """


class video(Tag):
    """
    This class represents a video tag in HTML. It inherits from the _Tag class.
    """


class source(SingleTag):
    """
    This class represents a source tag in HTML. It inherits from the _SingleTag class.
    """


class track(SingleTag):
    """
    This class represents a track tag in HTML. It inherits from the _SingleTag class.
    """


class iframe(Tag):
    """
    This class represents an iframe tag in HTML. It inherits from the _Tag class.
    """


class embed(SingleTag):
    """
    This class represents an embed tag in HTML. It inherits from the _SingleTag class.
    """


class object_(Tag):
    """
    This class represents an object tag in HTML. It inherits from the _Tag class.
    """


class param(SingleTag):
    """
    This class represents a param tag in HTML. It inherits from the _SingleTag class.
    """


class canvas(Tag):
    """
    This class represents a canvas tag in HTML. It inherits from the _Tag class.
    """


class svg(Tag):
    """
    This class represents an svg tag in HTML. It inherits from the _Tag class.
    """


class map_(Tag):
    """
    This class represents a map tag in HTML. It inherits from the _Tag class.
    """


class area(SingleTag):
    """
    This class represents an area tag in HTML. It inherits from the _SingleTag class.
    """
