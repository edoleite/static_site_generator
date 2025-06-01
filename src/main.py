from textnode import *
from htmlnode import *
from functions import *
from blocknode import *


def main():
   
   src = "/home/edo/workspace/github.com/edoleite/static_site_generator/static"
   dest = "/home/edo/workspace/github.com/edoleite/static_site_generator/public"
   copy_contents(src, dest)

   
   
   src = "/home/edo/workspace/github.com/edoleite/static_site_generator/content"
   dest = "/home/edo/workspace/github.com/edoleite/static_site_generator/public"
   temp = "/home/edo/workspace/github.com/edoleite/static_site_generator/template.html"

   generate_pages_recursive(src, temp, dest)
   


main()


