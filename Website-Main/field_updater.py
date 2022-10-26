# https://api.libreoffice.org/docs/idl/ref/
# https://wiki.documentfoundation.org/Development/DispatchCommands
# https://wiki.openoffice.org/wiki/Python/Transfer_from_Basic_to_Python

try:
    import uno
except ImportError:
    raise ImportError(
        "Could not find the 'uno' library. This package must be installed with a Python "
        "installation that has a 'uno' library. This typically means you should install "
        "it with the same Python executable as your Libreoffice installation uses."
    )

import argparse
import io
import logging
import os
import sys
import unohelper

from com.sun.star.beans import PropertyValue
from com.sun.star.io import XOutputStream

logger = logging.getLogger("unoserver")

SFX_FILTER_IMPORT = 1
SFX_FILTER_EXPORT = 2
DOC_TYPES = {
    "com.sun.star.sheet.SpreadsheetDocument",
    "com.sun.star.text.TextDocument",
    "com.sun.star.presentation.PresentationDocument",
    "com.sun.star.drawing.DrawingDocument",
    "com.sun.star.sdb.DocumentDataSource",
    "com.sun.star.formula.FormulaProperties",
    "com.sun.star.script.BasicIDE",
    "com.sun.star.text.WebDocument",  # Supposedly deprecated? But still around.
}


def prop2dict(properties):
    return {p.Name: p.Value for p in properties}


def get_doc_type(doc):
    for t in DOC_TYPES:
        if doc.supportsService(t):
            return t

    # LibreOffice opened it, but it's not one of the known document types.
    # This really should only happen if a future version of LibreOffice starts
    # adding document types, which seems unlikely.
    raise RuntimeError(
        "The input document is of an unknown document type. This is probably a bug.\n"
        "Please create an issue at https://github.com/unoconv/unoserver."
    )

def absoluteUrl(relativeFile):
    """Constructs absolute path to the current dir in the format required by PyUNO that working with files"""
    return "file:///" + os.path.realpath(".") + "/" + relativeFile
class OutputStream(unohelper.Base, XOutputStream):
    def __init__(self):
        self.buffer = io.BytesIO()

    def closeOutput(self):
        pass

    def writeBytes(self, seq):
        self.buffer.write(seq.value)


