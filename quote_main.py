import requests
from bs4 import BeautifulSoup
from random import choice
import csv

# Will scrape quotes from "quotes.toscrape.com".
# Will check for "quote_data.csv" and create it, if not found.

def scraper():
	url = "http://quotes.toscrape.com/"
	responses = []
	responses.append(requests.get(url))
	data = []

	while True:
		soup = BeautifulSoup(responses[-1].text, "html.parser")
		if not soup.select(".next"):
			break
		link = soup.select(".next")[0]
		next_page_url = url + link.a['href']
		responses.append(requests.get(next_page_url))

		quotes = soup.select(".quote")
		for quote in quotes:
			quote_info = []
			quote_text = quote.select(".text")[0].get_text()
			author_name = quote.select(".author")[0].get_text()
			quote_link = quote.a.attrs["href"]
			quote_info.append(quote_text)
			quote_info.append(author_name)
			quote_info.append(quote_link)
			data.append(quote_info)
	return data

def csv_writer(data):
	with open("quote_data.csv", "w", newline="") as csvfile:
		headers = ["text", "author", "href"]
		my_writer = csv.writer(csvfile)
		my_writer.writerow(headers)
		for quote in data:
			print(quote)
			try:
				my_writer.writerow(quote)
			except UnicodeEncodeError:
				pass

def csv_reader():
	data = []
	with open("quote_data.csv", "r") as csvfile:
		my_reader = csv.reader(csvfile)
		for row in my_reader:
			data.append(row)
	return data

def main():
	try:
		quotes = csv_reader()
	except FileNotFoundError:
		csv_writer(scraper())
	game(csv_reader())

def game(data):
	reply = "y"
	url = "http://quotes.toscrape.com/"
	no_of_guess = 4
	while reply != "n":
		if no_of_guess == 0:
			reply = input("Would you like to play again(y/n): ")
			no_of_guess = 4
		if reply == "y":
			guess = choice(data)
			author_page = requests.get(url + guess[2])
			soup = BeautifulSoup(author_page.text, "html.parser")
			author_born_date = soup.select(".author-born-date")[0].get_text()
			author_born_place = soup.select(".author-born-location")[0].get_text()
			print("Here is a quote: \n")
			print(guess[0])
		while reply != "n":
			reply = input("\nWho said this? Guesses remaining: {} ".format(no_of_guess))
			no_of_guess -= 1
			if reply == guess[1]:
				print("Correct Guess!")
				break
			if no_of_guess == 3:
				print("Here a hint: The author was born on {} {}\n".format(author_born_date, author_born_place))
			if no_of_guess == 2:
				print("Heres another hint: The first initial of the author's name is {}\n".format(guess[1][0]))
			if no_of_guess == 1:
				name_split = guess[1].split()
				print("Heres one more hint: The second inital of the author's surname is {}\n".format(name_split[1][0]))
			if no_of_guess == 0:
				print("Sorry, you've run out of guesses! The author's name is {}\n".format(guess[1]))
				break

main()
