import json
import os
from shutil import copyfile
from collections import defaultdict

with open('data.json') as f:
  json_data = json.load(f)

def replace_text_in_file(old_text, new_text, filename):
  if not new_text: new_text = ""

  # Read in the file
  with open(filename, 'r') as file:
    filedata = file.read()

  # Replace the target string
  new_file_data = filedata.replace(old_text, new_text)
  
  # Write the file out again
  with open(filename, 'w') as file:
    file.write(new_file_data)


def generate_menu_list(json_data):
  pages = json_data["pages"]
  titles = sorted([ (page_name, page["title"]) for page_name, page in pages.items() if "index" in page and page["index"]])
  html_frag = ["<li><a href=\"./{}.html\">{}</a></li>".format(page_name, page) for page_name, page in titles]
  return "<ul>{}</ul>".format('\n'.join(html_frag))

def update_generic_params(filename):
  replace_text_in_file("{website_title}", "Suyash Shekhar", filename)
  replace_text_in_file("{menu_title}", "Suyash Shekhar", filename)
  replace_text_in_file("{menu_list}", generate_menu_list(json_data), filename)


def unpack_text_list(text_lst):
  if not isinstance(text_lst, list):
    return text_lst
  paragraphs = [f'<p> {text} </p>' for text in text_lst]
  return '\n'.join(paragraphs) 

def mark_menu_item_as_selected(filename):
  current_li = "href=\"./{}\">".format(filename)
  replacement = current_li.replace("href=", "id=\"selected\" href=")
  replace_text_in_file(current_li, replacement, filename)

def generate_page_list(items):
  if not items: return ""
  links = ["<li><a href=\"{}\">{}</a>{}</li>".format(item["link"], item["title"], ": {}".format(item["desc"]) if "desc" in item else "") for item in items]
  return "<ul>{}</ul>".format("\n".join(links))


def generate_html(page_name, data):
  filename = "{}.html".format(page_name)
  copyfile('template.txt', filename)

  update_generic_params(filename)
  replace_text_in_file("{page_title}", data["title"], filename)
  replace_text_in_file("{page_desc}", unpack_text_list(
      data["description"]), filename)
  replace_text_in_file("{text_above_embed}", unpack_text_list(
      data["text_above_embed"]), filename)
  replace_text_in_file("{embed_content}", data["embed"], filename)
  replace_text_in_file(
      "{page_list}", generate_page_list(data["list"]), filename)
  mark_menu_item_as_selected(filename)


# Generate index.html
generate_html('index', defaultdict(str))

# Main part
for page_name, data in json_data["pages"].items():
  generate_html(page_name, data)