class UNO:
    def __init__(self, interface="127.0.0.1", port="2002"):
        logger.info("Starting unoconverter.")

        self.local_context = uno.getComponentContext()
        self.resolver = self.local_context.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", self.local_context
        )
        self.context = self.resolver.resolve(
            f"uno:socket,host={interface},port={port};urp;StarOffice.ComponentContext"
        )
        self.service = self.context.ServiceManager
        self.desktop = self.service.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.context
        )
        self.filter_service = self.service.createInstanceWithContext(
            "com.sun.star.document.FilterFactory", self.context
        )
        self.type_service = self.service.createInstanceWithContext(
            "com.sun.star.document.TypeDetection", self.context
        )

    def find_filter(self, import_type, export_type):
        # List export filters. You can only search on module, iflags and eflags,
        # so the import and export types we have to test in a loop
        export_filters = self.filter_service.createSubSetEnumerationByQuery(
            "getSortedFilterList():iflags=2"
        )

        while export_filters.hasMoreElements():
            # Filter DocumentService here
            export_filter = prop2dict(export_filters.nextElement())
            if export_filter["DocumentService"] != import_type:
                continue
            if export_filter["Type"] != export_type:
                continue

            # There is only one possible filter per import and export type,
            # so the first one we find is correct
            return export_filter["Name"]

        # No filter found
        return None

    # def BytesToDOC_URL(self, bytes, document):
    #     # input_props = (PropertyValue(Name="ReadOnly", Value=False),)
    #
    #     input_stream = self.service.createInstanceWithContext(
    #         "com.sun.star.io.SequenceInputStream", uno.getComponentContext()
    #     )
    #     input_stream.initialize((uno.ByteSequence(fortnite),))
    #     input_props = (PropertyValue(Name="InputStream", Value=input_stream),
    #                    # PropertyValue(Name="Frame", Value=document.getCurrentController().getFrame()),
    #                    PropertyValue(Name="Filter", Value="writer8")
    #                    )
    #     input_props = (PropertyValue(Name="Filter", Value="writer8"),)
    #     path = "file:///C:\\Users\Jared\Pycharmrojects\\UNO\doc.docx"
    #     # path = "private:stream"
    #
    #     return path, input_props


    def update(self, inpath=None, indata=None, outpath=None, convert_to=None):
        input_props = (PropertyValue(Name="ReadOnly", Value=False),)

        input_stream = self.service.createInstanceWithContext(
            "com.sun.star.io.SequenceInputStream", uno.getComponentContext()
        )
        input_stream.initialize((uno.ByteSequence(indata),))
        input_props += (PropertyValue(Name="InputStream", Value=input_stream),)
        import_path = "private:stream"

        document = self.desktop.loadComponentFromURL(
            import_path, "_default", 0, input_props
        )

        CTX = uno.getComponentContext()
        SM = CTX.getServiceManager()
        def create_instance(name, with_context=False):
            if with_context:
                instance = SM.createInstanceWithContext(name, CTX)
            else:
                instance = SM.createInstance(name)
            return instance

        def call_dispatch(doc, url, args=()):
            frame = doc.getCurrentController().getFrame()
            dispatch = create_instance('com.sun.star.frame.DispatchHelper')
            dispatch.executeDispatch(frame, url, '', 0, args)
            return

        def _toProperties(**kwargs):
            props = []
            for key in kwargs:
                prop = PropertyValue()
                prop.Name = key
                prop.Value = kwargs[key]
                props.append(prop)
            return tuple(props)

        search = document.createSearchDescriptor()
        search.SearchAll = True
        search.SearchWords = True
        search.SearchCaseSensitive = False

        # path, prop = self.BytesToDOC_URL(indata)

        # search.SearchString = "COMPANY_NAME"
        # selsFound = document.findAll(search)
        # safety.setString("BRUH")

        call_dispatch(document,'.uno:UpdateAll') # Update all fields

        # Now do the conversion
        try:
            # Figure out document type:
            import_type = get_doc_type(document)

            if outpath:
                export_path = uno.systemPathToFileUrl(os.path.abspath(outpath))
            else:
                export_path = "private:stream"

            # Figure out the output type:
            if convert_to:
                export_type = self.type_service.queryTypeByURL(
                    f"file:///dummy.{convert_to}"
                )
            else:
                export_type = self.type_service.queryTypeByURL(export_path)

            if not export_type:
                if convert_to:
                    extension = convert_to
                else:
                    extension = os.path.splitext(outpath)[-1]
                raise RuntimeError(
                    f"Unknown export file type, unknown extension '{extension}'"
                )

            filtername = self.find_filter(import_type, export_type)
            if filtername is None:
                raise RuntimeError(
                    f"Could not find an export filter from {import_type} to {export_type}"
                )

            logger.info(f"Exporting to {outpath}")
            logger.info(f"Using {filtername} export filter")

            output_props = (
                PropertyValue(Name="FilterName", Value=filtername),
                PropertyValue(Name="Overwrite", Value=True),
            )
            if outpath is None:
                output_stream = OutputStream()
                output_props += (
                    PropertyValue(Name="OutputStream", Value=output_stream),
                )
            document.storeToURL(export_path, output_props)

        finally:
            document.close(True)

        # if outpath is None:
        return output_stream.buffer.getvalue()
        # else:
        #     return None
        # return output_stream.buffer.getvalue()



# interface = "127.0.0.1"
# port = "60771"
# converter = UnoConverter(interface, port)
# from io import BytesIO
# with open('doc.docx') as f:
#     indata = f.buffer.read()
# with open('C:\\Users\Jared\Downloads\\fortnite.odt') as f:
#     fortnite = f.buffer.read()
#
# def update_fields(input):
#     result = converter.convert(
#         indata=input, convert_to="pdf"
#     )
#     return result
#
# with open('output.pdf', 'wb') as f:
#     f.write(update_fields(indata))
