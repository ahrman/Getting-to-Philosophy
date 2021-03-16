import re
import time

import requests
from bs4 import BeautifulSoup

philosophy_url = "https://en.wikipedia.org/wiki/Philosophy"
current_url = ""
visited_articles = []

# function that removes all parentheses and all text between them
# except in valid links, ex: 'https://en.wikipedia.org/wiki/Stimulus_(physiology)'


def ignore_parentheses(text):
    no_parentheses_after_quoutes = re.sub(r"\"\((.*?)\)", r'"', text)
    no_parentheses_after_tags = re.sub(r">\((.*?)\)", r">",
                                       no_parentheses_after_quoutes)
    no_parentheses_after_curly_brackets = re.sub(r"}\((.*?)\)", r"}",
                                                 no_parentheses_after_tags)
    no_parentheses_after_commas = re.sub(r",\((.*?)\)", r",",
                                         no_parentheses_after_curly_brackets)
    no_parentheses_after_periods = re.sub(r"\.\((.*?)\)", r".",
                                          no_parentheses_after_commas)
    no_parentheses_after_spaces = re.sub(r" \((.*?)\)", r" ",
                                         no_parentheses_after_periods)
    no_parentheses = no_parentheses_after_spaces
    return no_parentheses


def get_to_philosophy(url):

    not_philosophy = True

    while not_philosophy:
        time.sleep(0.5)
        response = requests.get(url)
        print(response.url)
        visited_articles.append(url)

        no_parentheses = ignore_parentheses(response.text)

        soup = BeautifulSoup(no_parentheses, features="lxml")

        # selects the tag containing the article body
        main_body = soup.select("#mw-content-text > div.mw-parser-output")

        # clears tags of tables, boxes, and footnotes
        for element in main_body[0].select(
                "span, table, sup, i, .thumbinner, .IPA"):
            element.clear()

        text_elements = main_body[0].find_all(["p", "ul", "ol"])

        # searches for wikipedia links inside of paragraphs, unordered lists, and ordered lists in article
        # and returns the url for the first valid link
        for text_element in text_elements:
            if text_element.find("a", href=re.compile("/wiki/")) is not None:
                href = text_element.find("a",
                                         href=re.compile("/wiki/")).get("href")
                url = "https://en.wikipedia.org" + href
                break

        # checks for infinite loops and Dead-end pages
        if url == philosophy_url:
            not_philosophy = False
            print(url)
            print("Reached Philosophy")
            break
        elif url in visited_articles:
            print(url)
            print("Loop detected")
            break


wikipedia_link = input()

get_to_philosophy(wikipedia_link)
