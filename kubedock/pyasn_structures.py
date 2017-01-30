
# KuberDock - is a platform that allows users to run applications using Docker
# container images and create SaaS / PaaS based on these applications.
# Copyright (C) 2017 Cloud Linux INC
#
# This file is part of KuberDock.
#
# KuberDock is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# KuberDock is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with KuberDock; if not, see <http://www.gnu.org/licenses/>.

"""NDG HTTPS Client package

Use pyasn1 to provide support for parsing ASN.1 formatted subjectAltName
content for SSL peer verification.  Code based on:
"""
__author__ = "P J Kershaw"
__date__ = "01/02/12"
__copyright__ = "(C) 2012 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__revision__ = '$Id$'
try:
    from pyasn1.type import univ, constraint, char, namedtype, tag
except ImportError as e:
    import_error_msg = ('Error importing pyasn1, subjectAltName check for SSL '
                        'peer verification will be disabled.  Import error '
                        'is: %s' % e)
    import warnings
    warnings.warn(import_error_msg)

    class Pyasn1ImportError(ImportError):
        "Raise for pyasn1 import error"
    raise Pyasn1ImportError(import_error_msg)

MAX = 64


class DirectoryString(univ.Choice):
    """ASN.1 Directory string class"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType(
            'teletexString', char.TeletexString().subtype(
                subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
        namedtype.NamedType(
            'printableString', char.PrintableString().subtype(
                subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
        namedtype.NamedType(
            'universalString', char.UniversalString().subtype(
                subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
        namedtype.NamedType(
            'utf8String', char.UTF8String().subtype(
                subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
        namedtype.NamedType(
            'bmpString', char.BMPString().subtype(
                subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
        namedtype.NamedType(
            'ia5String', char.IA5String().subtype(
                subtypeSpec=constraint.ValueSizeConstraint(1, MAX))),
    )


class AttributeValue(DirectoryString):
    """ASN.1 Attribute value"""


class AttributeType(univ.ObjectIdentifier):
    """ASN.1 Attribute type"""


class AttributeTypeAndValue(univ.Sequence):
    """ASN.1 Attribute type and value class"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('type', AttributeType()),
        namedtype.NamedType('value', AttributeValue()),
    )


class RelativeDistinguishedName(univ.SetOf):
    '''ASN.1 Realtive distinguished name'''
    componentType = AttributeTypeAndValue()


class RDNSequence(univ.SequenceOf):
    '''ASN.1 RDN sequence class'''
    componentType = RelativeDistinguishedName()


class Name(univ.Choice):
    '''ASN.1 name class'''
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('', RDNSequence()),
    )


class Extension(univ.Sequence):
    '''ASN.1 extension class'''
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('extnID', univ.ObjectIdentifier()),
        namedtype.DefaultedNamedType('critical', univ.Boolean('False')),
        namedtype.NamedType('extnValue', univ.OctetString()),
    )


class Extensions(univ.SequenceOf):
    '''ASN.1 extensions class'''
    componentType = Extension()
    sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)


class AnotherName(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('type-id', univ.ObjectIdentifier()),
        namedtype.NamedType('value', univ.Any().subtype(
                            explicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 0)))
    )


class GeneralName(univ.Choice):
    '''ASN.1 configuration for X.509 certificate subjectAltNames fields'''
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('otherName', AnotherName().subtype(
                            implicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 0))),
        namedtype.NamedType('rfc822Name', char.IA5String().subtype(
                            implicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 1))),
        namedtype.NamedType('dNSName', char.IA5String().subtype(
                            implicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 2))),
        namedtype.NamedType('directoryName', Name().subtype(
                            implicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 4))),
        namedtype.NamedType('uniformResourceIdentifier', char.IA5String()
                            .subtype(
                            implicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 6))),
        namedtype.NamedType('iPAddress', univ.OctetString().subtype(
                            implicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 7))),
        namedtype.NamedType('registeredID', univ.ObjectIdentifier().subtype(
                            implicitTag=tag.Tag(tag.tagClassContext,
                                                tag.tagFormatSimple, 8))),
    )


class GeneralNames(univ.SequenceOf):
    '''Sequence of names for ASN.1 subjectAltNames settings'''
    componentType = GeneralName()
    sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)


class SubjectAltName(GeneralNames):
    '''ASN.1 implementation for subjectAltNames support'''
