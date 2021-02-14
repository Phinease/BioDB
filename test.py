import cx_Oracle
import xml.etree.ElementTree as ET
import sys
import configparser
from uniprotLoadDB import UniprotParser, UniprotOracle
from builtins import Exception
from uniprotLoadDB.Comment import Comment
from uniprotLoadDB.DbRef import DbRef
from uniprotLoadDB.Entry import Entry
from uniprotLoadDB.GeneName import GeneName
from uniprotLoadDB.Keyword import Keyword
from uniprotLoadDB.Protein import Protein
from uniprotLoadDB.ProtName import ProtName

help()