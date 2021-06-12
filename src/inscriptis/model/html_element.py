from inscriptis.html_properties import Display, HorizontalAlignment, \
    VerticalAlignment, WhiteSpace


class HtmlElement:
    """
    The HtmlElement class stores the following CSS properties of HTML
    elements:

    - tag: tag name of the given HtmlElement.
    - prefix: specifies a prefix that to insert before the tag's content.
    - suffix: a suffix to append after the tag's content.
    - display: :class:`~inscriptis.html_properties.Display` strategy used for
      the content.
    - margin_before: vertical margin before the tag's content.
    - margin_after: vertical margin after the tag's content.
    - padding_inline: horizontal padding_inline before the tag's content.
    - whitespace: the :class:`~inscriptis.html_properties.Whitespace` handling
      strategy.
    - limit_whitespace_affixes: limit printing of whitespace affixes to
      elements with `normal` whitespace handling.
    """

    __slots__ = ('canvas', 'tag', 'prefix', 'suffix', 'display',
                 'margin_before', 'margin_after', 'padding_inline',
                 'list_bullet', 'whitespace', 'limit_whitespace_affixes',
                 'align', 'valign', 'previous_margin_after', 'annotation')

    def __init__(self, tag='default', prefix='', suffix='',
                 display=Display.inline,
                 margin_before=0, margin_after=0, padding_inline=0,
                 list_bullet='',
                 whitespace=None, limit_whitespace_affixes=False,
                 align=HorizontalAlignment.left,
                 valign=VerticalAlignment.middle,
                 annotation=()):
        self.canvas = None
        self.tag = tag
        self.prefix = prefix
        self.suffix = suffix
        self.display = display
        self.margin_before = margin_before
        self.margin_after = margin_after
        self.padding_inline = padding_inline
        self.list_bullet = list_bullet
        self.whitespace = whitespace
        self.limit_whitespace_affixes = limit_whitespace_affixes
        self.align = align
        self.valign = valign
        self.previous_margin_after = 0
        self.annotation = annotation

    def __copy__(self) -> 'HtmlElement':
        """
        Improved copy implementation.
        """
        copy = self.__class__.__new__(self.__class__)
        for attr in self.__slots__:
            setattr(copy, attr, getattr(self, attr))
        return copy

    def write(self, text: str):
        """
        Writes the given HTML text.
        """
        if not text or self.display == Display.none:
            return

        self.canvas.write(self, ''.join(
            (self.prefix, text, self.suffix)))

    def write_tail(self, text: str):
        """
        Writes the tail text of an element.

        Args:
            text: the text to write
        """
        if not text or self.display == Display.none:
            return
        self.write(text)

    def set_canvas(self, canvas) -> 'HtmlElement':
        self.canvas = canvas
        return self

    def set_tag(self, tag: str) -> 'HtmlElement':
        self.tag = tag
        return self

    def write_verbatim_text(self, text: str):
        """
        Writes the given text verbatim to the canvas.
        Args:
            text: the text to write
        """
        if not text:
            return

        if self.display == Display.block:
            self.canvas.open_block(self)

        self.canvas.write(self, text, whitespace=WhiteSpace.pre)

        if self.display == Display.block:
            self.canvas.close_block(self)

    def get_refined_html_element(self, new) -> 'HtmlElement':
        """
        Computes the new HTML element based on the previous one.

        Adaptations:
            margin_top: additional margin required when considering
                        margin_bottom of the previous element

        Args:
            new: The new HtmlElement to be applied to the current context.

        Returns:
            The refined element with the context applied.
        """
        new.canvas = self.canvas

        # inherit `display:none` attributes and ignore further refinements
        if self.display == Display.none:
            new.display = Display.none
            return new

        # no whitespace set => inherit
        new.whitespace = new.whitespace or self.whitespace

        # do not display whitespace only affixes in Whitespace.pre areas
        # if `limit_whitespace_affixes` is set.
        if (new.limit_whitespace_affixes
                and self.whitespace == WhiteSpace.pre):
            if new.prefix.isspace():
                new.prefix = ''
            if new.suffix.isspace():
                new.suffix = ''

        if new.display == Display.block and self.display == Display.block:
            new.previous_margin_after = self.margin_after
        return new

    def __str__(self):
        return (
            '<{self.tag} prefix={self.prefix}, suffix={self.suffix}, '
            'display={self.display}, margin_before={self.margin_before}, '
            'margin_after={self.margin_after}, '
            'padding_inline={self.padding_inline}, '
            'list_bullet={self.list_bullet}, '
            'whitespace={self.whitespace}, align={self.align}, '
            'valign={self.valign}, annotation={self.annotation}>'
        ).format(self=self)

    __repr__ = __str__


"""
An empty default HTML element.
"""
DEFAULT_HTML_ELEMENT = HtmlElement()
