
import scrapy
import random
import time
from getuseragent import UserAgent
useragent = UserAgent()

myuseragent = UserAgent("all", requestsPrefix=True).Random()

class hh_Spider(scrapy.Spider):
    name="hh_Spider"
    start_urls=["https://tomsk.hh.ru/search/vacancy?L_save_area=true&search_field=name&area=113&order_by=salary_asc&search_period=30&items_on_page=20&hhtmFrom=vacancy_search_filter&text=Аналитик+данных&enable_snippets=false&only_with_salary=true"]
    # чтобы получить эту ссылку, настроил фильтр hh.ru и скопировал ссылку на открывщиеся страницу


    def parse(self, response):
        links=response.css("div.serp-item span.serp-item__title-link-wrapper a::attr(href)").getall()
        for link in links:
            time.sleep(random.randrange(0,5))
            with open('links.csv', 'a') as f:
                f.write(link + "\n")                
            yield response.follow(link, self.parse_hh, headers=myuseragent)
        next_page=response.css("div.pager  a::attr(href)").getall()[-1]
        if next_page is not None:
            next_page_url= "https://tomsk.hh.ru/"+next_page
            yield response.follow(next_page_url, self.parse, headers=myuseragent)   

    def parse_hh(self, response):
        yield {
                "вакансия":response.css("h1.bloko-header-section-1::text").get(),
                "ключевые навыки":response.css("div.bloko-tag-list div.bloko-tag span::text").getall(),
                "опыт работы":response.css("p.vacancy-description-list-item span::text").get(),
                "зарплата":response.css("div.vacancy-title div span.bloko-header-section-2::text").getall(),
                "название компании":response.css("span.vacancy-company-name span ::text").getall()[-1],
                "Звезды":response.css("div.AjI0Ncv___rating-container div::text").get(),
                "кол-во отзывов":response.css("div.XQ_6djb___small-widget button.bloko-link span::text").get()
                # "ссылка":link,
            }
        
 
