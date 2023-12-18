#!/usr/bin/env python

import logging
import json
import subprocess
from datetime import datetime


########################################################################################################################


def set_timestamp(s):
    """Returns a date object of a string in format %Y-%m-%d.

    The string has to be in the correct format, if not None is returned."""

    date_format = "%Y-%m-%d"
    try:
        ts = datetime.strptime(str(s), date_format)
    except ValueError:
        logging.error(f"Unable to convert provided argument '{str(s)}' to timestamp object")
        return

    return ts


class AzureKeyVaultReport(object):
    """
    Fetches the list of secrets in the specified key-vault

    The list is fetched by invoking the following shell command as subprocess:
    'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT'

    The values of 'updated', 'created' and 'expires' are converted to date object
    and the age (in days) is calculated.

    Then a table is generated and sorted by (from top to bottom):
    the oldest 'Expiration' date, then by
    the oldest 'Last Updated' date

    ...

    Attributes
    ----------
    vault_name : str
        The name of the vault
    result : json
        The raw result from the azure cli command
    items : list
        The list of items. After the age of each date element, for each item, is calculated.
    header : str
        The report header
    body : str
        The report body. Generated based on arguments passed to generate_report method and outcome of the az cli cmd
    footer : str
        The report footer, containing a summary.
    table_columns : tuple
        The table columns and width. Defaults to:
        'Secret Name'  : 50
        'Last Updated' : 18
        'Expiration'   : 18
        'Comment'      : 55
    sep_line : str
        The dotted line which separates the header and footer. Length is calculated by column widths
    lm : str
        The left margin space
    this_year : int
        Counter for secret records that have been updated within the last 365 days
    one_year : int
        Counter for secret records updated within the range between age of 365 and 730 days
    two_years : int
        Counter for secret records updated within the range between age of 730 and 1095 days
    three_years : int
        Counter for secret records updated within the last 3 years
    missing_expiration_date : int
        Counter for secret records which are missing an Expiration Date
    facts : list
        The list of facts used in MS Teams output
    html_table : str
        The html table used in MS Teams output

    Methods
    -------
    az_cmd()
        Execute the shell command
        'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT'
        and set the result to variable 'result'
    parse_results()
        Parse through the result from the azure cli keyvault output.

        For each item in the result;
        date objects are created from the 'updated', 'created' and 'expires' values and stored as values
        in new X_ts keys.

        The age (in days) is calculated from each of the date objects and stored as values in new X_age keys.

        For each item parsed, a new item is created and added to the items list.
    set_report_header()
        Set the header part of the report:
        At the top row with dashes, then
        left aligned columns with fixed width, separated by |
        then a new row with dashes
    generate_report()
        Creates a plain text report and initiates ms team report generation if specified.
        Returns the plain text report.
        The 'Comment' column created is generated according to the age of 'updated', 'created' and 'expires'.
        If missing 'expires' then a comment concerning that is also added.
    set_report_header()
        Add a summary footer to the report
    """

    def __init__(self, vault_name):
        """
        Parameters
        ----------
        vault_name : str
            The name of the key vault
        """

        self.vault_name = vault_name
        self.table_columns = (
            (50, "Secret Name"),
            (18, "Last Updated"),
            (18, "Expiration"),
            (55, "Comment")
        )
        self.missing_expiration_date = 0
        self.result = {}
        self.items = []
        self.header = ""
        self.body = ""
        self.footer = ""
        self.sep_line = ""    # A dotted line based on table column widths
        self.lm = " "         # Left margin
        self.this_year = 0    # Updated this year
        self.one_year = 0     # One year and older, but less than two years
        self.two_years = 0    # Two year and older, but less than three years
        self.three_years = 0  # Three years and older
        self.facts = []       # Facts used in the Teams output
        self.html_table = ""  # HTML table used in the Teams output
        self.json_output = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "-",
            "sections": [
                {
                    "activityTitle": self.vault_name,
                    "activitySubtitle": "",
                    "activityImage": "",
                    "facts": [],
                    "markdown": True
                },
                {
                    "startGroup": True,
                    "text": ""
                }
            ]
        }

    def az_cmd(self, path="", cmd=""):
        """invoke the 'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT' shell cmd

        Parameters
        ----------
        path : str
            Option to set path to where az is found. If not located in default PATH.
        cmd : str
            The shell subprocess command invoked to fetch the secret list
            (default: 'az keyvault secret list --vault-name NAME-OF-THE-KEY-VAULT')
        """

        if not cmd:
            cmd = f"az keyvault secret list --vault-name {self.vault_name}"

        if not isinstance(path, str):
            logging.error(f"Not a valid path: '{str(path)}'")
            return

        # If path provided, add it to cmd and ensure no double //
        if path:
            cmd = f"{path.rstrip('/')}/{cmd}"

        az = subprocess.run(cmd, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        az_stdout = az.stdout.decode("utf-8")
        if az_stdout:
            self.result = json.loads(az_stdout)
            return

        # Try to read stderr from cmd, but only if not stdout.
        logging.error(f"{cmd} returned with an error.")
        if az.stderr:
            try:
                az_stderr = az.stderr.decode("utf-8").rstrip()
            except:
                az_stderr = az.stderr.rstrip()
        else:
            return
        logging.error(f"Error output: '{az_stderr}'")

    def parse_results(self):
        """parse through the result from the azure cli keyvault cmd output"""
        if not isinstance(self.result, list):
            return

        now = datetime.now()
        for r in self.result:
            item = {}
            if isinstance(r, dict):
                a = r.get("attributes")
                item["name"] = r.get("name")
                if isinstance(a, dict):
                    for k, v in a.items():
                        if "updated" in k or "created" in k or "expires" in k and v:
                            value = v.split("T")[0]
                            item[k] = value
                            ts = set_timestamp(value)
                            item[f"{k}_ts"] = ts
                            age = (now - ts).days
                            item[f"{k}_age"] = age

                            # Update the update age counters:
                            # One year and older, but less than two years
                            if "updated" in k and age < 365:
                                self.this_year += 1

                            # One year and older, but less than two years
                            if "updated" in k and (365 <= age < 365 * 2):
                                self.one_year += 1

                            # Two year and older, but less than three years
                            elif "updated" in k and (365 * 2 <= age < 365 * 3):
                                self.two_years += 1

                            # Three years and older
                            elif "updated" in k and age >= 365 * 3:
                                self.three_years += 1

            self.items.append(item)

    def set_report_header(self):
        """set the header part of the report"""
        if not isinstance(self.result, list):
            return

        # Ensure the report variable is empty before heading is added to it
        self.header = ""

        # Create the dotted line part of the header. The length of the dotted row is each sum of chars from each column
        sep_line = ""
        for col in self.table_columns:
            sep_line += col[0] * "-"
        sep_line += "\n"
        self.sep_line = sep_line

        # Parse through each part of the header row. Element 0 is column total width. Element 1 is the actual value.
        header_row = ""
        for col in self.table_columns:
            header_row += f"| {col[1]: <{col[0]}}"

        # Add one dotted line row, the header row and one more dotted line row to the report
        self.header += self.sep_line
        self.header += f"{self.lm}{header_row.lstrip('| ')}"
        self.header += "\n"
        self.header += self.sep_line
        logging.info(f"header generated.")

    def generate_report(self, expire_threshold=None, ignore_no_expiration=True, include_all=False, teams_json=False):
        """creates a plain text report and initiates ms team report generation if specified.
        returns the plain text report.

        Parameters
        ----------
        expire_threshold : int
            Ignore to report the record if days till the secret will expire are more than this 'expire_threshold' value
            NOTE: Secrets expiring today or already expired will always be reported.
        ignore_no_expiration : bool
            Report all records if set to False. If set to True only secrets with Expiration Date set will be reported.
        include_all : bool
            If set to True all records are included in the output.
        teams_json : bool
            If set to True then a report in json format containing a html table will also be generated.
        """
        if not isinstance(self.result, list):
            return

        if not self.header:
            self.set_report_header()


        # Ensure empty body
        self.body = ""

        # Sort the items from top and down
        # First sort by the oldest 'Expiration' date
        # Then sort by the oldest 'Last Updated' date
        items = sorted(self.items, key=lambda x: (str(x.get('expires')), x.get('updated', ' ')), reverse=False)

        logging.info(f"expire_threshold: {expire_threshold} {type(expire_threshold)} - "
                     f"ignore_no_expiration: {ignore_no_expiration} ({type(ignore_no_expiration)}) - "
                     f"include_all: {include_all} {type(include_all)}")
        for item in items:
            row = ""

            # Get name of the secret. If no name, we skip to next item in the list
            name = item.get("name")
            if not name:
                continue

            # Get the expires and update values
            expires = item.get("expires", "")
            expires_age = item.get("expires_age")
            updated = item.get("updated")
            updated_age = item.get("updated_age")

            # Skip records with no Expiration Date set, only if 'ignore_no_expiration' and not 'include_all'
            if not expires:
                self.missing_expiration_date += 1
                if ignore_no_expiration and not include_all:
                    continue

            # Handle those with Expiration Date
            if isinstance(expires_age, int):

                # Handle those which has not expired yet
                if expires_age < 0:
                    logging.info(f"'{name}' has not expired yet. It will expire in {abs(expires_age)} days ({expires}).")

                    # Handle those within valid 'expire_threshold'
                    if isinstance(expire_threshold, int) and expire_threshold < abs(expires_age):
                        logging.info(f"'{name}' Expiration Date is within the valid specified threshold of "
                                     f"{expire_threshold} days. This record will start to be "
                                     f"reported in {abs(expires_age) - expire_threshold} days.")

                        # Only skipped if 'include_all' is not specified.
                        if not include_all:
                            continue

            # First column added is 'Name'. Second column is 'Last Updated'
            row += f"{self.lm}{name: <{self.table_columns[0][0]}}|"
            row += f" {updated: <{self.table_columns[1][0]}}|"

            # Third column added is 'Expiration'. If 'Expiration' value is empty, blank spaces are added instead.
            if expires:
                row += f" {expires: <{self.table_columns[2][0]}}|"
            else:
                row += self.table_columns[2][0] * " "
                row += " |"

            # The last column 'Comment' has to be created before added to the row.
            # The value of 'Comment' is dependent of the info from the expires and update values
            comment = ""
            if isinstance(expires_age, int):
                if expires_age <= 0:
                    comment += f"Will expire in {abs(expires_age)} days. "
                if expires_age > 0:
                    comment += f"Expired {expires_age} days ago. "

            if not expires:
                comment += f"Has no expiration date. "

            if isinstance(updated_age, int):
                comment += f"Updated {updated_age} days ago. "

            # Finally the 'Comment' column is added to the row, along with a linebreak for the row
            row += f" {comment}\n"

            # A little cosmetic touch to avoid plural where it should not be used
            self.body += row.replace(" 1 days", " 1 day")

            # Generate json with html table to be used in Teams
            if teams_json:
                self.add_html_row(name, updated, expires, comment)

        logging.info(f"{self.vault_name} - secret list report generated.")

        if teams_json:
            self.finalize_html()
            self.generate_json_facts()

        # Set the plain text report footer
        self.set_report_footer()

    def set_report_footer(self):
        """set the stats in the plain text report footer"""
        if not isinstance(self.result, list):
            return

        # Ensure footer starts with dotted line
        self.footer = self.sep_line

        # Add summary rows to the report
        if self.this_year:
            self.footer += f"{self.lm}Secrets updated in the last year.........: {self.this_year}\n"

        if self.one_year:
            self.footer += f"{self.lm}Secrets NOT updated in the last year.....: {self.one_year}\n"

        if self.two_years:
            self.footer += f"{self.lm}Secrets NOT updated for the last 2 years.: {self.two_years}\n"

        if self.three_years:
            self.footer += f"{self.lm}Secrets NOT updated for the last 3 years.: {self.three_years}\n"

        self.footer += f"{self.lm}Secrets missing Expiration Date..........: {self.missing_expiration_date}\n"
        self.footer += f"{self.lm}Total number of secrets..................: {len(self.items)}\n"
        self.footer += self.sep_line
        logging.info(f"footer generated.")

    def generate_html_table(self):
        """generates a html table to be used in json output for MS Teams"""
        self.html_table = f"""<table bordercolor='black' border='2'>
    <thead>
    <tr style='background-color : Teal; color: White'>
        <th>{self.table_columns[0][1]}</th>
        <th>{self.table_columns[1][1]}</th>
        <th>{self.table_columns[2][1]}</th>
        <th>{self.table_columns[3][1]}</th>
    </tr>
    </thead>
    <tbody>
    """
# add rows

    def add_html_row(self, *args):
        """adds the table rows to html table"""
        if not self.html_table:
            self.generate_html_table()
        self.html_table += "<tr>"
        for arg in args:
            self.html_table += f"<td>{arg}</td>"
        self.html_table += "</tr>"

    def finalize_html(self):
        """adding closing html tags and remove plural in days when it should not be used"""
        if self.html_table:
            self.html_table += "</tbody></table>"
            self.html_table = self.html_table.replace(" 1 days", " 1 day").replace("\n", "")

    def generate_json_facts(self):
        """generates the fact used in the json output for MS Teams"""
        if not isinstance(self.result, list):
            return

        self.facts = [
            {"name": "Total number of secrets:",
             "value": len(self.items)
             }
        ]

        if self.missing_expiration_date:
            self.facts.append(
                {"name": "Secrets missing Expiration Date:",
                 "value": self.missing_expiration_date
                 }
            )

        if self.this_year:
            self.facts.append(
                {"name": "Secrets updated in the last year:",
                 "value": self.this_year
                 }
            )

        if self.one_year:
            self.facts.append(
                {"name": "Secrets NOT updated in the last year:",
                 "value": self.one_year
                 }
            )

        if self.two_years:
            self.facts.append(
                {"name": "Secrets NOT updated for the last 2 years:",
                 "value": self.two_years
                 }
            )

        if self.three_years:
            self.facts.append(
                {"name": "Secrets NOT updated for the last 3 years:",
                 "value": self.three_years
                 }
            )

        logging.info(f"json summary generated.")

    def get_report(self):
        """return the plain text report"""

        # If a body has been generated, then the header is also included in the output.
        if self.body:
            return self.header + self.body + self.footer

        # Only the summary footer is output when a body has not been generated.
        return self.footer

    def get_json_output(self, report_if_no_html=False):
        """add the facts and text to the json output for MS Teams, and then return the json output

        If no items in the report, no payload is returned.

        If 'report_if_no_html' is set to True (default: False) a payload with the facts will be returned,
        even though there are no records to report in the html table.
        """

        if len(self.items) == 0:
            return None

        if not report_if_no_html and not self.html_table:
            return None

        self.json_output["sections"][0]["facts"] = self.facts
        self.json_output["sections"][1]["text"] = self.html_table

        return json.dumps(self.json_output)
