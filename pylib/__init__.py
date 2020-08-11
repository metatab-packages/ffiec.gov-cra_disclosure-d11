""" Example pylib functions"""



def extract(resource, doc, *args, **kwargs):
    """Extract rows from an FFIEC disclosire file, from a collection of Root.References,
    for a given prefix

    This function is used as a program URL in a Root.DataFile term:

    Section: Resources
    DataFile:       python:publicdata.ffiec#extract
    Datafile.Name:  sb_loan_orig
    Datafile.Schema:cra_disclosure
    Datafile.Prefix:D1-1

    The schema for the table must be specified, because the rows are fixed width, so
    the schema must have a Column.Width for each column.

    The function also expects that all of the references in the document refer to FFEIC file, such as:

    Section: References
    Reference: https://www.ffiec.gov/cra/xls/15exp_discl.zip
    Reference.Name: discl_15
    Reference: https://www.ffiec.gov/cra/xls/14exp_discl.zip
    Reference.Name: discl_14
    Reference: https://www.ffiec.gov/cra/xls/13exp_discl.zip
    Reference.Name: discl_13
    Reference: https://www.ffiec.gov/cra/xls/12exp_discl.zip
    Reference.Name: discl_12
    Reference: https://www.ffiec.gov/cra/xls/11exp_discl.zip
    Reference.Name: discl_11
    Reference: https://www.ffiec.gov/cra/xls/10exp_discl.zip
    Reference.Name: discl_10


    """

    test = bool(resource.get_value('test', False))

    prefix = resource.prefix

    table = resource.row_processor_table()

    yield table.headers

    parser = table.make_fw_row_parser(ignore_empty=True)

    for r in doc.references():

        print("Processing ", r.name)

        t = r.resolved_url.get_resource().get_target()

        with open(t.fspath, 'rU') as f:

            for line in (islice(f.readlines(), 10) if test else f.readlines()):
                if not line.startswith(prefix+' '):
                    continue

                yield parser(line)


def row_generator(resource, doc, env, *args, **kwargs):
    """ An example row generator function.

    Reference this function in a Metatab file as the value of a Datafile:

            Datafile: python:pylib#row_generator

    The function must yield rows, with the first being headers, and subsequenct rows being data.

    :param resource: The Datafile term being processed
    :param doc: The Metatab document that contains the term being processed
    :param args: Positional arguments passed to the generator
    :param kwargs: Keyword arguments passed to the generator
    :return:


    The env argument is a dict with these environmental keys:

    * CACHE_DIR
    * RESOURCE_NAME
    * RESOLVED_URL
    * WORKING_DIR
    * METATAB_DOC
    * METATAB_WORKING_DIR
    * METATAB_PACKAGE

    It also contains key/value pairs for all of the properties of the resource.

    """

    yield 'a b c'.split()

    for i in range(10):
        yield [i, i * 2, i * 3]


def example_transform(v, row, row_n, i_s, i_d, header_s, header_d, scratch, errors, accumulator):
    """ An example column transform.

    This is an example of a column transform with all of the arguments listed. An real transform
    can omit any ( or all ) of these, and can supply them in any order; the calling code will inspect the
    signature.

    When the function is listed as a transform for a column, it is called for every row of data.

    :param v: The current value of the column
    :param row: A RowProxy object for the whiole row.
    :param row_n: The current row number.
    :param i_s: The numeric index of the source column
    :param i_d: The numeric index for the destination column
    :param header_s: The name of the source column
    :param header_d: The name of the destination column
    :param scratch: A dict that can be used for storing any values. Persists between rows.
    :param errors: A dict used to store error messages. Persists for all columns in a row, but not between rows.
    :param accumulator: A dict for use in accumulating values, such as computing aggregates.
    :return: The final value to be supplied for the column.
    """

    return str(v) + '-foo'


def custom_update(doc, args):
    """Custom update function, run with `mp update -U`

    The args argument will recieve any remainder arguments from the call, for instance

        mp update -U -- --foo bar

    """

    doc.reference('source')

    doc.write()
