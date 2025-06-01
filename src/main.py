from textnode import *
from htmlnode import *
from functions import *
from markdown_to_htmlnode import *

def main():
   
   src = "/home/edo/workspace/github.com/edoleite/static_site_generator/static"
   dest = "/home/edo/workspace/github.com/edoleite/static_site_generator/public"
   copy_contents(src, dest)


main()


