import requests
from bs4 import BeautifulSoup
from stringfoos import find_all, add_line_at, add_lines_at, remove_excess_lines

def get_last_event_slug(url):

  response = requests.get(url)
  html = response.text
  soup_chapter = BeautifulSoup(html, "html.parser")
  soup_last_event = soup_chapter.find("div", class_="panel-picture-content")

  if soup_last_event == None:
    return
    
  links = soup_last_event.findAll("a")
  last_event_slug = links[0].get('href')

  return last_event_slug

def get_event_url(slug):

  event_url = "https://gdsc.community.dev/" + slug

  return event_url

def get_event_info_soups(url):

  # Get the html for the event.
  response = requests.get(url)
  html = response.text
  event_soup = BeautifulSoup(html, "html.parser")

  # Get the soup for each event info.
  title_soup = event_soup.find("span", itemprop="name")
  address_soup = event_soup.find("span", itemprop="address")
  date_soup = event_soup.find("div", class_="event-date-time")
  short_description_soup = event_soup.find('p', attrs={'class' : 'event-short-description-on-banner'})
  big_description_soup = event_soup.find('div', attrs={'class' : 'event-description general-body'})

  return (title_soup, address_soup, date_soup, short_description_soup, big_description_soup, event_soup)

def get_index_html_tag(html_string, tag):

  index_list = [] + list(find_all(html_string, tag))

  return index_list

def prepare_big_description_soup(big_description_soup):

  description_string = str(big_description_soup)
    
  line_break_index = get_index_html_tag(description_string, '<br/>')
  paragraph_index = get_index_html_tag(description_string, '</p>')
  listed_start_index = get_index_html_tag(description_string, '<li>')
  listed_end_index = get_index_html_tag(description_string, '</li>')
  ord_list_index = get_index_html_tag(description_string, '</ol>')
  uno_list_index = get_index_html_tag(description_string, '</ul>')

  all_index = line_break_index + paragraph_index + listed_end_index + listed_start_index + ord_list_index + uno_list_index

  all_index.sort()
  all_index.reverse()

  for i in all_index:
    if i in line_break_index:
      description_string = add_line_at(i, description_string)
    elif i in paragraph_index:
      description_string = add_lines_at(i, description_string, 2)
    elif i in listed_start_index:
      description_string = description_string[:i] + "- " + description_string[i:]
    elif i in listed_end_index:
      description_string = add_line_at(i, description_string)
    elif i in ord_list_index:
      description_string = add_line_at(i, description_string)
    elif i in uno_list_index:
      description_string = add_line_at(i, description_string)
  # TODO - ol adds num ite (eg. 1. 2. 3. ...), ul adds '- '

  description_soup = BeautifulSoup(description_string, "html.parser")

  return description_soup

def get_title(title_soup):

  normal_title = title_soup.get_text()
  title = normal_title.upper()

  return title

def get_address(address_soup):

  if address_soup == None:
    return "Location TBD"

  bad_address = address_soup.get_text()
  sep_address = bad_address.rfind("-")
  address = bad_address[:sep_address]

  return address

def get_date(date_soup):

  event_date = date_soup.get_text()
  sep_date = event_date.rfind(",")

  day = event_date[:sep_date]
  event_time = event_date[(sep_date + 2):]

  return (day, event_time)

def get_description(small_description_soup, big_description_soup):

  if small_description_soup == None:
    description_soup = prepare_big_description_soup(big_description_soup)
  else:
    description_soup = small_description_soup

  description = description_soup.get_text()

  description = remove_excess_lines(description)

  return description

def get_tags(event_soup):

  possible_tags = ["Android","AR / VR","Assistant / Actions on Google","Career Development","Firebase","Flutter","Flutter Festival","Google Cloud Platform","International Women's Day (IWD)","Machine Learning / AI","Solution Challenge","UI / UX","Web"]

  tags_list = []

  soup_string = str(event_soup)

  index_tags = soup_string.find('tags')
  soup_string = soup_string[index_tags:(index_tags + 1700)]

  for tag in possible_tags:
    if tag in soup_string:
      tags_list.append(tag)

  tags = ' | '.join(tags_list)

  return tags

def get_event_info(url):

  # Get the soup for each event info.
  soups = get_event_info_soups(url)

  title_soup = soups[0]
  address_soup = soups[1]
  date_soup = soups[2]
  small_description_soup = soups[3]
  big_description_soup = soups[4]
  event_soup = soups[5]

  # Transform each soup into strings with the event info.
  title = get_title(title_soup)
  address = get_address(address_soup)

  day_time = get_date(date_soup)
  day = day_time[0]
  event_time = day_time[1]

  description = get_description(small_description_soup, big_description_soup)

  tags = get_tags(event_soup)

  return (title, address, day, event_time, description, tags, url)

def prepare_event_message(event_info):

  title = event_info[0]
  address = event_info[1]
  day = event_info[2]
  event_time = event_info[3]
  description = event_info[4]
  tags = event_info[5]
  url = event_info[6]

  event_message = r"""
\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//

**{}**

**{}** at **{}**
**{}**

{}

**{}**

Click here to **RSVP** for the event:
{}

\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//\\\\//
""".format(title, day, event_time, address, description, tags, url)

  return event_message
# TODO add clock emoji that reacts to the time by changing the emoji and dynamic emojis

def get_last_GDSCevent(url):

  slug = get_last_event_slug(url)

  if slug == None:
    return 'No new events'

  last_event_url = get_event_url(slug)
  event_info = get_event_info(last_event_url)
  event_message = prepare_event_message(event_info)

  return event_message

def foo(pizza, merch, googler):
  return
  # TODO create tags that are added under the event when there's pizza or to categorise the event