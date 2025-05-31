from textnode import *
from htmlnode import *
from blocknode import *
from functions import *



def main():
   
   source = "/home/edo/workspace/github.com/edoleite/static_site_generator/static"
   dest = "/home/edo/workspace/github.com/edoleite/static_site_generator/public"
   copy_contents(source, dest)

   page_source = "/home/edo/workspace/github.com/edoleite/static_site_generator/content/index.md" 
   template = "/home/edo/workspace/github.com/edoleite/static_site_generator/template.html"
   page_dest = "/home/edo/workspace/github.com/edoleite/static_site_generator/public/index.html"
   generate_page(page_source, template, page_dest)

main()


