#!/usr/bin/python
# Copyright 2016 Shea G. Craig
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Spruce includes tools to analyze the quality of a Munki repo, as wll
as commands to automate archiving or removing unwanted items, and for
making bulk data changes to metadata as well as deployment settings
by product, category, etc.
"""


import argparse

import munki_tools


def main():
    """Handle arguments and execute commands."""
    args = get_argument_parser().parse_args()
    args.func(args)


def get_argument_parser():
    """Create our argument parser."""
    description = ("Spruce is a tool for improving the quality of your Munki "
                   "repo.")
    parser = argparse.ArgumentParser(description=description)
    subparser = parser.add_subparsers(help="Sub-command help")

    phelp = (
        "Output all unique product names present in the Munki all catalog.")
    names_parser = subparser.add_parser("name", help=phelp)
    names_parser.set_defaults(func=munki_tools.run_names)
    phelp = "Show each version of the software per name."
    names_parser.add_argument("-v", "--version", help=phelp,
                              action="store_true")

    # categories arguments
    phelp = ("List all categories present in the repo, and the count of "
             "pkginfo files in each, or show members of a single category..")
    categories_parser = subparser.add_parser("category", help=phelp)
    categories_parser.set_defaults(func=munki_tools.run_categories)
    phelp = "Name of one or more categories to display."
    categories_parser.add_argument("category", help=phelp, nargs="*")
    phelp = ("Output a plist representation of all pkginfo files organized by "
             "category. This file can be used with the recategorize command.")
    categories_parser.add_argument("-p", "--prepare", help=phelp,
                                   action="store_true")

    # recategorize arguments
    phelp = ("Recategorize products based on an input plist generated by "
             "the prepare command.")
    update_parser = subparser.add_parser("recategorize", help=phelp)
    phelp = ("Path to a plist file containing the desired changes to product "
             "categories. This file may be generated by the category command. "
             "See the documentation for more details.")
    update_parser.add_argument("plist", help=phelp)
    update_parser.set_defaults(func=munki_tools.update_categories)

    # deprecate arguments
    phelp = (
        "Remove unwanted products from a Munki repo. Pkg and pkginfo files "
        "will be removed, or optionally can be archived in an archive repo. "
        "All products to be completely removed will then have their names "
        "removed from all manifests.")
    dep_parser = subparser.add_parser("deprecate", help=phelp)
    dep_parser.set_defaults(func=munki_tools.deprecate)

    phelp = ("Move, rather than delete, pkginfos and pkgs to the archive repo "
             "rooted at 'ARCHIVE'. The original folder structure will be "
             "preserved.")
    dep_parser.add_argument("-a", "--archive", help=phelp)
    phelp = "Don't prompt before removal or archiving procedure."
    dep_parser.add_argument("-f", "--force", help=phelp, action="store_true")

    deprecator_parser = dep_parser.add_argument_group("Deprecation Arguments")
    phelp = "Remove all pkginfos and pkgs with category 'CATEGORY'."
    deprecator_parser.add_argument("-c", "--category", help=phelp, nargs="+")
    phelp = "Remove all pkginfos and pkgs with name 'NAME'."
    deprecator_parser.add_argument("-n", "--name", help=phelp, nargs="+")

    # icons arguments
    phelp = "Report on unused icons and optionally remove or archive them."
    icon_parser = subparser.add_parser("icons", help=phelp)
    icon_parser.set_defaults(func=munki_tools.handle_icons)

    group = icon_parser.add_mutually_exclusive_group()
    phelp = "Delete unused icons."
    group.add_argument("-d", "--delete", help=phelp, action="store_true")
    phelp = ("Move, rather than delete, icons to the archive repo "
             "rooted at 'ARCHIVE'. The original folder structure will "
             "be preserved.")
    group.add_argument("-a", "--archive", help=phelp)
    phelp = "Don't prompt before removal or archiving procedure."
    icon_parser.add_argument("-f", "--force", help=phelp, action="store_true")

    return parser


if __name__ == "__main__":
    main()
