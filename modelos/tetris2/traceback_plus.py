"""
traceback_plus.py

a modified version of python cookbook, page 342, recipe 8.6

Tracebacks, while handy, are rather limited in the amount of information
they contain. The actual traceback objects contain a massive amount of
information in the form of the local variables in the different frames
when the exception occured. The function contained in this module gives
you access to this plethra of information, it is used in the same way as
the traceback.print_exc() function.
"""
import sys, traceback

def print_exc_plus(File = sys.stdout):
    """ Print the usual traceback information, followed by a listing of
        all the local variables in each frame.

        keyword args:
            File : the file/file-like object that the "super traceback"
                   is printed to. Defaults to sys.stdout.
                   All that is required of a file-like object is a write
                   function accepting a string.
    """
    # first validate our File object by printing a header line
    try:
        File.write('Traceback Plus:\n\n')
    except:
        # the file-like object is invalid, fall back to sys.stdout
        # and tell the user about it in the new header
        File = sys.stdout
        File.write('Traceback Plus:\nWARNING: provided log file is invalid \n\n')

    tb = sys.exc_info()[2]
    while tb.tb_next:
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc(file = File)
    File.write('\nLocals by frame, innermost last\n')
    for frame in stack:
        File.write('\n')
        File.write("Frame %s in %s at line %s\n" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
                   )
        for key, value in frame.f_locals.items():
            # we must _absolutely_ avoid propagating exceptions, and str(value)
            # COULD cause any exception, so we MUST catch any...:
            try:
                File.write("\t%20s = " % key + str(value) + '\n')
            except:
                File.write("\t%20s = <ERROR WHILE PRINTING VALUE>\n" % key)



if __name__ == "__main__":
    # an example situation where you would use it:
    
    data = ['1', '2', 3, '4'] # Typo: we "forget" the quotes on the three
    def pad4(seq):
        """
        Pad each string in seq with zeros up to four places.
        Note that python already accomplishes this in a better and
        faster way, this is just an example.
        """
        return_value = []
        for thing in seq:
            return_value.append('0' * (4 - len(thing)) + thing)
        return return_value
    
    try:
        pad4(data)
    except:
        print_exc_plus()

    # note how easy it is to see that we forgot the quotes from data[2].
    
    # Where you would normally have to guess or wade through your code
    # to find the problem, you now have it right at your fingertips.

    # using this recipe has spawned a whole new programming methodology
    # for me, which not only improves speed, but productivity. In all situations
    # where it is possible, try to bring necessary variables into local scope.
    # this not only allows me to see what they are when exceptions occur, but
    # it also speeds up the program because looking up local variables is very fast.
