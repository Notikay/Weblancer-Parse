import requests
import re
from bs4 import BeautifulSoup as bs

def parser(soup, projects):

	cols = soup.find('div', attrs={'class': 'cols_table'}) # Поиск div'а с контентом.
	
	for rows in cols.find_all('div', attrs={'class': 'row'}):
		
		# Поиск заголовка/ссылки/описания.
		title = rows.find('h2').text
		href = rows.find('h2').a['href']
		description = rows.find('p').text

		chekpoint = rows.next_element.next_sibling # Общая точка поиска элементов.

		# Зарплата.
		cash = chekpoint.next_element.text
		if cash == '':
			cash = 'Не указано'

		# Количество заявок.
		application = chekpoint.next_element.next_sibling.text
		application = application.strip()

		# Тип разработки.
		type_dev = chekpoint.next_sibling.text

		# Срок публикации.
		limit = rows.find('span', attrs={'class': 'time_ago'}).text

		projects.append({
			"Заголовок": title,
			"Ссылка": href,
			"Описание": description,
			"Зарплата": cash,
			"Заявки": application,
			"Тип": type_dev,
			"Срок": limit
			})
	return projects

def main(base_url, headers):

	urls = []

	session = requests.Session()
	request = session.get(base_url, headers = headers)

	if request.status_code == 200:

		soup = bs(request.content, 'lxml').find('div', attrs={'class': 'page_content'})
		
		# Определение максимального количества страниц с помощью пагинации.
		pagination = soup.find('div', attrs={'class': 'pagination_box'})
		pag_row = pagination.next_element
		pag_div = pag_row.next_element.next_sibling.next_sibling
		pag_href = pag_div.a['href']

		max_page = int(pag_href[43:]) # Максимальное количество страниц.

		for i in range(1, max_page+1):
			url = f'https://www.weblancer.net/jobs/programmirovanie-po-i-sistem-2/?page={i}'
			urls.append(url)
	else:
		print("Ошибка")

	for url in urls:

		projects = []

		request = session.get(url, headers = headers)
		soup = bs(request.content, 'lxml').find('div', attrs={'class': 'page_content'})

		projects = parser(soup, projects)

		with open("parse.txt", "a", encoding = 'utf-8') as file:
			for prj in projects:
				for key, value in prj.items():
					file.write(key + ": " + value +"\n")
				file.write("\n")

if __name__ == '__main__':
	
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
	base_url = "https://www.weblancer.net/jobs/programmirovanie-po-i-sistem-2/?page=1"
	
	main(base_url, headers)