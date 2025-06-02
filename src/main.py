from textnode import *
from htmlnode import *
from functions import *
from blocknode import *
import sys


def main():

   if len(sys.argv) > 1:
      basepath = sys.argv[1]
   else:
      basepath = "/"
   
   src = "/home/edo/workspace/github.com/edoleite/static_site_generator/static"
   dest = "/home/edo/workspace/github.com/edoleite/static_site_generator/docs"
   copy_contents(src, dest)

   
   
   src = "/home/edo/workspace/github.com/edoleite/static_site_generator/content"
   dest = "/home/edo/workspace/github.com/edoleite/static_site_generator/docs"
   temp = "/home/edo/workspace/github.com/edoleite/static_site_generator/template.html"

   generate_pages_recursive(src, temp, dest, basepath)
   


main()


