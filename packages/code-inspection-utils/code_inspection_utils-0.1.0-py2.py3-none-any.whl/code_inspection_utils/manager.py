import logging
import sys
import shutil
import os

from datetime import datetime
from typing import Dict, Optional

# from .file_utils import calculate_md5, get_file_creation_date, get_file_list

DEFAULT_VERBOSE = False
DEFAULT_TRACE_PREFIX = "TRACE :: "

class Manager:
    """Class for profiling the data directory."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.trace_prefix = kwargs.get("trace_prefix", DEFAULT_TRACE_PREFIX)
        self.verbose = kwargs.get("verbose", DEFAULT_VERBOSE)

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _check_infile_status(self, infile: str = None, extension: str = None) -> None:
        """Check if the file exists, if it is a regular file and whether it has content.

        Args:
            infile (str): the file to be checked
            extension (str): optional - the file name extension

        Raises:
            None
        """

        error_ctr = 0

        if infile is None or infile == '':
            logging.error(f"'{infile}' is not defined")
            error_ctr += 1
        else:
            if not os.path.exists(infile):
                error_ctr += 1
                logging.error(f"'{infile}' does not exist")
            else:
                if not os.path.isfile(infile):
                    error_ctr += 1
                    logging.error(f"'{infile}' is not a regular file")
                if os.stat(infile).st_size == 0:
                    logging.error(f"'{infile}' has no content")
                    error_ctr += 1
                if extension is not None and not infile.endswith(extension):
                    logging.error(f"'{infile}' does not have filename extension '{extension}'")
                    error_ctr += 1

        if error_ctr > 0:
            logging.error(f"Detected problems with input file '{infile}'")
            sys.exit(1)


    def _backup_file(self, infile: str) -> str:
        """Backup the file.

        Args:
            infile (str): the file to be backed-up
        Returns:
            str: the name of the backed-up file
        Raises:
            Exception if the file does not exist
        """
        if os.path.exists(infile):
            bakfile = os.path.abspath(infile) + datetime.today().strftime("%Y-%m-%d-%H%M") + '.bak'
            shutil.copy(infile, bakfile)
            logging.info(f"Copied '{infile}' to '{bakfile}'")
            return bakfile
        else:
            raise Exception(f"File '{infile}' does not exist, so nothing to backup")

    def insert_trace_statements(self, infile: str, outfile: Optional[str]) -> None:
        self._check_infile_status(infile)
        if outfile is None:
            bakfile = self._backup_file(infile)
            outfile = infile
            infile = bakfile



        if infile.endswith(".pl") or infile.endswith(".pm"):
            self._process_perl_file(infile, outfile)
        elif infile.endswith(".py"):
            self._process_python_file(infile, outfile)
        else:
            raise Exception(f"Have not implemented support for file type '{infile}'")

    def _process_python_file(self, infile: str, outfile: str) -> None:
        logging.warning("NOT YET IMPLEMENTED")
        sys.exit(1)


    def _get_leading_whitespace(self, s) -> str:
        """Count the number of leading whitespaces in a string.

        Args:
            s (str): input string

        Returns:
            str: leading whitespaces
        """
        count = 0
        for char in s:
            if char.isspace():
                count += 1
            else:
                break  # Stop counting when a non-whitespace character is encountered
        leading_whitespace = ' ' * count
        return leading_whitespace

    # # Example usage:
    # input_string = "    This is an example string with leading whitespaces."
    # leading_whitespace_count = count_leading_whitespace(input_string)
    # print(f"Number of leading whitespaces: {leading_whitespace_count}")

    def _get_variables(self, cleaned_line: str) -> str:
        parts = cleaned_line.split(" ")
        variables = []
        for part in parts:
            part = part.replace("(", "").replace(")", "")
            if part.startswith("$"):
                var = part
                var_name = part.lstrip("$")
                variable = f"{var_name} '{var}'"
                variables.append(variable)
                logging.info(f"Found variable '{variable}'")

        return " ".join(variables)

    def _get_subroutine_name(self, cleaned_line: str) -> str:
        return cleaned_line.replace("sub ", "").strip().replace("{", "")

    def _process_perl_file(self, infile: str, outfile: str) -> None:
        logging.info(f"Will process Perl file '{infile}'")
        line_ctr = 0
        if_ctr = 0
        else_ctr = 0
        elsif_ctr = 0
        while_ctr = 0
        for_ctr = 0
        foreach_ctr = 0
        sub_ctr = 0
        trace_ctr = 0

        with open(infile, 'r') as f:
            with open(outfile, 'w') as of:
                for line in f:
                    line = line.rstrip()
                    line_ctr += 1
                    cleaned_line = line.strip()
                    if cleaned_line.startswith("if"):
                        if_ctr += 1
                        trace_ctr += 1
                        variables = self._get_variables(cleaned_line)
                        of.write(f"{line}\n")
                        leading_whitespace = self._get_leading_whitespace(line)
                        outline = leading_whitespace + f"print(\"{self.trace_prefix}if-{if_ctr} {variables}\\n\");"
                        of.write(f"    {outline}\n")
                        continue
                    if cleaned_line.startswith("else") or cleaned_line.replace(" ", "").startswith("}else"):
                        else_ctr += 1
                        trace_ctr += 1
                        variables = self._get_variables(cleaned_line)
                        of.write(f"{line}\n")
                        leading_whitespace = self._get_leading_whitespace(line)
                        outline = leading_whitespace + f"print(\"{self.trace_prefix}else-{else_ctr} {variables}\\n\");"
                        of.write(f"    {outline}\n")
                        continue
                    if cleaned_line.startswith("elsif") or cleaned_line.replace(" ", "").startswith("}elsif"):
                        elsif_ctr += 1
                        trace_ctr += 1
                        variables = self._get_variables(cleaned_line)
                        of.write(f"{line}\n")
                        leading_whitespace = self._get_leading_whitespace(line)
                        outline = leading_whitespace + f"print(\"{self.trace_prefix}elsif-{elsif_ctr} {variables}\\n\");"
                        of.write(f"    {outline}\n")
                        continue
                    if cleaned_line.startswith("while"):
                        while_ctr += 1
                        trace_ctr += 1
                        variables = self._get_variables(cleaned_line)
                        of.write(f"{line}\n")
                        leading_whitespace = self._get_leading_whitespace(line)
                        outline = leading_whitespace + f"print(\"{self.trace_prefix}while-{while_ctr} {variables}\\n\");"
                        of.write(f"    {outline}\n")
                        continue
                    if cleaned_line.startswith("foreach"):
                        foreach_ctr += 1
                        trace_ctr += 1
                        variables = self._get_variables(cleaned_line)
                        of.write(f"{line}\n")
                        leading_whitespace = self._get_leading_whitespace(line)
                        outline = leading_whitespace + f"print(\"{self.trace_prefix}foreach-{foreach_ctr} {variables}\\n\");"
                        of.write(f"    {outline}\n")
                        continue
                    if cleaned_line.startswith("for"):
                        for_ctr += 1
                        trace_ctr += 1
                        variables = self._get_variables(cleaned_line)
                        of.write(f"{line}\n")
                        leading_whitespace = self._get_leading_whitespace(line)
                        outline = leading_whitespace + f"print(\"{self.trace_prefix}for-{for_ctr} {variables}\\n\");"
                        of.write(f"    {outline}\n")
                        continue
                    if cleaned_line.startswith("sub"):
                        sub_ctr += 1
                        trace_ctr += 1
                        name = self._get_subroutine_name(cleaned_line)
                        of.write(f"{line}\n")
                        leading_whitespace = self._get_leading_whitespace(line)
                        outline = leading_whitespace + f"print(\"{self.trace_prefix}sub-{sub_ctr} {name}\\n\");"
                        of.write(f"    {outline}\n")
                        continue
                    of.write(f"{line}\n")


        if line_ctr > 0:
            logging.info(f"Read '{line_ctr}' lines from file '{infile}'")
        else:
            logging.info(f"Did not read any lines from file '{infile}'")

        if trace_ctr > 0:
            logging.info(f"Wrote '{trace_ctr}' trace statements to file '{outfile}'")
        else:
            logging.warning(f"Did not write any trace statements to the file '{outfile}'")


