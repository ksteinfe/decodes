using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DcPython.Decodes
{
    public class DecodesAppendedCode
    {
        public static string header = @"## -- BEGIN DECODES HEADER -- ##
import decodes.core as dc
from decodes.core import *
exec(dc.innies.ghIn.component_header_code)
exec(dc.outies.ghOut.component_header_code)
## -- END DECODES HEADER -- ##




"; // this makes it an even ten lines of code for header.  line numbers in text editor start on 11, the same line this comment is on.

        public static string footer = @"
## -- BEGIN DECODES FOOTER -- ##
exec(dc.innies.ghIn.component_footer_code)
exec(dc.outies.ghOut.component_footer_code)
## -- END DECODES FOOTER -- ##

";
    }
}
