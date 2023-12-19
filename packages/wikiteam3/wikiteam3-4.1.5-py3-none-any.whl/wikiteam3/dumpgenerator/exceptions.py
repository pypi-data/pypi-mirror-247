class PageMissingError(Exception):
    def __init__(self, title, xml):
        self.title = title
        self.xml = xml

    def __str__(self):
        return "page '%s' not found" % self.title


class ExportAbortedError(Exception):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "Export from '%s' did not return anything." % self.index


class FileSizeError(Exception):
    def __init__(self, file, excpected_size):
        self.file = file
        self.excpected_size = excpected_size

    def __str__(self):
        return "File '%s' size is not match '%s'." % (self.file, self.excpected_size)


class FileSha1Error(Exception):
    def __init__(self, file, excpected_sha1):
        self.file = file
        self.excpected_sha1 = excpected_sha1

    def __str__(self):
        return "File '%s' sha1 is not match '%s'." % (self.file, self.excpected_sha1)
