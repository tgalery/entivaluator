import re
import sys

# ranges for illegal xml expressions
illegal_unichrs = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), (0x7F, 0x84),
                   (0x86, 0x9F), (0xD800, 0xDFFF), (0xFDD0, 0xFDDF),
                   (0xFFFE, 0xFFFF), (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF),
                   (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF), (0x5FFFE, 0x5FFFF),
                   (0x6FFFE, 0x6FFFF), (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
                   (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF), (0xBFFFE, 0xBFFFF),
                   (0xCFFFE, 0xCFFFF), (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
                   (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)
                   ]

# list of converted characters
illegal_ranges = ["%s-%s" % (unichr(low), unichr(high))
                  for (low, high) in illegal_unichrs
                  if low < sys.maxunicode]

# regular expression that captures the character ranges
illegal_xml_re = re.compile(u'[%s]' % u''.join(illegal_ranges))

# def int2utf8(n):
#     "A function for returning the "
#     return six.u(str(n))


def remove_illegal_chars(text):
    """
    A funcion for stripping illegal xml ranges from text.
    :param text: unicode
    """
    return re.sub(illegal_xml_re, '', text)
