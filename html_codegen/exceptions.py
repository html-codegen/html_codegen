class HTMLCodeGenError(Exception):
    pass


class NodeValidationError(HTMLCodeGenError):
    pass


class NodeAlreadyHasParentError(NodeValidationError):
    pass


class TextNodeNestingError(NodeValidationError):
    pass


class SingleTagNestingError(NodeValidationError):
    pass


class TagPlacementError(HTMLCodeGenError):
    pass


class TagOutsideHtmlError(TagPlacementError):
    pass


class DuplicateTagError(TagPlacementError):
    pass


class OnlyTextContentError(HTMLCodeGenError):
    pass


class BrythonNotEnabledError(HTMLCodeGenError):
    pass
